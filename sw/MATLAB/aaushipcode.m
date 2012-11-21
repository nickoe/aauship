%% State space system simulation:
% Rasmus Christensen
% Discrete - Ship Control Simulator - 20/11/2012
% 12gr730

K = 1000;
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

inp_sort = [1 0.5;
            1 -0.5];

A = zeros(5,5,K);
B = zeros(5,2,K);
C = zeros(2,5,K);

betaX = zeros(1,K);
betaW = zeros(1,K);

F = zeros(2,5,K);
N = zeros(2,2,K);

rot = zeros(2,2,K);
rot(:,:,1) = eye(2);
x = zeros(5,K);
y = zeros(2,K);
u = zeros(2,K);
u(:,1) = [10;10]; % Cannot start from zero
        
% Generation of reference signals:
r = [ones(1,K);
     zeros(1,0.2*K) 0.1*pi*ones(1,0.02*K) zeros(1,0.36*K) -0.1*pi*ones(1,0.02*K) zeros(1,0.4*K)];
r_boat = zeros(2,K);

for n = 2:K % thrust computation    
         k1 = rho*(D^4)*Kt*abs(u(1))*u(1);
         k2 = rho*(D^4)*Kt*abs(u(2))*u(2);
         k3 = rho*(D^4)*Kt*abs(u(1))*u(1)*l*sin(phi);
         k4 = rho*(D^4)*Kt*abs(u(2))*u(2)*l*sin(phi);   
 betaX(:,n) = abs(x(1,n-1))*Cd*A_h*0.5*rho;
 betaW(:,n) = 1/8*Cd*rho*depth*(rf^4+rr^4)*abs(x(3,n-1));     
      
      % System Matrices are defined below: 
   A(:,:,n) = [1 ts 0 0 0;... % Velocity
               -5.8 0 0 0 0;... % Acceleration
               0 0 1 ts ((ts^2)/2);... % Angle
               0 0 0 1 ts;... % Angular Velocity
               0 0 0 -1.7326 0]; % Angular Acceleration

   B(:,:,n) = [0 0;...
               10/m 10/m;... % acceleration input, sum of propellers
               0 0;...
               0 0;...
               0.609/I -0.609/I]; % angular acceleration input, difference between them

   C(:,:,n) = [1 0 0 0 0;... % velocity output
               0 0 1 0 0]; % angle output
           
       % Feedback poles are computed below:
          %Q = diag([1/(20^2) 1/(10^2) 1/((2*pi)^2) 1/(2^2) 1/(2^2)]);
          %R = diag([1/(50^2) 1/(120^2)]);
   F(:,:,n) = lqr(A(:,:,n),B(:,:,n),0.01*C(:,:,n)'*C(:,:,n),eye(2));
          
       % Reference gains are compute below:          
       A_nf =[A(:,:,n) B(:,:,n);C(:,:,n) zeros(2,2)];
       B_nf = [zeros(5,2);eye(2)];
        N_f = A_nf\B_nf;
        Nxf = N_f(1:5,:);
        Nuf = [N_f(6,:);N_f(7,:)];
   N(:,:,n) = Nuf + F(:,:,n)*Nxf;
   
       % Conversion of reference signal to boatframe:
 rot(:,:,n) = [cos(x(3,n)) -sin(x(3,n));sin(x(3,n)) cos(x(3,n))];
r_boat(:,n) = rot(:,:,n)\r(:,n);

       % Update of the system:
     u(:,n) = (inp_sort*(-F(:,:,n)*x(:,n)) + N(:,:,n)*r_boat(:,n)); % Input to the system - check if ts should be in this one.
     x(:,n) = bsxfun(@plus,A(:,:,n)*x(:,n-1),B(:,:,n)*u(:,n)); % Computation of state values
     y(:,n) = C(:,:,n)*x(:,n); % System output!
end

h1 = figure(1);
plot(x')
legend('Velocity','Acceleration','Angle','Angular Velocity','Angular Acceleration')
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

h3 = figure(3);
plot(u')
legend('Engine 1','Engine 2')
title('RPS on engines');
xlabel('Sample [n]');
ylabel('Revolutions [rps]');
grid on
% print(h3,'-depsc2','-painters','eng_in.eps')