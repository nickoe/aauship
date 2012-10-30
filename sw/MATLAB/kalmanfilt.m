%% Simulation of Kalman Filter for Position Measurements (3-dimensional)
% CA1 - 730
% Nick Østergaard, Frederik Juul, Tudor Muresan, Rasmus L. Christensen and
% Attila Fodor

clc, clear all, close all

%Simulation parameters
ts = 0.1; % Samling time
N = 100; % Number of samples

%% Computation of the drag coefficient:

% For simulation purposes the below can be used as a reference, this system
% will have a big drag in sway and heave direction, whilst the one in the
% forward direction is low. 
alphaX = 0.014; % Drag coefficient x-direction
alphaY = 0.9; % Drag coefficient y-direction
alphaZ = 0.9; % Drag coefficient z-direction


% The observation model is used to compute soem derived versions of the
% output. This is done to achieve a better estimate of the filter, as
% further constants are available for measurements. The general expression
% for the obesrvation model is as follows:
% X(n) = A(n) * Y(n) + W(n), where A(n) is defined as:
%  An = [1 ts ts^2/2 0 0 0;... % gps position
%       1 0 0 -1 0 0;... % gps velocity
%       0 1 0 0 -1 0;... % gps acceleration
%       0 1 0 0 1 0;... % vel posiiotn
%       0 1 ts 0 0 0;...% vel velocity
%       0 1 0 0 -1 0;... % vel acceleratoin
%       0 1 0 0 1 0;... % imu position
%       0 0 1 0 0 1;... % imu velocity
%       0 0 1 0 0 0]; % imu acceleration
  
  An = [1 0 0 0 0 0;...
      1 0 0 -1 0 0;...
      0 1 0 0 -1 0;...
      0 1 0 0 1 0;...
      0 1 0 0 0 0;...
      0 1 0 0 -1 0;...
      0 1 0 0 1 0;...
      0 0 1 0 0 1;...
      0 0 1 0 0 0];

% The system model is now defined as:
% Y(n) = H(n)*Y(n) + Z(n)
Hn = [1 ts ts^2/2 0 0 0;...
      0 1 ts 0 0 0;...
      0 -alphaX 0 0 0 0;...
      1 0 0 0 0 0;...
      0 1 0 0 0 0;...
      0 0 1 0 0 0];
    
% Again, the noise is changed at each sample. 

%% Kalman Filtering
% Initiation of the Kalman filter:
Ypred = zeros(6,N); % Prediction of Y
Xpred = zeros(9,N); % Prediction of X
Rpred = zeros(6,6,N); % Prediction of R
B = zeros(6,9,N); % Kalman filter gain B

Yupdate = zeros(6,N); % Update step of Y
Rupdate = zeros(6,6,N); % Update step of R

X = zeros(9,N);
Y = zeros(6,N);

varPOS = 0.2; % The different signal generation variances are defined in this. 
varVEL = 0.3; % They are set to be equal as the variances currently are unknown. 
varACC = 0.2; % 

% These variances are the driving signals, and can be changed to give a
% more accurate estimate of the system. To make these accurate, you would
% have to build a model of the noise the system would experience - rather
% than just generating a normal distribution of numbers. This noise
% represents for instance enviromental parameters (such as waves, wind and
% currents etc.). It can be seen on the plots that the system has trouble
% coping with the variances in the turning phases - which can be enhanced
% by changing the above. But this would result in a lower accuracy on the
% straight lines. 

varW = .1; % The variance of the different measurement instruments.

% Covariance matrix of Z(n)
Qz = [varPOS 0 0 0 0 0;...
      0 varVEL 0 0 0 0;...
      0 0 varACC 0 0 0;...
      0 0 0 0 0 0;...
      0 0 0 0 0 0;...
      0 0 0 0 0 0];
  
% Covariance matrix W(n)
Qw = [1 0 0 0 0 0 0 0 0;...
      0 0 0 0 0 0 0 0 0;...
      0 0 0 0 0 0 0 0 0;...
      0 0 0 0 0 0 0 0 0;...
      0 0 0 0 1 0 0 0 0;...
      0 0 0 0 0 0 0 0 0;...
      0 0 0 0 0 0 0 0 0;...
      0 0 0 0 0 0 0 0 0;...
      0 0 0 0 0 0 0 0 1]*varW;            

% The above represents the measurement accuracy of the different sensors
% mounted on the ship. If this is very high, the Kalman estimator will not
% be as good at estimating - and the filtered version of the signal, will
% look like its influenced by a lot of noise, which makes sense, as the
% signal is varying a lot!

% 0 0 0 randn(1,1) 0 0 0 randn(1,1)
% randn(1,1)*sqrt(varPOS) randn(1,1)*sqrt(varVEL)
for n = 2:1:N
            Zn(:,n) = [zeros(1,2) randn(1,1)*sqrt(varACC) zeros(1,3)]'; % New samples are generated at each time step (inputs to the system).
            Wn(:,n) = [randn(1,1) 0 0 0 randn(1,1) 0 0 0 randn(1,1)]'*sqrt(varW); % Measuremnet noise (all the sensors are IID uncorrelated).
            %Qw = eye(9)*varW; % cov(Wn(n)*Wn(n))
            Qz = cov(Zn*Zn');
        Y(:,n) = Hn*Y(:,n-1)+Zn(:,n);
        X(:,n) = An*Y(:,n)+Wn(:,n);
    Ypred(:,n) = Hn*Yupdate(:,n-1);
    Xpred(:,n) = An*Ypred(:,n);
  Rpred(:,:,n) = Hn*Rupdate(:,:,n-1)*Hn'+Qz;
      B(:,:,n) = (Rpred(:,:,n)*An')*inv(An*Rpred(:,:,n)*An'+Qw);
  Yupdate(:,n) = Ypred(:,n)+B(:,:,n)*(X(:,n)-Xpred(:,n));
Rupdate(:,:,n) = (eye(6)-B(:,:,n)*An)*Rpred(:,:,n);
end

Y_kal_posX = Yupdate(1,:)'; % Filtered Y - x position
Y_kal_velX = Yupdate(2,:)'; % Filtered Y - x velocity
Y_kal_accX = Yupdate(3,:)'; % Filtered Y - x acceleration

X_posX_GPS = X(1,:)'; % Observed position from GPS
X_velX_GPS = X(2,:)'; % Derived position from GPS position
X_accX_GPS = X(3,:)'; % Derived position from GPS position

X_posX_GPSv = X(4,:)'; % Derived position from velocity measurement
X_velX_GPSv = X(5,:)'; % Observed velocity from velocity measurement
X_accX_GPSv = X(6,:)'; % Derived acceleration from velcoity measurement

X_posX_IMU = X(7,:)'; % Derived position from acceleration
X_velX_IMU = X(8,:)'; % Derived velocity from acceleration
X_accX_IMU = X(9,:)'; % Observed acceleration

Y_posX = Y(1,:)'; % True Y - x position
Y_velX = Y(2,:)'; % True Y - x velocity
Y_accX = Y(3,:)'; % True Y - x acceleration

h1 = figure(1);
hold on
plot(X_posX_GPS,'g*')
plot(Y_kal_posX,'b')
plot(Y_posX,'m')
grid on
title('X position')
xlabel('Sample [n]')
ylabel('Distance [m]')
legend('GPS Position Data','Filtered Position Data','True Position')


h2 = figure(2);
hold on
plot(X_velX_GPSv,'g*')
plot(Y_kal_velX,'b')
plot(Y_velX,'m')
grid on
title('X velocity')
xlabel('Sample [n]')
ylabel('Velocity [m/s]')
legend('GPS Velocity Data','Filtered Velocity Data','True Velocity')

h3 = figure(3);
hold on
plot(X_accX_IMU,'g*')
plot(Y_kal_accX,'b')
plot(Y_accX,'m')
grid on
title('X acceleration')
xlabel('Sample [n]')
ylabel('Acceleration [m/s^2]')
legend('IMU Acceleration Data','Filtered Acceleration Data','True Acceleration')