%% Discrete System Simulation - Final;
% Rasmus Christensen 24/11/2012
clc; clear all; clf;

% Simulation Parameters:
ts = 0.01;
K = 100;
betaX = 0.4462;
betaW = 0.0784;
m = 9;
I = (1/12)*m*(0.25*0.25+1.05*1.05);
% The discrete state space model of the system is described below:
% System Dynamics:
A = [-betaX*ts/m 0 0;...
     0 1 ts;...
     0 0 -betaW*ts/I];

% Input Matrix:
B = [ts/m 0;...
     0 0;...
     0 ts/I];
 
% Output Matrix:
C = [1 0 0;...
     0 1 0];
 
poles = eig(A)

sysD = ss(A,B,C,0,ts)

h1 = figure(1);
pzmap(sysD)
% A feedback loop is introduced, setting u = -K*x, this is computed using
% optimal gain. 
Qf = diag([1/3 1/360 1/30]);
Rf = diag([1/1000 1/200]);
F = lqr(sysD,Qf,Rf);

% When a reference signal is introduced, this gives the following equation:
R = [ones(1,K);...
     0*ones(1,K)];
 
% Introducing a reference gain:
A_nf = [sysD.a sysD.b;sysD.c zeros(2,2)];
B_nf = [zeros(3,2);eye(2)];
N_f = inv(A_nf)*B_nf;
Nxf = N_f(1:3,:);
Nuf = N_f(4:5,:);
N = Nuf + F*Nxf


x = zeros(3,K);
u = zeros(2,K);
y = zeros(2,K);

for n = 2:K
   u(:,n) = -F*x(:,n-1) + N*R(:,n);
   x(:,n) = A*x(:,n-1) + B*u(:,n);
   y(:,n) = C*x(:,n);
end
h2 = figure(2)
plot(x')
cl_poles = eig(A-B*F)