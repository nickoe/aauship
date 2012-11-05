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
m = 12; % Mass of the ship
I = 30;

k1 = 15; % Revolution 1 to force
k2 = 15; % Revolution 2 to force
k3 = 10; % Revolution 1 to torque
k4 = 10; % Revoltuion 2 to torque

% For simulation purposes the below can be used as a reference, this system
% will have a big drag in sway and heave direction, whilst the one in the
% forward direction is low. 
alphaV = 6;
alphaW = 0.4;

% Variances of the measurement instruments:
varPOS = 0.2;
varVEL = 0.001;
varACC = 0.03;

%% Generation of Simulation Data:
% The below generates a function where the ship applies equal revolutions to the
% ship for the first 500 samples, then increases revolutions on one
% propeller, and then back again. 
n1 = [6*ones(1,0.5*N) 2*ones(1,0.5*N)]'; % Engine one is set to constantly apply 500 revolutions.
n2 = [6*ones(1,0.5*N) 2*ones(1,0.5*N)]'; % Engine two applies 500 revolutions, then changes to 700 then back to 500 again. 
U = [n1 n2]';

%% Kalman Filtering

% The observation matrix adds noise to the measurements. 
% X(n) = A(n) * Y(n) + W(n), where A(n) is defined as:
An = [1 0 0;...
      0 1 0;...
      0 0 1]; % The identity function, as we measure all the constants directly.

% The W(n) term is the noise in the sensors. This is assumed to be white
% gaussian uncorrelated noise. The noise is given as the following:
Wn = zeros(3,N);
Wn(:,1) = [randn(1,1) randn(1,1) randn(1,1)]'.*[sqrt(varPOS) sqrt(varVEL) sqrt(varACC)]'; % Initiation of the system.

% The system model is now defined as:
% Y(n) = H(n)*Y(n) + Z(n), where H(n) is defined as:
Hn = [1 ts ts^2/2;...
      0 1 ts;...
      0 -alphaV 0];
  
% The Z(n) term is in this case not added noise, but the development of the
% system, hence the Z(n) term will be equal to our input, which we define:
% Z(n) = B*U(n) which gives:
Bl = [0 0;...
      0 0;...
      k1/m k1/m];
 
for ii = 1:N
    Zn(:,ii) = Bl*U(:,ii); % Generation of the input stream to the system. 
end



%% Kalman Filtering
% Initiation of the Kalman filter - the ship is assumed to start at [0,0]
Ypred = zeros(3,N); % Prediction of Y
Xpred = zeros(3,N); % Prediction of X
Rpred = zeros(3,3,N); % Prediction of R
B = zeros(3,3,N); % Kalman filter gain B

Yupdate = zeros(3,N); % Update step of Y
Rupdate = zeros(3,3,N); % Update step of R

X = zeros(3,N);
Y = zeros(3,N);

% Covariance matrix of Z(n)
% The Covariance matrix is given as:
  
% Covariance matrix W(n)         

% The above represents the measurement accuracy of the different sensors
% mounted on the ship. If this is very high, the Kalman estimator will not
% be as good at estimating - and the filtered version of the signal, will
% look like its influenced by a lot of noise, which makes sense, as the
% signal is varying a lot!

% 0 0 0 randn(1,1) 0 0 0 randn(1,1)
% randn(1,1)*sqrt(varPOS) randn(1,1)*sqrt(varVEL)
for n = 2:1:N
            Wn(:,n) = [randn(1,1) randn(1,1) randn(1,1)]'.*[sqrt(varPOS) sqrt(varVEL) sqrt(varACC)]'; % Measuremnet noise (all the sensors are IID uncorrelated).
            %Qw = cov(Wn(:,n-1)*Wn(:,n)');% - mean(Wn(:,n-1)) * mean(Wn(:,n))'; % Covariance matrix of Wn
            Qw = [varPOS 0 0;0 varVEL 0;0 0 varACC];
            Qz = cov(Zn(:,n-1)*Zn(:,n)') - mean(Zn(:,n-1)) * mean(Zn(:,n))';% Covariance matrix of Zn
        Y(:,n) = Hn*Y(:,n-1)+Zn(:,n);
        X(:,n) = An*Y(:,n)+Wn(:,n);
    Ypred(:,n) = Hn*Yupdate(:,n-1);
    Xpred(:,n) = An*Ypred(:,n);
  Rpred(:,:,n) = Hn*Rupdate(:,:,n-1)*Hn'+Qz;
      B(:,:,n) = (Rpred(:,:,n)*An')/(An*Rpred(:,:,n)*An'+Qw);
  Yupdate(:,n) = Ypred(:,n)+B(:,:,n)*(X(:,n)-Xpred(:,n));
%Rupdate(:,:,n) = (eye(3)-B(:,:,n)*An)*Rpred(:,:,n);
Rupdate(:,:,n) = (eye(3) - B(:,:,n)*An)*Rpred(:,:,n)*(eye(3) - B(:,:,n)*An)'+(B(:,:,n)*Qw*B(:,:,n)'); % Joseph Form
end

h1 = figure(1);
Y_kal_posX = Yupdate(1,:)'; % Updated Y - x position
Y_kal_velX = Yupdate(2,:)'; % Updated Y - x velocity
Y_kal_accX = Yupdate(3,:)'; % Updated Y - x acceleration

X_posX = X(1,:)'; % Observation X - x position
X_velX = X(2,:)'; % Observation X - x velocity
X_accX = X(3,:)'; % Observation X - x acceleration

Y_posX = Y(1,:)'; % True Y - x position
Y_velX = Y(2,:)'; % True Y - x velocity
Y_accX = Y(3,:)'; % True Y - x acceleration

% Figure plot of the velocity
h1 = figure(1);
hold on
plot(X_posX,'g+','MarkerSize',2);
plot(Y_kal_posX,'b','LineWidth',1);
plot(Y_posX,'m','LineWidth',1);
hold off
title('Position')
legend('Observed Position','Filtered Position','True Position')
xlabel('Sample [n]');ylabel('Position [m]');
grid on

% Figure plot of the angular velocity
h2 = figure(2);
hold on
plot(X_velX,'g+','MarkerSize',2);
plot(Y_kal_velX,'b','LineWidth',1);
plot(Y_velX,'m','LineWidth',1);
hold off
title('Velocity')
legend('Observed Velocity','Filtered Velocity','True Velocity')
xlabel('Sample [n]');ylabel('Velocity [m/s]');
grid on

% Figure plot of the angle
h3 = figure(3);
hold on
plot(X_accX,'g+','MarkerSize',2);
plot(Y_kal_accX,'b','LineWidth',1);
plot(Y_accX,'m','LineWidth',1);
hold off
title('Acceleration')
legend('Observed Acceleration','Filtered Acceleration','True Acceleration')
xlabel('Sample [n]');ylabel('Acceleration [m^2/s]');
grid on

