%% Discrete System, take 2!
clc; clear all; clf;
K = 100;

ts = 0.01;
m = 12;
I = (1/12)*m*(0.25*0.25+1.05*1.05);
betaX = 0.4462
betaW = 0.0784


A = [-betaX 0 0;...
     0 0 1;...
     0 0 -betaW];

B = [1/m 0;...
     0 0;...
     0 1/I];

C = [1 0 0;...
     0 1 0];

sys = ss(A,B,C,0);
sysD = c2d(sys,ts)
h5 = figure(5);
pzmap(sysD)
poles = pole(sysD)

Q = diag([1/20 1/1000 1/20]); %1/max velocity^2, 1/max angle^2, 1/max ang. vel.^2
R = diag([1/1000 1/2500]);
F = lqr(sysD,Q,R);
%F = lqr(sysD,90*C'*C,eye(2));

A_nf =[sysD.a sysD.b;sysD.c sysD.d];
B_nf = [zeros(3,2);eye(2)];
N_f = inv(A_nf)*B_nf;
Nxf = N_f(1:3,:);
Nuf = N_f(4:5,:);
N = Nuf + F*Nxf;

rot(:,:,1) = eye(2);

r = [ones(1,K);
     zeros(1,K)];

x = zeros(3,K);
u = zeros(2,K);
y = zeros(2,K);

for n = 2:K
   % Rotation Matrices
    %rot(:,:,n) = [cos(x(2,n-1)) -sin(x(2,n-1));sin(x(2,n-1)) cos(x(2,n-1))];
    %r_boat(:,n) = inv(rot(:,:,n))*r(:,n);
   % System Simulation
   Fx(:,n) = -F*x(:,n-1);
   Nr(:,n) = r(:,n);
Input(:,n) = Fx(:,n)+Nr(:,n);
    u(:,n) = (Fx(:,n) + Nr(:,n));
    x(:,n) = sys.a*x(:,n-1)+sys.b*u(:,n);
    y(:,n) = (sys.c*x(:,n));
end

h1 = figure(1);
plot(x')
legend('Velocity','Angle','Angular Velocity')
grid on

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
hold on
plot(mean(u),'k--')
legend('Engine 1','Engine 2')
title('RPS on engines');
xlabel('Sample [n]');
ylabel('Revolutions [rps]');
grid on
% print(h4,'-depsc2','-painters','eng_in.eps')