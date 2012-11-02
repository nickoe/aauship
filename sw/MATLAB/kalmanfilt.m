%% Simulation of Kalman Filter for Position Measurements (3-dimensional)
% CA1 - 730
% Nick Østergaard, Frederik Juul, Tudor Muresan, Rasmus L. Christensen and
% Attila Fodor

clc, clear all, close all
format short
% Simulation parameters
N = 1000; % Number of samples

%% Computation of system constants used for simulation:

% The mass and inertia of the ship is defined here: 
m = 12; % Mass of the ship
I = 10;

k1 = 50; % Revolution 1 to force
k2 = 50; % Revolution 2 to force
k3 = 30; % Revolution 1 to torque
k4 = 30; % Revoltuion 2 to torque

% For simulation purposes the below can be used as a reference, this system
% will have a big drag in sway and heave direction, whilst the one in the
% forward direction is low. 
alphaV = 7.5;
alphaW = 0.4;

% Variances of the measurement instruments:
var_w1 = .2;
var_w2 = .1;
var_w3 = .5;

%% Generation of Simulation Data:
% The below generates a function where the ship applies equal revolutions to the
% ship for the first 500 samples, then increases revolutions on one
% propeller, and then back again. 
n1 = 20*ones(1,1000)'; % Engine one is set to constantly apply 500 revolutions.
n2 = [20*ones(1,500) 22*ones(1,200) 20*ones(1,300)]'; % Engine two applies 500 revolutions, then changes to 700 then back to 500 again. 
U = [n1 n2]';

%% Kalman Filtering

% The observation matrix adds noise to the measurements. 
% X(n) = A(n) * Y(n) + W(n), where A(n) is defined as:
An = eye(3); % The identity function, as we measure all the constants directly.

% The W(n) term is the noise in the sensors. This is assumed to be white
% gaussian uncorrelated noise. The noise is given as the following:
Wn = zeros(3,N);
Wn(:,1) = [sqrt(var_w1) sqrt(var_w2) sqrt(var_w3)]'.*randn(1,3)'; % Initiation of the system.

% The system model is now defined as:
% Y(n) = H(n)*Y(n) + Z(n), where H(n) is defined as:
Hn = [-alphaV/m 0 0;...
      0 -alphaW/m 0;...
      0 1 0];
  
% The Z(n) term is in this case not added noise, but the development of the
% system, hence the Z(n) term will be equal to our input, which we define:
% Z(n) = B*U(n) which gives:
Bl = [k1/m k2/m;...
     k3/I -k4/I;...
     0 0];
 
for ii = 1:N
    Zn(:,ii) = Bl*U(:,ii); % Generation of the input terms to the system. 
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
            %Zn = Zn(:,n); % New samples are generated at each time step (inputs to the system).
            Wn(:,n) = [sqrt(var_w1) sqrt(var_w2) sqrt(var_w3)]'.*randn(1,3)'; % Measuremnet noise (all the sensors are IID uncorrelated).
            Qw = cov(Wn(:,n-1)*Wn(:,n)')-mean(Wn(:,n))*mean(Wn(:,n-1))'; % Covariance matrix of Wn
            Qz = cov(Zn(:,n-1)*Zn(:,n)')-mean(Zn(:,n))*mean(Zn(:,n-1))'; % Covariance matrix of Zn
        Y(:,n) = Hn*Y(:,n-1)+Zn(:,n);
        X(:,n) = An*Y(:,n)+Wn(:,n);
    Ypred(:,n) = Hn*Yupdate(:,n-1);
    Xpred(:,n) = An*Ypred(:,n);
  Rpred(:,:,n) = Hn*Rupdate(:,:,n-1)*Hn'+Qz;
      B(:,:,n) = (Rpred(:,:,n)*An')/(An*Rpred(:,:,n)*An'+Qw);
  Yupdate(:,n) = Ypred(:,n)+B(:,:,n)*(X(:,n)-Xpred(:,n));
Rupdate(:,:,n) = (eye(3)-B(:,:,n)*An)*Rpred(:,:,n);
end

h1 = figure(1);
Y_kal_velocX = Yupdate(1,:)'; % Updated Y - x position
Y_kal_omegaX = Yupdate(2,:)'; % Updated Y - x velocity
Y_kal_thetaX = Yupdate(3,:)'; % Updated Y - x acceleration

X_velocX = X(1,:)'; % Observation X - x position
X_omegaX = X(2,:)'; % Observation X - x velocity
X_thetaX = X(3,:)'; % Observation X - x acceleration

Y_velocX = Y(1,:)'; % True Y - x position
Y_omegaX = Y(2,:)'; % True Y - x velocity
Y_thetaX = Y(3,:)'; % True Y - x acceleration

% Figure plot of the velocity
h1 = figure(1);
hold on
plot(X_velocX,'g+','MarkerSize',2);
plot(Y_kal_velocX,'b','LineWidth',1);
plot(Y_velocX,'m','LineWidth',1);
hold off
title('Velocity Plot')
legend('Observed Velocity','Filtered Velocity','True Velocity')
xlabel('Sample [n]');ylabel('Velocity [m/s]');
grid on

% Figure plot of the angular velocity
h2 = figure(2);
hold on
plot(X_omegaX,'g+','MarkerSize',2);
plot(Y_kal_omegaX,'b','LineWidth',1);
plot(Y_omegaX,'m','LineWidth',1);
hold off
title('Angular Velocity Plot')
legend('Observed Angular Velocity','Filtered Angular Velocity','True Angular Velocity')
xlabel('Sample [n]');ylabel('Angular Velocity [degrees/s]');
grid on

% Figure plot of the angle
h3 = figure(3);
hold on
plot(X_thetaX,'g+','MarkerSize',2);
plot(Y_kal_thetaX,'b','LineWidth',1);
plot(Y_thetaX,'m','LineWidth',1);
hold off
title('Angle Plot')
legend('Observed Angle','Filtered Angle','True Angle')
xlabel('Sample [n]');ylabel('Angle [degrees]');
grid on

