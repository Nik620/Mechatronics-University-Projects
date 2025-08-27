%%% Part 1 - 2D TRUSS STRUCTURES %%%
clear all, close all
format compact

%%% GIVEN %%%
P = 600000; % Load (N)
a = 1; % Length (m)
A = 4E-4; % Area (sqm)
I = 4E-6; % Inertia (m^4)
E = 200E9; % Modulus of Elasticity (Pa)
EA = E * A;

% Nodal coordinates
nodes = [0 0; % node 1, origin
         a 0; % node 2
         2*a 0; % node 3
         (a*cosd(60)) (a*sind(60)); % node 4
         (a+a*cosd(60)) (a*sind(60))]; % node 5
n = size(nodes, 1); % number of nodes

% Elements
elem = [1 2 EA; % element 1 
        2 3 EA; % element 2 
        1 4 EA; % element 3 
        2 4 EA; % element 4 
        2 5 EA; % element 5 
        3 5 EA; % element 6 
        4 5 EA]; % element 7
m = size(elem, 1); % number of elements

%%% CALCULATIONS %%%
K = zeros(2*n, 2*n);

for q = 1:m
    i = elem(q, 1); xi = nodes(i, 1); yi = nodes(i, 2); % coordinates of node i
    j = elem(q, 2); xj = nodes(j, 1); yj = nodes(j, 2); % coordinates of node j
    L = sqrt((xj - xi)^2 + (yj - yi)^2); Lv(q) = L;
    kq = elem(q, 3) / L; % Stiffness
    tht = atan2((yj - yi), (xj - xi)); % Angle
    Ne = kq * [-cos(tht); -sin(tht); cos(tht); sin(tht)];
    Nev(q,:) = Ne;
    Ke = 1/kq * Ne * Ne';
    edofs = [2*j-1, 2*i, 2*j-1, 2*j];
    K(edofs, edofs) = K(edofs, edofs) + Ke;
end

% Boundary conditions
fix_dofs = [1 2 3 4 5 6]; % Fixed at nodes 1, 2, and 3 (both x and y directions)
free_dofs = setdiff([1:2*n], fix_dofs); % Free DOFs

% Loads
fc1 = zeros(2*n, 1);
fc1([8, 10]) = -P; % Load applied at nodes 4 and 5

% Solution
uc1 = zeros(2*n, 1); 
uc1(free_dofs) = K(free_dofs, free_dofs) \ fc1(free_dofs);

%%% PLOTS %%%
% Plot deformation
figure(1)
hold on
grid on
grid minor
title("Original vs. Deformed Elements, Load 1", "FontSize", 15)
xlabel("Unit Length (a)", "FontSize", 10)
ylabel("Unit Length (a)", "FontSize", 10)

for q = 1:m
    i = elem(q, 1); j = elem(q, 2);
    xi = nodes(i, 1); yi = nodes(i, 2); % Undeformed configuration
    xj = nodes(j, 1); yj = nodes(j, 2);
    xid = xi + uc1(2*i-1); yid = yi + uc1(2*i); % Deformed configuration
    xjd = xj + uc1(2*j-1); yjd = yj + uc1(2*j);
    plot([xi, xj], [yi, yj], 'k-o') % Original structure
    plot([xid, xjd], [yid, yjd], 'b-o') % Deformed structure
end
legend('Original - black', 'Deformation - blue', 'Location', 'southoutside')

% Plot tension/compression
figure(2)
hold on
grid on
grid minor
title("Compression vs. Tension Elements, Load 1", "FontSize",15)
xlabel("Unit Length (a)", "FontSize", 10)
ylabel("Unit Length (a)", "FontSize", 10)

disp("Element Forces (N)")
for q = 1:m
    i = elem(q, 1); j = elem(q, 2);
    xi = nodes(i, 1); yi = nodes(i, 2); % Undeformed configuration
    xj = nodes(j, 1); yj = nodes(j, 2);
    Neq = Nev(q,:);
    edofs = [2*i-1, 2*i, 2*j-1, 2*j];
    Nq = Neq * uc1(edofs);
    Nv(q) = Nq;
    if Nq > 0
        plot([xi, xj], [yi, yj], 'r', 'LineWidth', .01);  % Tension, red color
    elseif Nq < 0
        plot([xi, xj], [yi, yj], 'b', 'LineWidth', .01);  % Compression, blue color
    else
        plot([xi, xj], [yi, yj], 'k', 'LineWidth', .01); % No load
    end
    xmid = (.6*xi + .4*xj);
    ymid = (.6*yi + .4*yj); 

    fij = sprintf('%.2f', Nq);
    disp(fij)
    text(xmid, ymid, fij, 'FontSize', 8, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle')
end
legend('Tension - red', 'Compression - blue', 'Location', 'southoutside')

figure(1)
title("Original vs. Deformed Elements, Load 1", "FontSize",15)
xlabel("Unit Length (a)", "FontSize", 10)
ylabel("Unit Length (a)", "FontSize", 10)

figure(2)
title("Compression vs. Tension Elements, Load 1", "FontSize",15)
xlabel("Unit Length (a)", "FontSize", 10)
ylabel("Unit Length (a)", "FontSize", 10)

% Rotations
uc1_reshaped = reshape(uc1, 2, [])'; % The transpose (') is used to get a 4x2 matrix
nodes2 = nodes + uc1_reshaped; % Deformed node positions
rotations = zeros(m, 1); % Initialize rotations array

for q = 1:m
    i = elem(q, 1); % Index of the first node of the element
    j = elem(q, 2); % Index of the second node of the element
    
    % Undeformed configuration
    xi1 = nodes(i, 1); yi1 = nodes(i, 2); 
    xj1 = nodes(j, 1); yj1 = nodes(j, 2);
    
    % Deformed configuration
    xi2 = nodes2(i, 1); yi2 = nodes2(i, 2); 
    xj2 = nodes2(j, 1); yj2 = nodes2(j, 2);
    
    % Initial angle
    initial_angle = atan2((yj1 - yi1), (xj1 - xi1)); 
    
    % Deformed angle
    deformed_angle = atan2((yj2 - yi2), (xj2 - xi2)); 
    
    % Rotation
    rotations(q) = (deformed_angle - initial_angle) * 180/pi;
    
    % Adjust for small numerical precision errors
    if abs(rotations(q)) < 1e-10
        rotations(q) = 0;
    end
end

disp('Rotations (in degrees):')
disp(rotations)

disp('Displacement (in meters):')
disp(uc1_reshaped)
