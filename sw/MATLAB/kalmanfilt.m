%% Simulation of Kalman Filter for Position Measurements (3-dimensional)
% CA1 - 730
% Nick Østergaard, Frederik Juul, Tudor Muresan, Rasmus L. Christensen and
% Attila Fodor

clc, clear all, close all
format short
% Simulation parameters
N = 1000; % Number of samples
ts = .01;

%% Computation of system constants used for simulation:

% The mass and inertia of the ship is defined here: 
m = 40; % Mass of the ship
I = 30;

% For simulation purposes the below can be used as a reference, this system
% will have a big drag in sway and heave direction, whilst the one in the
% forward direction is low. 
Cd = 0.3;
rho = 1025;
A_h = 1;
depth = 0.02;
rf = 2;
rr = 1;
D = 0.05;
Kt = 0.5;
l = 20;

% Variances of the measurement instruments:
varPOS = 0.1;
varVEL = 0.01; % Variance of velocity measurements
varACC = 0.8; % variance of acceleration measurements
varANGA = 0.4; % variance of angular acceleration
varANGV = 0.02; % variance of angular velocity
varANG = 0.01; % variance of the angle measurement

varWN = [sqrt(varPOS) sqrt(varVEL) sqrt(varACC) sqrt(varANGA) sqrt(varANGV) sqrt(varANG)]'; % variance vector

%% Generation of Simulation Data:
% The below generates a function where the ship applies equal revolutions to the
% ship for the first 500 samples, then increases revolutions on one
% propeller, and then back again. 
n1 = [100*ones(1,1*N)]'; % Engine one is set to constantly apply 500 revolutions.
n2 = [80*ones(1,1*N)]'; % Engine two applies 500 revolutions, then changes to 700 then back to 500 again. 
U = [n1 n2]';

%% Kalman Filtering

% The observation matrix adds noise to the measurements. 
% X(n) = A(n) * Y(n) + W(n), where A(n) is defined as:
An = eye(6); % The identity function, as we measure all the constants directly.

% The W(n) term is the noise in the sensors. This is assumed to be white
% gaussian uncorrelated noise. The noise is given as the following:
Wn = zeros(6,N);
Wn(:,1) = [randn(1,1) randn(1,1) randn(1,1) randn(1,1) randn(1,1) randn(1,1)]'.*varWN; % Initiation of the system.

% The system model is now defined as:
% Y(n) = H(n)*Y(n) + Z(n), where H(n) is defined as:
% Hn = [1 ts ts^2/2 0 0 0;
%       0 1 ts 0 0 0;...
%       0 -alphaV 0 0 0 0;...
%       0 0 0 0 -alphaW 0;...
%       0 0 0 ts 1 0;...
%       0 0 0 ts^2/2 ts 1];
  
% The Z(n) term is in this case not added noise, but the development of the
% system, hence the Z(n) term will be equal to our input, which we define:
% Z(n) = B*U(n) which gives:

 phi = pi/16;
 
for ii = 1:N
            k1 = rho*(D^4)*Kt*abs(n1(ii));
            k2 = rho*(D^4)*Kt*abs(n2(ii));
            k3 = rho*(D^4)*Kt*abs(n1(ii))*l*sin(phi);
            k4 = rho*(D^4)*Kt*abs(n2(ii))*l*sin(phi);
            Bl = [0 0;
                  0 0;...
                  k1/m k2/m;...
                  k3/I -k4/I;...
                  0 0;
                  0 0];
    Zn(:,ii) = Bl*U(:,ii); % Input stream to the system. 
end



%% Kalman Filtering
% Initiation of the Kalman filter - the ship is assumed to start at [0,0]
Ypred = zeros(6,N); % Prediction of Y
Xpred = zeros(6,N); % Prediction of X
Rpred = zeros(6,6,N); % Prediction of R
B = zeros(6,6,N); % Kalman filter gain B

Yupdate = zeros(6,N); % Update step of Y
Rupdate = zeros(6,6,N); % Update step of R

X = zeros(6,N);
Y = zeros(6,N);

% Covariance matrix of Z(n)
% The Covariance matrix is given as:
  
% Covariance matrix W(n)         

% The above represents the measurement accuracy of the different sensors
% mounted on the ship. If this is very high, the Kalman estimator will not
% be as good at estimating - and the filtered version of the signal, will
% look like its influenced by a lot of noise, which makes sense, as the
% signal is varying a lot!

for n = 2:1:N
     % Simulation parameters are changed, as the system dynamic change at
     % each time step (for nonlinear dynamics).
        alphaV = Y(2,n-1)*Cd*A_h*0.5*rho;
        alphaW = 1/8*Cd*rho*depth*(rf^4+rr^4)*Y(5,n-1);
            Hn = [1 ts ts^2/2 0 0 0;
                  0 1 ts 0 0 0;...
                  0 -alphaV 0 0 0 0;...
                  0 0 0 0 -alphaW 0;...
                  0 0 0 ts 1 0;...
                  0 0 0 ts^2/2 ts 1];
     % Kalman Filter is defined below!
       Wn(:,n) = [randn(1,1) randn(1,1) randn(1,1) randn(1,1) randn(1,1) randn(1,1)]'.*varWN; % Measuremnet noise (all the sensors are IID uncorrelated).
            %Qw = cov(Wn(:,n-1)*Wn(:,n)');% - mean(Wn(:,n-1)) * mean(Wn(:,n))'; % Covariance matrix of Wn
            Qw = diag([sqrt(varPOS) sqrt(varVEL) sqrt(varACC) sqrt(varANGA) sqrt(varANGV) sqrt(varANG)]);
            Qz = cov(Zn(:,n-1)*Zn(:,n)');% Covariance of Zn
        Y(:,n) = Hn*Y(:,n-1)+Zn(:,n);
        X(:,n) = An*Y(:,n)+Wn(:,n);
    Ypred(:,n) = Hn*Yupdate(:,n-1);
    Xpred(:,n) = An*Ypred(:,n);
  Rpred(:,:,n) = Hn*Rupdate(:,:,n-1)*Hn'+Qz;
      B(:,:,n) = (Rpred(:,:,n)*An')/(An*Rpred(:,:,n)*An'+Qw);
  Yupdate(:,n) = Ypred(:,n)+B(:,:,n)*(X(:,n)-Xpred(:,n));
%Rupdate(:,:,n) = (eye(6)-B(:,:,n)*An)*Rpred(:,:,n);
Rupdate(:,:,n) = (eye(6) - B(:,:,n)*An)*Rpred(:,:,n)*(eye(6) - B(:,:,n)*An)'+(B(:,:,n)*Qw*B(:,:,n)'); % Joseph Form
    k_rot(:,n) = [cos(Yupdate(6,n)) sin(Yupdate(6,n))];
 k_newpos(:,n) = Yupdate(1,n).*k_rot(:,n) + (k_rot(:,n).*Yupdate(5,n).*ts);
    y_rot(:,n) = [cos(Y(6,n)) sin(Y(6,n))];
 y_newpos(:,n) = Y(1,n).*y_rot(:,n) + (y_rot(:,n).*Y(5,n).*ts);
    x_rot(:,n) = [cos(X(6,n)) sin(X(6,n))];
 x_newpos(:,n) = X(1,n).*x_rot(:,n) + (x_rot(:,n).*X(5,n).*ts);
end

Y_kal_vel_X = Yupdate(2,:)'; % Updated Y - x position
Y_kal_acc_X = Yupdate(3,:)';
Y_kal_angA_X = Yupdate(4,:)'; 
Y_kal_angV_X = Yupdate(5,:)'; % Updated Y - x velocity
Y_kal_ang_X = Yupdate(6,:)'; % Updated Y - x acceleration

X_vel_X = X(2,:)'; % Observation X - x position
X_acc_X = X(3,:)';
X_angA_X = X(4,:)';
X_angV_X = X(5,:)'; % Observation X - x velocity
X_ang_X = X(6,:)'; % Observation X - x acceleration

Y_vel_X = Y(2,:)'; % True Y - x position
Y_acc_X = Y(3,:)';
Y_angA_X = Y(4,:)'; % True Y - x velocity
Y_angV_X = Y(5,:)';
Y_ang_X = Y(6,:)'; % True Y - x acceleration

% Figure plot of the velocity
h1 = figure(1);
hold on
plot(X_vel_X,'g+','MarkerSize',2);
plot(Y_kal_vel_X,'b','LineWidth',1);
plot(Y_vel_X,'m','LineWidth',1);
hold off
title('Velocity')
legend('Observed','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

% Figure plot of the acceleration
h2 = figure(2);
hold on
plot(X_acc_X,'g+','MarkerSize',2);
plot(Y_kal_acc_X,'b','LineWidth',1);
plot(Y_acc_X,'m','LineWidth',1);
hold off
title('Acceleration')
legend('Observed','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

% Figure plot of the angular acceleration
h3 = figure(3);
hold on
plot(X_angA_X,'g+','MarkerSize',2);
plot(Y_kal_angA_X,'b','LineWidth',1);
plot(Y_angA_X,'m','LineWidth',1);
hold off
title('Angular Acceleration')
legend('Observed','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular Acceleration [degrees/s^2]');
grid on

% Figure plot of the angular velocity
h4 = figure(4);
hold on
plot(X_angV_X,'g+','MarkerSize',2);
plot(Y_kal_angV_X,'b','LineWidth',1);
plot(Y_angV_X,'m','LineWidth',1);
hold off
title('Angular Velocity')
legend('Observed','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular Velocity [degrees/s]');
grid on

% Figure plot of the angle
h5 = figure(5);
hold on
plot(X_ang_X,'g+','MarkerSize',2);
plot(Y_kal_ang_X,'b','LineWidth',1);
plot(Y_ang_X,'m','LineWidth',1);
hold off
title('Angle')
legend('Observed','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angle [degrees]');
grid on

% Rotation 
h6 = figure(6)
hold on
plot(x_newpos(1,:)',x_newpos(2,:)','g+','MarkerSize',2);
plot(k_newpos(1,:)',k_newpos(2,:)','b','LineWidth',1);
plot(y_newpos(1,:)',y_newpos(2,:)','m','LineWidth',1);
hold off
grid on
axis equal