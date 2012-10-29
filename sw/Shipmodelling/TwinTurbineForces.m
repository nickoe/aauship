clc
clear

nl = 15;        % Rotation of left motor - Revolutions pr s
nr = 14;        % Rotation of right motor - Revolutions pr s

theta_H = 0;    % Heading. 0 = straight north.
v = [0;0];      % speed;
pos = [0;0];    % Position
omega = 0;      % Angular velocity

rho = 1025;     % Water density
Cd = 0.3;       % Drag Coefficient
A = [1;10];     % Area in x direction
Mvessel = 20;   % Weight of vessel
Ivessel = 10;   % Inertia of vessel
D = 0.05;       % Diameter of screw
Kt = 0.5;       % Propeller constant
figure(1)
hold off
plot(pos);
hold on
while(1)
    clc
    l = 20;     % Length from masscenter to applied forces
    theta=pi/16; % Angle from masscenter to applied forces.
    Fwater = [1/2*rho*v(1)^2*Cd*A(1);
             1/2*rho*v(2)^2*Cd*A(2)]; %Resistance from water in X
    
    Fl = rho * D^4 * Kt * abs(nl)*nl; %Force applied from left motor
    Fr = rho * D^4 * Kt * abs(nr)*nr; %Force applied from right motor
    %Fl = 4;
    %Fr = 3;
    %Final forces in long form (outdated):
    Ftl = cos(theta)*Fl;
    Ftr = cos(-theta)*Fr;
    Fxl = cos(theta)*Ftl;
    Fxr = cos(-theta)*Ftr;
    Fx = (Fxr+Fxl);
    Fyl = sin(theta)*Ftl;
    Fyr = sin(-theta)*Ftr;
    Fy = (Fyl+Fyr);
    FRl=sin(-theta)*Fl;
    FRr=sin(theta)*Fr;
    FR=(FRr+FRl);

    %Forces in vector notation:    
    F = [cos(theta)^2;cos(theta)*sin(theta);
        sin(-theta)]*Fl+[cos(-theta)^2;
        cos(-theta)*sin(-theta);sin(theta)]*Fr
    v = v + (F(1:2)-Fwater)/Mvessel
    omega = omega + ((F(3)-(theta_H^2*rho/2))*l/Ivessel);
    theta_H = mod(theta_H + omega,2*pi)
    Rot= [cos(theta_H) sin(theta_H);sin(theta_H) -cos(theta_H)];%Rotation matrix based on heading.
    prevpos = pos;
    pos = pos + Rot*v(1:2)
    ship=[cos(theta_H);sin(theta_H)]*0.05;
    hold on
    plot([pos(1)+ship(1);pos(1)],[pos(2)+ship(2);pos(2)])
    %line(pos',(pos+ship)')
    pause(0.1)
end

omega
