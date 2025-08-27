%%% Part 2 - Plane Strain/Stress %%%

%%% a2D continuum structure %%%
clear all, close all, clc

% Plot parameters
nms = 3; % node marker size for displacements plot

% Material properties
E = 1; % Young modulus in [N/m^2]
v = 0.3;

% Size of the structure
Lx = 2; % length of the structure in x-direction [m]
Ly = 1;
D = 0.4; % diameter of the hole

% Mesh
nx = 10*Lx; % n. elements in x
ny = 10*Ly;
m = nx*ny; % total n. of elements
Dx = Lx/nx; % size of the element along x
Dy = Ly/ny;

% Nodes
N = (nx+1)*(ny+1); % total n. of nodes

% Node grid - we use here a grid numeration
ix = [1:nx+1];
iy = [1:ny+1];

% Node coordinates
x = (ix-1)*Dx;
y = (iy-1)*Dy;
[xn,yn] = meshgrid(x,y);

% Hole dimensions and coordinates
R = D/2 - 0.01; % accountfor error
center = [Lx/2,Ly/2];

% Stiffness matrix
K = zeros(2*N,2*N);
Em = [1 v 0;
      v 1 0;
      0 0 (1-v)/2]*E/(1-v^2); % plane stress
% Em = [(1-v) v 0;
%       v (1-v) 0;
%       0 0 (1-2*v)/2]*E/((1+v)*(1-2*v)); % plane strain

% Gauss points
g(1,:) = 1/sqrt(3)*[-1,-1]; % the matrix g contains the coordinates of the Gaussian points
g(2,:) = 1/sqrt(3)*[1,-1];
g(3,:) = 1/sqrt(3)*[-1,1];
g(4,:) = 1/sqrt(3)*[1,1];

for ex = 1:nx
    for ey = 1:ny
        i = (ey-1)*(nx+1)+ex;
        j = i+nx+1;
        x1 = xn(ey,ex); x2 = xn(ey,ex+1); x3 = x1; x4 = x2;
        y1 = yn(ey,ex); y2 = y1; y3 = yn(ey+1,ex); y4 = y3;
        
        % Hole
        distance = sqrt((x1 - center(1))^2 + (y1 - center(2))^2); 
        if distance <= R 
            xn(ey, ex) = NaN; 
            yn(ey, ex) = NaN;
            continue
        end

        Kq = 0;
        for gg = 1:4 % the four Gauss points
            xx = g(gg,1);
            yy = g(gg,2);
            Nxx = [-0.25*(1-yy), 0.25*(1-yy), -0.25*(1+yy), 0.25*(1+yy)];
            Nyy = [-0.25*(1-xx), -0.25*(1+xx), 0.25*(1-xx), 0.25*(1+xx)];
            J = [Nxx*[x1;x2;x3;x4], Nxx*[y1;y2;y3;y4]; Nyy*[x1;x2;x3;x4], Nyy*[y1;y2;y3;y4]];
            dJ = det(J);
            iJ = inv(J);
            A= (1/dJ)*([J(2,2) -1*J(1,2) 0 0; 0 0 -1*J(2,1) J(1,1); -1*J(2,1) J(1,1) J(2,2) -1*J(1,2)]);
            G = [Nxx(1) 0 Nxx(2) 0 Nxx(3) 0 Nxx(4) 0;
                Nyy(1) 0 Nyy(2) 0 Nyy(3) 0 Nyy(4) 0;
                0 Nxx(1) 0 Nxx(2) 0 Nxx(3) 0 Nxx(4);
                0 Nyy(1) 0 Nyy(2) 0 Nyy(3) 0 Nyy(4)];
            B = A*G;
            Kq = Kq + B'*Em*B*dJ;
            Bg(:,:,gg) = B;
        end
        edofs = [2*i-1,2*i,2*(i+1)-1,2*(i+1),2*j-1,2*j,2*(j+1)-1,2*(j+1)];
        K(edofs,edofs) = K(edofs,edofs)+Kq;
    end
end

% Boundary conditions
ixfix = [1:nx+1]; % position of the fixed nodes in the node grid
iyfix = 1;
ifix = (iyfix-1)*(nx+1)+ixfix;
fix_dofs = [2*(ifix)-1 2*(ifix)]; % both u and v are constrained here

% Loads
f = zeros(2*N,1);
q = -0.1; % this is the distributed load at the top surface in [N/m]
ixload = [1:nx+1]; % position of the loaded nodes in the node grid
iyload = (ny+1);
iload = (iyload-1)*(nx+1)+ixload;
load_dofs = 2*(iload); % we are loading in the y direction
xload = [xn(iyload,1) xn(iyload,ixload) xn(iyload,end)];
f(load_dofs) = q*0.5*(xload(3:end)-xload(1:end-2));

% Solution
free_dofs = setdiff([1:2*N],[fix_dofs]);
K_free=K(free_dofs,free_dofs);
revised_dofs = setdiff([free_dofs],find(all(K_free == 0,1)));
K_free(all(K_free == 0,2),:) = [];
K_free(:,all(K_free == 0,1)) = [];
u = zeros(2*N,1); 
u(revised_dofs) = K_free\f(revised_dofs);

% Plot results
figure(1)
hold on; grid on; grid minor
title('Nodes','fontsize',15)
plot(xn(iyfix,ixfix),yn(iyfix,ixfix),'rs','Markersize',6)
plot(xn(iyload,ixload),yn(iyload,ixload),'gv','MarkerEdgeColor',[0,0.7,0],'Markersize',6)
plot(xn,yn,'ko','Markersize',3)
legend('fixed nodes','loaded nodes','all nodes','Location','NorthEastOutside')
axis equal;

%%%
figure(2)
title('Displacements','fontsize',15)
hold on; grid on; grid minor
grey = 0.6*[1 1 1]; % light grey as the color for the undeformed structure

for ey = 1:ny
    for ex = 1:nx
        x1 = xn(ey,ex); x2 = xn(ey,ex+1); x3 = x1; x4 = x2;
        y1 = yn(ey,ex); y2 = y1; y3 = yn(ey+1,ex); y4 = y3;
        i = (ey-1)*(nx+1)+ex;
        j = i+nx+1;

        % Skip if any node in the element is NaN
        % if any(isnan([x1, x2, x3, x4, y1, y2, y3, y4]))
        %     continue
        % end

        u1 = u(2*i-1,1); v1 = u(2*i,1);
        u2 = u(2*(i+1)-1,1); v2 = u(2*(i+1),1);
        u3 = u(2*j-1,1); v3 = u(2*j,1);
        u4 = u(2*(j+1)-1,1); v4 = u(2*(j+1),1);
        plot([x1,x2],[y1,y2],'k-o','Color',grey,'MarkerSize',nms,'markerfacecolor',grey)
        plot([x1,x3],[y1,y3],'k-o','Color',grey,'MarkerSize',nms,'markerfacecolor',grey)
        plot([x2,x4],[y2,y4],'k-o','Color',grey,'MarkerSize',nms,'markerfacecolor',grey)
        plot([x3,x4],[y3,y4],'k-o','Color',grey,'MarkerSize',nms,'markerfacecolor',grey)
        plot([x1+u1,x2+u2],[y1+v1,y2+v2],'b-o','MarkerSize',nms,'markerfacecolor','b')
        plot([x1+u1,x3+u3],[y1+v1,y3+v3],'b-o','MarkerSize',nms,'markerfacecolor','b')
        plot([x2+u2,x4+u4],[y2+v2,y4+v4],'b-o','MarkerSize',nms,'markerfacecolor','b')
        plot([x3+u3,x4+u4],[y3+v3,y4+v4],'b-o','MarkerSize',nms,'markerfacecolor','b')
        % average strains and stresses in the element - from their values
        % at the Gauss points
        uv = [u1;v1;u2;v2;u3;v3;u4;v4];
        ev = 0;
        for gg = 1:4
            ev = ev+0.25*Bg(:,:,gg)*uv;
        end
        eev(ey,ex,:) = ev;
        sv(ey,ex,:) = Em*ev;
        xc(ey,ex) = 0.25*(x1+x2+x3+x4);
        yc(ey,ex) = 0.25*(y1+y2+y3+y4);
    end
end
axis equal
for splt = 1:3
figure(10+splt)
contourf(xc,yc,sv(:,:,splt))
colorbar
axis equal
end
for eplt = 1:3
figure(20+eplt)
contourf(xc,yc,eev(:,:,eplt))
colorbar
axis equal
end
