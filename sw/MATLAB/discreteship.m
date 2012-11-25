%% Discrete version.
%% State space system simulation:
% Rasmus Christensen
% Discrete - Ship Control Simulator - 20/11/2012
% 12gr730

clc; clear all; close all;

K = 10000;
ts = 0.01;

% System parameters:
Cd = 0.5;
rho = 999.9925;
A_h = 0.5*0.232*0.1;
depth = 0.09;
rf = 0.5;
rr = 0.55;
D = 0.05;
Kt = 0.5;
l = 0.5;


m = 13; % mass of the ship
I = (1/12)*m*(0.25*0.25+1.05*1.05)*2; % inertia of the ship

% System matrices:
% Controller skal køre i bådrammen men mappes over i lokal rammen for at
% sammenholde denne med GPS koordinatet. Så de skal mappes ned i bådrammen!

% HUSK AT n1 + n2 = en fart der giver 1 m/s!

% The control inputs should be mapped down into the boatframe. 

phi = pi/16;

inp_sort = [0.5 0.5;
            0.5 -0.5];

A = zeros(3,3,K);
B = zeros(3,2,K);
C = zeros(2,3,K);

betaX = zeros(1,K);
betaW = zeros(1,K);

F = zeros(2,3,K);
N = zeros(2,2,K);

rot = zeros(2,2,K);
rot(:,:,1) = eye(2);
x = zeros(3,K);
y = zeros(2,K);
u = zeros(2,K);
        
% Generation of reference signals:
r = [ones(1,K);
     zeros(1,K)];% -pi*ones(1,0.02*K) zeros(1,0.36*K) zeros(1,0.4*K)];
r_boat = zeros(2,K);

          A = [-5.8/m 0 0;...
               0 0 1;...
               0 0 -2];

          B = [0.62/m 0.62/m;...
               0 0;...
               0.0305/I -0.0305/I];
           
          C = [1 0 0;...
               0 1 0];
           
        sys = ss(A,B,C,0);
       sysD = c2d(sys,ts)
       
       

for n = 2:K % thrust computation    
         k1 = rho*(D^4)*Kt*abs(u(1));
         k2 = rho*(D^4)*Kt*abs(u(2));
         k3 = rho*(D^4)*Kt*abs(u(1))*l*sin(phi);
         k4 = rho*(D^4)*Kt*abs(u(2))*l*sin(phi);   
 betaX(:,n) = abs(x(1,n-1))*Cd*A_h*0.5*rho;
 betaW(:,n) = 1/8*Cd*rho*depth*(rf^4+rr^4)*abs(x(3,n-1));     
      
      % System Matrices are defined below: 
   A(:,:,n) = sysD.a;

   B(:,:,n) = sysD.b;

   C(:,:,n) = sysD.c;
           
       % Feedback poles are computed below:
          Q = diag([1/25 1/(20*pi) 1/200]); %1/max velocity^2, 1/max angle^2, 1/max ang. vel.^2
          R = diag([1/100 1/100]);
   F(:,:,n) = lqr(sysD,Q,R);
   %F(:,:,n) = lqr(sysD,ts*C(:,:,n)'*C(:,:,n),eye(2));
          
       % Reference gains are compute below:          
       A_nf =[A(:,:,n) B(:,:,n);C(:,:,n) zeros(2,2)];
       B_nf = [zeros(3,2);eye(2)];
        N_f = A_nf\B_nf;
        Nxf = N_f(1:3,:);
        Nuf = N_f(4:5,:);
   N(:,:,n) = Nuf + F(:,:,n)*Nxf;

       % Conversion of reference signal to boatframe:
 rot(:,:,n) = [cos(x(2,n-1)) -sin(x(2,n-1));sin(x(2,n-1)) cos(x(2,n-1))];
r_boat(:,n) = rot(:,:,n)\r(:,n);

       % Update of the system:
     x(:,n) = bsxfun(@plus,(A(:,:,n)-(B(:,:,n)*F(:,:,n)))*x(:,n-1),B(:,:,n)*N(:,:,n)*r(:,n)); % Computation of state values
     u(:,n) = (-(F(:,:,n)*x(:,n-1)) + N(:,:,n)*r(:,n)); % Input to the system - check if ts should be in this one.
     y(:,n) = (C(:,:,n)*x(:,n)); % System output!
end

h1 = figure(1);
plot(x')
legend('Velocity','Angle','Angular Velocity')
grid on
% print(h1,'-depsc2','-painters','mass_plot.eps')

h2 = figure(2);
plot(y')
hold on
legend('Velocity','Angle')
title('System Output y(n)')
plot(r','k--')
grid on
xlabel('Sample [n]');
ylabel('Velocity [m/s] and Angle [rad]');
% print(h2,'-depsc2','-painters','velang.eps')

h4 = figure(4);
plot(u')
legend('Engine 1','Engine 2')
title('RPS on engines');
xlabel('Sample [n]');
ylabel('Revolutions [rps]');
grid on
% print(h4,'-depsc2','-painters','eng_in.eps')