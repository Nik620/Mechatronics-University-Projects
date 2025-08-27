% Clear environment and load data
clear all; close all; clc;
format compact;

% Load your data
data = readtable('solar_data_10.4kW_sept.xlsx', 'VariableNamingRule', 'preserve');


% Data
base_daily        = data.('Base Daily Price ($)');
tier_1            = data.('Tier 1 Pricing ($/kWh)');
demand_house      = data.('Household Demand (kWh)');
solar_AC_out      = data.('AC System Output (W)') / 1000; % to kW/kWh
ytd               = data.('YTD (Num days since start of year)');
tracked_time      = data.('Date/Time');

% Normalize date/time 
data.DateTime = datetime(tracked_time, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');

% Threshold for switching between tier 1/2 pricing
tier_threshold = 650;

% Initialize reference signal
P_demand = demand_house;

% Initialize control signals
P_grid    = zeros(height(data), 1);
P_battery = zeros(height(data), 1);

% Initialize State Vectors
P_solar = solar_AC_out;
SoC     = zeros(height(data), 1);
P_output = P_grid + P_battery + P_solar;

% Pricing
C_T1 = tier_1;
C_Daily = base_daily;

% Other
unique_days = unique(ytd); % Use unique ytd values to identify days
daily_cost = zeros(length(unique_days), 1); % Initialize daily cost array
max_battery_capacity = 3.8; % Max capacity (kWh)
min_battery_capacity = 0; % Min capacity (kWh)
max_soc = 100; % Max SoC percentage
min_soc = 0; % Min SoC percentage
base_daily_cost = base_daily; % Base daily cost

% Loop through each unique day
for d_idx = 1:length(unique_days)
    d = unique_days(d_idx);

    % Identify the indices for the current day
    day_indices = find(ytd == d);

    P_battery_day = zeros(length(day_indices), 1);
    SoC_day = zeros(length(day_indices), 1);
    P_output_day = zeros(length(day_indices), 1);
    P_grid_day = zeros(length(day_indices), 1);

    for k = 1:length(day_indices)
        idx = day_indices(k);

        % Convert solar power output from W to kWh
        P_solar_k = max(P_solar(idx), 0); % Ensuring solar output is non-negative
        P_demand_k = P_demand(idx);

        % Calculate net power: PV output - household demand
        P_net = P_solar_k - P_demand_k;

        % Calculate battery power based on conditions
        if P_net > 0
            % Excess power: Charge the battery first
            P_battery_day(k) = min(P_net, (max_battery_capacity - SoC_day(k) * max_battery_capacity / 100));
            
            % After charging the battery, any remaining power goes to the grid
            P_remaining = P_net - P_battery_day(k);
            if P_remaining > 0
                P_grid_day(k) = -P_remaining; % Feeding excess power back to the grid
            end
        else
            % Deficit: Discharge the battery or draw from the grid if SoC is zero
            if SoC_day(k) > min_soc
                P_battery_day(k) = max(P_net, (min_battery_capacity - SoC_day(k) * max_battery_capacity / 100));
            else
                P_battery_day(k) = 0; % No discharge possible, set battery power to zero
            end
        end

        % Update state of charge, constrained between 0% and 100%
        SoC_day(k) = max(min(SoC_day(k) + P_battery_day(k) / max_battery_capacity * 100, max_soc), min_soc);

        % Calculate the output power
        P_output_day(k) = P_solar_k + P_battery_day(k);

        % If the battery is not sufficient, draw from the grid
        if SoC_day(k) == 0 && P_solar_k == 0
            P_grid_day(k) = P_demand_k; % Draw all power from the grid
        else
            P_grid_day(k) = max(P_demand_k - P_output_day(k), 0); % Draw remaining power from the grid if needed
        end
    end

    % Update overall variables for the day
    P_battery(day_indices) = P_battery_day;
    SoC(day_indices) = SoC_day;
    P_output(day_indices) = P_output_day;
    P_grid(day_indices) = P_grid_day;

    % Apply pricing logic after determining grid energy consumed for the day
    daily_pricing = max(C_T1(day_indices), 0); % Ensuring tier 1 pricing is non-negative

    % Calculate total cost for the day based on grid energy consumed and pricing
    daily_grid_cost = sum(P_grid_day .* daily_pricing);
    daily_cost(d_idx) = daily_grid_cost + base_daily_cost(day_indices(1));
end


%% Part 2 - SINDy Setup and Visualization

% Create the control inputs u based on battery power and grid power
u = [P_battery, P_grid];

% Update state variables x to include grid power, battery power, solar AC output, output power, and SoC
x = [P_grid, P_battery, P_solar, P_output, SoC];

% Set daily cost as the output variable y
y = daily_cost;

% Define the state names for plotting
state_names = {'Grid Power', 'Battery Charge/Supply', 'Solar AC Output', 'Output Power', 'State of Charge'};

% Display the state vector outputs
disp('State Vector Outputs (x):');
disp(x);

% Display the control values (u):
disp('Control Values (u):');
disp(u);

% Define the time vector based on the sampling interval (e.g., hourly data)
time = (0:(height(data)-1))'; % Assuming the data is sampled hourly

% Display the time vector for verification
disp('Time Vector:');
disp(time);

% Calculate derivatives of state variables (use finite differences)
dX = zeros(size(x));
for i = 1:(size(x, 1) - 1)
    dt = time(i + 1) - time(i);
    dX(i, :) = (x(i + 1, :) - x(i, :)) / dt;
end
dX(end, :) = dX(end-1, :);  % Use the previous derivative for the last point

% Transpose dX to align dimensions correctly for pseudoinverse calculation
dX_T = dX';

% Construct the library matrix ThetaXU
ThetaXU = [
    ones(size(time))';
    x(:, 1)';
    x(:, 2)';
    x(:, 3)';
    x(:, 4)';
    x(:, 5)';
    u(:, 1)'; % Battery power as control input
    u(:, 2)'; % Grid power as control input
    % Interaction terms
    x(:, 1)'.*x(:, 2)';
    x(:, 1)'.*x(:, 3)';
    x(:, 1)'.*x(:, 4)';
    x(:, 1)'.*x(:, 5)';
    x(:, 2)'.*x(:, 3)';
    x(:, 2)'.*x(:, 4)';
    x(:, 2)'.*x(:, 5)';
    x(:, 3)'.*x(:, 4)';
    x(:, 3)'.*x(:, 5)';
    x(:, 4)'.*x(:, 5)';
    % Quadratic terms
    x(:, 1)'.^2;
    x(:, 2)'.^2;
    x(:, 3)'.^2;
    x(:, 4)'.^2;
    x(:, 5)'.^2;
    % Derivatives of the state variables
    dX_T(1, :);
    dX_T(2, :);
    dX_T(3, :);
    dX_T(4, :);
    dX_T(5, :);
    % Sinusoidal terms
    sin(x(:, 1))';
    sin(x(:, 2))';
    sin(x(:, 3))';
    sin(x(:, 4))';
    sin(x(:, 5))';
    cos(x(:, 1))';
    cos(x(:, 2))';
    cos(x(:, 3))';
    cos(x(:, 4))';
    cos(x(:, 5))';
    % Sinusoidal terms for u
    sin(u(:, 1))';
    cos(u(:, 1))';
    sin(u(:, 2))';
    cos(u(:, 2))';
]';

% Display ThetaXU for verification
disp('Library Matrix ThetaXU:');
disp(size(ThetaXU));

% Display the dimensions of dX_T and ThetaXU for verification
disp('Dimensions of dX_T:');
disp(size(dX_T)); % Should be 5 x N (number of samples)
disp('Dimensions of ThetaXU:');
disp(size(ThetaXU)); % Should be N x number of terms

% Verify Dimensions of ThetaXU and dX_T
if size(ThetaXU, 1) == size(dX_T, 2) % Adjusted dimension check
    % Use the sparsifyDynamics function for sparse regression
    lambda = 0.0000001; % Regularization parameter
    n = size(dX_T, 1); % State dimension
    Xi = sparsifyDynamics(ThetaXU, dX_T', lambda, n);

    % Display sparse coefficients for verification
    disp('Sparse Coefficients (Xi):');
    disp(Xi);

    % Simulate predicted state variables
    x_predicted = ThetaXU * Xi;

    % Ensure x_predicted has correct dimensions
    x_predicted = x_predicted';

    % Display the dimensions of x_predicted for verification
    disp('Dimensions of x_predicted:');
    disp(size(x_predicted)); % Should match x

    % Create a new figure for subplots
    figure('Name', 'SINDYc Controller Results', 'NumberTitle', 'off');

    % Number of state variables to plot
    num_states = size(x, 2);

    % Loop through each state variable and create a subplot
    for i = 1:num_states
        subplot(3, 3, i); % Create a subplot in a 3x3 grid
        plot(time, x(:, i), 'b', 'LineWidth', 1.5); % True state
        hold on;
        plot(time, x_predicted(i, :), 'r--', 'LineWidth', 1.5); % Simulated state
        title(['Comparison of ', state_names{i}]);
        legend('True', 'Simulated');
        xlabel('Time');
        ylabel(state_names{i});
    end

    % Plot the control input (P_battery)
    subplot(3, 3, 6);
    plot(time, u(:, 1), 'b', 'LineWidth', 1.5); % True control input (P_battery)
    hold on;
    plot(time, x_predicted(2, :), 'r--', 'LineWidth', 1.5); % Simulated control input (P_battery)
    title('Comparison of Control Input (P_battery)');
    legend('True', 'Simulated');
    xlabel('Time');
    ylabel('Control Input (P_battery)');

    % Plot the control input (P_grid)
    subplot(3, 3, 7);
    plot(time, u(:, 2), 'b', 'LineWidth', 1.5); % True control input (P_grid)
    hold on;
    plot(time, x_predicted(1, :), 'r--', 'LineWidth', 1.5); % Simulated control input (P_grid)
    title('Comparison of Control Input (P_grid)');
    legend('True', 'Simulated');
    xlabel('Time');
    ylabel('Control Input (P_grid)');

    % Plot the daily cost
    subplot(3, 3, 8);
    plot(unique_days, y, 'b', 'LineWidth', 1.5); % True output (daily cost)
    hold on;
    plot(unique_days, daily_cost, 'r--', 'LineWidth', 1.5); % Simulated output (daily cost)
    title('Comparison of Output y (Daily Cost)');
    legend('True', 'Simulated');
    xlabel('Day');
    ylabel('Cost ($)');

    % Save the combined figure
    savefig('SINDYc_Controller_Results.fig');
else
    disp('Error: Dimensions of ThetaXU and dX_T do not match for matrix division.');
end

%% Part 3 - MPC and Visualization

% Define MPC Parameters
horizon = 24 * 3; % Example prediction horizon (3 days)
control_horizon = 1; % Control horizon (e.g., 1 hour)
num_iterations = height(data) - horizon;

% MPC Constraints
P_battery_min = -max_battery_capacity; 
P_battery_max = max_battery_capacity;
P_grid_min = 0; % Minimum grid power (kWh)
P_grid_max = inf; % Maximum grid power (kWh)
solar_AC_out_min = 0;
solar_AC_out_max = 7;
soc_min = 0; % Minimum state of charge (%)
soc_max = 100; % Maximum state of charge (%)
P_out_min = 0;
P_out_max = inf;

% Set up the optimization problem
mpc_options = optimoptions('quadprog', 'Display', 'off');
Q = eye(size(x, 2)); % State weighting matrix, adjusted for new state vector size
R = eye(size(u, 2)); % Control weighting matrix

% Initialize the MPC controller variables
u_mpc = zeros(num_iterations, size(u, 2)); % Control inputs (P_battery and P_grid)
x_mpc = zeros(num_iterations + 1, size(x, 2)); % State variables

% Initial state
x_mpc(1, :) = [P_grid(1), P_battery(1), P_solar(1), P_output(1), SoC(1)];

% Simulate the MPC controller
for k = 1:num_iterations
    % Extract current state
    x0 = x_mpc(k, :)';
    
    % Define the cost function
    H = blkdiag(kron(eye(horizon), Q), kron(eye(horizon), R));
    f = zeros(size(x, 2) * horizon + size(u, 2) * horizon, 1);
    
    % Define the constraints
    Aineq = [];
    bineq = [];
    Aeq = [];
    beq = [];
    
    % Define the lower and upper bounds for the decision variables
    lb = [repmat([P_grid_min; P_battery_min; solar_AC_out_min; soc_min; P_out_min], horizon, 1); repmat(P_battery_min, horizon, 1); repmat(P_grid_min, horizon, 1)];
    ub = [repmat([P_grid_max; P_battery_max; solar_AC_out_max; soc_max; P_out_max], horizon, 1); repmat(P_battery_max, horizon, 1); repmat(P_grid_max, horizon, 1)];
        
    % Solve the optimization problem
    z = quadprog(H, f, Aineq, bineq, Aeq, beq, lb, ub, [], mpc_options);
    
    % Extract the optimal control input
    u_mpc(k, :) = z(end-size(u, 2)+1:end)';
    
    % Simulate the system with the optimal control input
    x_mpc(k + 1, :) = x0' + [P_grid(k+1), P_battery(k+1), P_solar(k+1), P_output(k+1), SoC(k+1)] + z(1:size(x, 2))';
end

% Visualization
figure('Name', 'MPC Controller Results', 'NumberTitle', 'off');
hold on;

% Plot the actual state vs. predicted state
for i = 1:5
    subplot(3, 3, i);
    plot(time, x(:, i), 'b', 'LineWidth', 1.5); % Actual state
    hold on;
    plot(time(1:num_iterations), x_mpc(1:num_iterations, i), 'r--', 'LineWidth', 1.5); % MPC state
    title(['State ', state_names{i}]);
    legend('Actual', 'MPC');
    xlabel('Time');
    ylabel(state_names{i});
end

% Plot the control input (P_battery)
subplot(3, 3, 6);
plot(time, u(:, 1), 'b', 'LineWidth', 1.5); % Actual control input (P_battery)
hold on;
plot(time(1:num_iterations), u_mpc(1:num_iterations, 1), 'r--', 'LineWidth', 1.5); % MPC control input (P_battery)
title('Comparison of Control Input (P_battery)');
legend('Actual', 'MPC');
xlabel('Time');
ylabel('Control Input (P_battery)');

% Plot the control input (P_grid)
subplot(3, 3, 7);
plot(time, u(:, 2), 'b', 'LineWidth', 1.5); % Actual control input (P_grid)
hold on;
plot(time(1:num_iterations), u_mpc(1:num_iterations, 2), 'r--', 'LineWidth', 1.5); % MPC control input (P_grid)
title('Comparison of Control Input (P_grid)');
legend('Actual', 'MPC');
xlabel('Time');
ylabel('Control Input (P_grid)');

% Plot the daily cost
subplot(3, 3, 8);
plot(unique_days, y, 'b', 'LineWidth', 1.5); % True output (daily cost)
hold on;
plot(unique_days, daily_cost, 'r--', 'LineWidth', 1.5); % Simulated output (daily cost)
title('Comparison of Output y (Daily Cost)');
legend('True', 'Simulated');
xlabel('Day');
ylabel('Cost ($)');

% Save the combined figure
savefig('MPC_Controller_Results.fig');

% Save the total cost figure
savefig('Total_Cost_Function.fig');

% Save all necessary data to a .mat file for future use
save('MPC_SINDyC_data.mat', 'x', 'u', 'time', 'unique_days', 'y', 'x_mpc', 'u_mpc');



%%Part 4
% SparsifyDynamics Function Definition
% function Xi = sparsifyDynamics(ThetaXU, dX, lambda, n)
%     % Perform sparse regression to identify the system's dynamics
%     Xi = zeros(size(ThetaXU, 2), n);
%     for k = 1:n
%         Xi(:, k) = lasso(ThetaXU, dX(:, k), 'Lambda', lambda);
%     end
% end

function Xi = sparsifyDynamics(Theta,dXdt,lambda,n)
% Copyright 2015, All Rights Reserved
% Code by Steven L. Brunton
% For Paper, "Discovering Governing Equations from Data: 
%        Sparse Identification of Nonlinear Dynamical Systems"
% by S. L. Brunton, J. L. Proctor, and J. N. Kutz

% compute Sparse regression: sequential least squares
Xi = Theta\dXdt;  % initial guess: Least-squares

% lambda is our sparsification knob.
for k=1:10
    smallinds = (abs(Xi)<lambda);   % find small coefficients
    Xi(smallinds)=0;                % and threshold
    for ind = 1:n                   % n is state dimension
        biginds = ~smallinds(:,ind);
        % Regress dynamics onto remaining terms to find sparse Xi
        Xi(biginds,ind) = Theta(:,biginds)\dXdt(:,ind); 
    end
end
end