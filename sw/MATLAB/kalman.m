%% Kalman Filter Implementation for AAUSHIP1:
% Rasmus Christensen 26/11/2012 - 12gr730 - AAUSHIP Kalaman Filter (c) 
clc; clear all; close all; clear java;
% for lunde = 1:15
%     clf(lunde)
% end
run('contsimu.m');
load inputD.mat; % Loads system input file from contsimu.m
inputD = inputD';
close all;

%load Wn.mat
% To reduce the amount of noise on the measurements which are fed to the
% system, and to enhance the precision of these, the data is run through a
% Kalman filter which is then estiamtes the position, given the noisy
% inputs. The HLI interface, which computes if the waypoint is reached,
% needs the X and Y position for the vessel to verify wether the ship has
% reached the desired waypoints. These two, can be measured by several
% devices, first of, the GPS spits out the position of the vessel, as well
% as the velocity. The velocity can be converted to a Y position, using the
% inverse of the rotation matrix. Using the IMU on board the ship, we're
% able to measure the acceleration in the X and Y direction. The IMU also
% meausres the rotational acceleration around the center of the ship.
%
% Later, this can also be used to estimate the roll of the ship, to give
% the precise position of the measurement taken, using simple geometry!
%
% First of, the state vector Y is defined as:
% Y(n) = A(n) * Y(n-1) + Z(n), where W(n) is driving noise/input to the
% system. 
%
% Then the measuremen vector X can be defined as:
% X(n) = H(n) * Y(n) + W(n), where Z(n) expresses the noisy measurements. 
%
% The desired measurements can be described as (the definition of the A
% matrix):

%% Number of Samples:
ts = 0.1; % Sampling time
N = 1000; % Then it fits with the Simulink Simulation!

%% System Parameters:
m = 12; % The ships mass
I = (1/12)*m*(0.25*0.25+1.05*1.05); % The ships inertia

betaX = 0.4462;
betaY = 0.8;
betaW = 0.0784;
GPS_freq = 10;

%% System Definition:
Hn = [1 ts (ts^2)/2 0 0 0 0 0 0;... % The X position
      0 1 ts 0 0 0 0 0 0;... % The X velocity
      0 -betaX 0 0 0 0 0 0 0;... % The X acceleration is a sum of forward motion (F_forward - F_drag)
      0 0 0 1 ts (ts^2)/2 0 0 0;... % The Y Position
      0 0 0 0 1 ts 0 0 0;... % The Y Velocity
      0 0 0 0 -betaY 0 0 0 0;... % The Y acceleration is a sum of the sideways motion (F_ymotion (wind?) - F_dragY)
      0 0 0 0 0 0 1 ts (ts^2)/2;... % The angle
      0 0 0 0 0 0 0 1 ts;... % The angular velocity
      0 0 0 0 0 0 0 -betaW 0]; % The angular acceleration is a sum of the drag an induced torque!
 
An = eye(9); % An eye matrix, as all the outputs scales equally - everything is in metric units!

%% Noise Terms (Input and Measurement Noise):
% The Z(n) is the "driving noise" - as the system input is a forward force
% and a torque, these are input here as well. The "input" matrix for the
% driving noise Z(n) is then equal to: 
varXpos = 0.979; % m
varXvel = 0.00262; % m/s
varXacc = 4.9451e-5; %  m/s^2 or 5.045*10^-6 G 

varYpos = 1.12; % m
varYvel = 0.0001; % m/s
varYacc = 4.8815e-5; % m/s^2; or 4.9801*10^-6 G

varWpos = 8.23332e-5; % computed from the conversion found in HoneyWell datasheet
varWvel = 2.3559e-5; % rad/s
varWacc = 5;

varYWacc = 2.4496*10^-6; % rad/s^2

SqM = sqrt([varXpos varXvel varXacc varYpos varYvel varYacc varWpos varWvel varWacc]);

Bn = [0 0;...
     0 0;...
     1/m 0;... % From force to input acceleration
     0 0;...
     0 0;...
     0 0;...
     0 0;...
     0 0;...
     0 1/I]; % From torque to angular acceleration

 for ii = 1:N
    Z(:,ii) = Bn*inputD(:,ii);
end

% W is the measurement noise on the system, this can be estimated to be
% white gaussian noise, with zero mean (for most cases) and with a
% variance, that are estimated in Appendix #XX. 
 % Random number at each iteration with a given variance. 

%% Covariance Matrices: 
% As the vector Kalman filter have several system inputs, the noise added
% to the system generates a covariance matrix. These are computed below.
% The covariance of a vector is given as: 
% cov(Z_i(n),Z_j(n)) = E[(Zi-mu_i)(Zj - mu_j)]. If the process is zero
% mean, this becomes a matrix with the diagonal entires given as: 
% cov(Z(n) = E[Z(n)*Z(n)'], but as the inputs to the system, cannot be
% considered to be zero mean, the latter is not used. 
% Qz = cov(Z(n-1)*Z(n)');
% The measuremnets, are considered to be white gaussian zero mean noise,
% and this can then be considered to be a diagonal matrix with the elements
% squared, hence there is no need for the square root, as this just gives
% the variance it self. 

% As the input signals are independent (eg. if a large force is needed,
% that doesn't mean that a large torque is needed, and vice versa), the
% covariance matrix is 

%% System initiation:
% The system is initialized, the parameters are: 
%Wn = zeros(9,N);
Qz = zeros(9,9,N);
Qw = zeros(9,9,N);
Y = zeros(9,N);
X = zeros(9,N);
Ypred = zeros(9,N);
Xpred = zeros(9,N);
Rpred = zeros(9,9,N);
B = zeros(9,9,N);
Yupdate = zeros(9,N);
Rupdate = zeros(9,9,N);
k_newpos = zeros(2,N);
y_newpos = zeros(2,N);
x_newpos = zeros(2,N);
k_rot = zeros(2,2,N);
y_rot = zeros(2,2,N);
x_rot = zeros(2,2,N);

%% Running Computation of the Monorate Kalman filter:
for n = 2:N;
       Wn(:,n) = [randn(4,1);0;randn(4,1)].*SqM';
       Wn([1 4],n) = inv([cos(Y(7,n-1)) -sin(Y(7,n-1));sin(Y(7,n-1)) cos(Y(7,n-1))])*Wn([1 4],n);
       %Wn([2 5],n) = [Y(2,n-1)*cos(Y(7,n-1));Y(2,n-1)*sin(Y(7,n-1))];
       %Wn([3 6],n) = [Y(3,n-1)*cos(Y(7,n-1));Y(6,n-1)*sin(Y(7,n-1))];
     Qz(:,:,n) = diag([0 0 55 0 0 0 0 0 20]); %
   %covari(n,:) = autocorr(Z(:,n));
     %Qw(:,:,n) = bsxfun(@minus,toeplitz(covari(n,:)),Z(:,n).*normpdf(Z(:,n),5.3544,50^2+pi^2));
     Qw(:,:,n) = diag([varXpos varXvel varXacc varYpos varYvel varYacc varWpos varWvel varWacc]);
        Y(:,n) = Hn*Y(:,n-1)+Z(:,n);
        X(:,n) = An*Y(:,n)+Wn(:,n);
    Ypred(:,n) = Hn*Yupdate(:,n-1);
    Xpred(:,n) = An*Ypred(:,n);
  Rpred(:,:,n) = Hn*Rupdate(:,:,n-1)*Hn'+Qz(:,:,n);
      B(:,:,n)       = (Rpred(:,:,n)*An')/(An*Rpred(:,:,n)*An'+Qw(:,:,n));
  Yupdate(:,n) = Ypred(:,n)+B(:,:,n)*(X(:,n)-Xpred(:,n));
Rupdate(:,:,n) = (eye(9)-B(:,:,n)*An)*Rpred(:,:,n);  
     
% Below - rotation udpate, so the route can be plotted:
  k_rot(:,:,n) = [cos(Yupdate(7,n-1)) -sin(Yupdate(7,n-1));sin(Yupdate(7,n-1)) cos(Yupdate(7,n-1))];
 k_newpos(:,n) = k_newpos(:,n-1) + k_rot(:,:,n)*[Yupdate(2,n-1);Yupdate(5,n-1)].*ts; % k_newposD(:,n-1)
  y_rot(:,:,n) = [cos(Y(7,n-1)) -sin(Y(7,n-1));sin(Y(7,n-1)) cos(Y(7,n-1))];
 y_newpos(:,n) = y_newpos(:,n-1) + y_rot(:,:,n)*[Y(2,n-1);Y(5,n-1)].*ts; 
  x_rot(:,:,n) = [cos(X(7,n-1)) -sin(X(7,n-1));sin(X(7,n-1)) cos(X(7,n-1))];
 x_newpos(:,n) = y_newpos(:,n) + y_rot(:,:,n)*[Wn(1,n);Wn(4,n)];% + y_rot(:,:,n)*[X(2,n-1);X(5,n-1)].*ts;
end

%% Output definitions:
% Filtered:
Y_kal_pos_X = Yupdate(1,:)'; % Updated Y - x position
Y_kal_vel_X = Yupdate(2,:)';
Y_kal_acc_X = Yupdate(3,:)'; 

Y_kal_pos_Y = Yupdate(4,:)'; % Updated Y - y position
Y_kal_vel_Y = Yupdate(5,:)';
Y_kal_acc_Y = Yupdate(6,:)'; 

Y_kal_pos_W = Yupdate(7,:)'; % Updated Y - angle
Y_kal_vel_W = Yupdate(8,:)';
Y_kal_acc_W = Yupdate(9,:)'; 

% Measured:
X_pos_X = X(1,:)'; % Observation X - x position
X_vel_X = X(2,:)';
X_acc_X = X(3,:)';

X_pos_Y = X(4,:)'; % Observation X - y position
X_vel_Y = X(5,:)';
X_acc_Y = X(6,:)';

X_pos_W = X(7,:)'; % Observation X - angle
X_vel_W = X(8,:)';
X_acc_W = X(9,:)';

% Actual:
Y_pos_X = Y(1,:)'; % True Y - x position
Y_vel_X = Y(2,:)';
Y_acc_X = Y(3,:)';

Y_pos_Y = Y(4,:)'; % True Y - x position
Y_vel_Y = Y(5,:)';
Y_acc_Y = Y(6,:)';

Y_pos_W = Y(7,:)'; % True Y - x position
Y_vel_W = Y(8,:)';
Y_acc_W = Y(9,:)';

%% Plot of figures for same Monorate sampling:
% Plot of position (x,y,w)
h1 = figure(1);
subplot(3,1,1)
hold on
plot(X_pos_X,'g+','MarkerSize',2);
plot(Y_kal_pos_X,'b','LineWidth',1);
plot(Y_pos_X,'m','LineWidth',1);
hold off
title('X-Position Estimation - Monorate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Position [m]');
grid on

subplot(3,1,2)
hold on
plot(X_pos_Y,'g+','MarkerSize',2);
plot(Y_kal_pos_Y,'b','LineWidth',1);
plot(Y_pos_Y,'m','LineWidth',1);
hold off
title('Y-Position Estimation - Monorate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Position [m]');
grid on

subplot(3,1,3)
hold on
plot(X_pos_W,'g+','MarkerSize',2);
plot(Y_kal_pos_W,'b','LineWidth',1);
plot(Y_pos_W,'m','LineWidth',1);
hold off
title('Angle Estimation - Monorate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angle [rad]');
grid on

% Plot of velocity (x,y,w)
h2 = figure(2);
subplot(3,1,1)
hold on
plot(X_vel_X,'g+','MarkerSize',2);
plot(Y_kal_vel_X,'b','LineWidth',1);
plot(Y_vel_X,'m','LineWidth',1);
hold off
title('X-Velocity Estimation')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

subplot(3,1,2)
hold on
plot(X_vel_Y,'g+','MarkerSize',2);
plot(Y_kal_vel_Y,'b','LineWidth',1);
plot(Y_vel_Y,'m','LineWidth',1);
hold off
title('Y-Velocity Estimation')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

subplot(3,1,3)
hold on
plot(X_vel_W,'g+','MarkerSize',2);
plot(Y_kal_vel_W,'b','LineWidth',1);
plot(Y_vel_W,'m','LineWidth',1);
hold off
title('Angular Velocity Estimation')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular velocity [rad/s]');
grid on

% Plot of acceleration (x,y,w)
h3 = figure(3);
subplot(3,1,1)
hold on
plot(X_acc_X,'g+','MarkerSize',2);
plot(Y_kal_acc_X,'b','LineWidth',1);
plot(Y_acc_X,'m','LineWidth',1);
hold off
title('X-Acceleration Estimation')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

subplot(3,1,2)
hold on
plot(X_acc_Y,'g+','MarkerSize',2);
plot(Y_kal_acc_Y,'b','LineWidth',1);
plot(Y_acc_Y,'m','LineWidth',1);
hold off
title('Y-Acceleration Estimation')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

subplot(3,1,3)
hold on
plot(X_acc_W,'g+','MarkerSize',2);
plot(Y_kal_acc_W,'b','LineWidth',1);
plot(Y_acc_W,'m','LineWidth',1);
hold off
title('Angular Acceleration Estimation')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular acceleration [rad/s]');
grid on

% Plot of actual X-Y position
h4 = figure(4);
hold on
plot(x_newpos(1,:),x_newpos(2,:),'g+','MarkerSize',2);
plot(k_newpos(1,:),k_newpos(2,:),'b','LineWidth',1);
plot(y_newpos(1,:),y_newpos(2,:),'m','LineWidth',1);
hold off
title('XY Position - Monorate')
legend('Measured','Filtered','True')
xlabel('Position [m]')
ylabel('Position [m]')
grid on

%% Running Computation of the Multirate Kalman filter (Negating the GPS input when no new sample is present):
% As not all of the measurements are sampled at the same time (some are
% slower, as the GPS for instance) - the samples where no GPS reading is
% available will have to increase the level of the noise. Below is a list
% of the sampling speeds of the sensors mounted on the ship:
% GPS = 1Hz;
% IMU = 20Hz;
% This calls for attention to the GPS measurements, as these are not
% sampled as often as the IMU! When this is done, the computation of the
% Kalman filter becomes: 

% Resetting the parameters:
YD = zeros(9,N);
XD = zeros(9,N);
YpredD = zeros(9,N);
XpredD = zeros(9,N);
RpredD = zeros(9,9,N);
BD = zeros(9,9,N);
YupdateD = zeros(9,N);
RupdateD = zeros(9,9,N);
k_newposD = zeros(2,N);
y_newposD = zeros(2,N);
x_newposD = zeros(2,N);
k_rotD = zeros(2,2,N);
y_rotD = zeros(2,2,N);
x_rotD = zeros(2,2,N);

sC = 1; % Sample counter - used to only include the 10th GPS sample. 

for n = 2:N;
            %sC = isinteger(n/10) % Sensor Count, used to zero out unsampled system inputs. 
      % Wn(:,n) = randn(9,1).*SqM';
     %Qz(:,:,n) = cov(Z(:,n-1)*Z(:,n)');     
     Qw(:,:,n) = diag([varXpos varXvel varXacc varYpos varYvel varYacc varWpos varWvel varWacc]);
       YD(:,n) = Hn*YD(:,n-1)+Z(:,n);
       XD(:,n) = An*YD(:,n)+Wn(:,n);
   YpredD(:,n) = Hn*YupdateD(:,n-1);
   XpredD(:,n) = An*YpredD(:,n);
 RpredD(:,:,n) = Hn*RupdateD(:,:,n-1)*Hn'+Qz(:,:,n);
     BD(:,:,n) = (RpredD(:,:,n)*An')/(An*RpredD(:,:,n)*An'+Qw(:,:,n));
             if sC == GPS_freq;
                   BD(:,:,n) = BD(:,:,n);
                          sC = 0;
             else                
                   BD(:,1,n) = zeros(9,1);
                   BD(:,4,n) = zeros(9,1);
             end
 YupdateD(:,n) = YpredD(:,n)+BD(:,:,n)*(XD(:,n)-XpredD(:,n));
RupdateD(:,:,n) = (eye(9)-BD(:,:,n)*An)*RpredD(:,:,n);
            sC = sC + 1;
% Below - rotation udpate, so the route can be plotted:
  k_rotD(:,:,n) = [cos(YupdateD(7,n-1)) -sin(YupdateD(7,n-1));sin(YupdateD(7,n-1)) cos(YupdateD(7,n-1))];
 k_newposD(:,n) = k_newposD(:,n-1) + k_rotD(:,:,n)*[YupdateD(2,n-1);YupdateD(5,n-1)].*ts; % k_newposD(:,n-1)
  y_rotD(:,:,n) = [cos(YD(7,n-1)) -sin(YD(7,n-1));sin(YD(7,n-1)) cos(YD(7,n-1))];
 y_newposD(:,n) = y_newposD(:,n-1) + y_rotD(:,:,n)*[YD(2,n-1);YD(5,n-1)].*ts; 
  x_rotD(:,:,n) = [cos(XD(7,n-1)) -sin(XD(7,n-1));sin(XD(7,n-1)) cos(XD(7,n-1))];
 x_newposD(:,n) = y_newposD(:,n) + y_rotD(:,:,n)*[Wn(1,n);Wn(4,n)];
end

%% Output definitions - Multirate sampling:
% Filtered:
Y_kal_pos_XD = YupdateD(1,:)'; % Updated Y - x position
Y_kal_vel_XD = YupdateD(2,:)';
Y_kal_acc_XD = YupdateD(3,:)'; 

Y_kal_pos_YD = YupdateD(4,:)'; % Updated Y - y position
Y_kal_vel_YD = YupdateD(5,:)';
Y_kal_acc_YD = YupdateD(6,:)'; 

Y_kal_pos_WD = YupdateD(7,:)'; % Updated Y - angle
Y_kal_vel_WD = YupdateD(8,:)';
Y_kal_acc_WD = YupdateD(9,:)'; 

% Measured:
X_pos_XD = XD(1,:)'; % Observation X - x position
X_vel_XD = XD(2,:)';
X_acc_XD = XD(3,:)';

X_pos_YD = XD(4,:)'; % Observation X - y position
X_vel_YD = XD(5,:)';
X_acc_YD = XD(6,:)';

X_pos_WD = XD(7,:)'; % Observation X - angle
X_vel_WD = XD(8,:)';
X_acc_WD = XD(9,:)';

% Actual:
Y_pos_XD = YD(1,:)'; % True Y - x position
Y_vel_XD = YD(2,:)';
Y_acc_XD = YD(3,:)';

Y_pos_YD = YD(4,:)'; % True Y - x position
Y_vel_YD = YD(5,:)';
Y_acc_YD = YD(6,:)';

Y_pos_WD = YD(7,:)'; % True Y - x position
Y_vel_WD = YD(8,:)';
Y_acc_WD = YD(9,:)';

%% Plot - Multirate Sampling (x,y,w)
h5 = figure(5);
subplot(3,1,1)
hold on
plot(X_pos_XD,'g+','MarkerSize',2);
plot(Y_kal_pos_XD,'b','LineWidth',1);
plot(Y_pos_XD,'m','LineWidth',1);
hold off
title('X-Position Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Position [m]');
grid on

subplot(3,1,2)
hold on
plot(X_pos_YD,'g+','MarkerSize',2);
plot(Y_kal_pos_YD,'b','LineWidth',1);
plot(Y_pos_YD,'m','LineWidth',1);
hold off
title('Y-Position Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Position [m]');
grid on

subplot(3,1,3)
hold on
plot(X_pos_WD,'g+','MarkerSize',2);
plot(Y_kal_pos_WD,'b','LineWidth',1);
plot(Y_pos_WD,'m','LineWidth',1);
hold off
title('Angle Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angle [rad]');
grid on

% Plot of velocity (x,y,w)
h6 = figure(6);
subplot(3,1,1)
hold on
plot(X_vel_XD,'g+','MarkerSize',2);
plot(Y_kal_vel_XD,'b','LineWidth',1);
plot(Y_vel_XD,'m','LineWidth',1);
hold off
title('X-Velocity Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

subplot(3,1,2)
hold on
plot(X_vel_YD,'g+','MarkerSize',2);
plot(Y_kal_vel_YD,'b','LineWidth',1);
plot(Y_vel_YD,'m','LineWidth',1);
hold off
title('Y-Velocity Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

subplot(3,1,3)
hold on
plot(X_vel_WD,'g+','MarkerSize',2);
plot(Y_kal_vel_WD,'b','LineWidth',1);
plot(Y_vel_WD,'m','LineWidth',1);
hold off
title('Angular Velocity Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular velocity [rad/s]');
grid on

% Plot of acceleration (x,y,w)
h7 = figure(7);
subplot(3,1,1)
hold on
plot(X_acc_XD,'g+','MarkerSize',2);
plot(Y_kal_acc_XD,'b','LineWidth',1);
plot(Y_acc_XD,'m','LineWidth',1);
hold off
title('X-Acceleration Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

subplot(3,1,2)
hold on
plot(X_acc_YD,'g+','MarkerSize',2);
plot(Y_kal_acc_YD,'b','LineWidth',1);
plot(Y_acc_YD,'m','LineWidth',1);
hold off
title('Y-Acceleration Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

subplot(3,1,3)
hold on
plot(X_acc_WD,'g+','MarkerSize',2);
plot(Y_kal_acc_WD,'b','LineWidth',1);
plot(Y_acc_WD,'m','LineWidth',1);
hold off
title('Angular Acceleration Estimation - Multirate')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular acceleration [rad/s]');
grid on

% Plot of actual X-Y position
h8 = figure(8);
hold on
plot(x_newposD(1,:),x_newposD(2,:),'g+','MarkerSize',2);
plot(k_newposD(1,:),k_newposD(2,:),'b','LineWidth',1);
plot(y_newposD(1,:),y_newposD(2,:),'m','LineWidth',1);
hold off
title('XY Position - Multirate (No input correlation)')
legend('Measured','Filtered','True')
xlabel('Position [m]')
ylabel('Position [m]')
grid on

%% Running Computation of the Multirate Kalman filter (Using previous GPS input when no new sample is present):

% As not all of the measurements are sampled at the same time (some are
% slower, as the GPS for instance) - the samples where no GPS reading is
% available will have to increase the level of the noise. Below is a list
% of the sampling speeds of the sensors mounted on the ship:
% GPS = 1Hz;
% IMU = 20Hz;
% This calls for attention to the GPS measurements, as these are not
% sampled as often as the IMU! When this is done, the computation of the
% Kalman filter becomes: 

% Resetting the parameters:
YK = zeros(9,N);
XK = zeros(9,N);
YpredK = zeros(9,N);
XpredK = zeros(9,N);
RpredK = zeros(9,9,N);
BK = zeros(9,9,N);
YupdateK = zeros(9,N);
RupdateK = zeros(9,9,N);
k_newposK = zeros(2,N);
y_newposK = zeros(2,N);
x_newposK = zeros(2,N);
k_rotK = zeros(2,2,N);
y_rotK = zeros(2,2,N);
x_rotK = zeros(2,2,N);

sK = 1; % Sample counter - used to only include the 10th GPS sample. 

for n = 2:N;
      % Wn(:,n) = randn(9,1).*SqM';
     %Qz(:,:,n) = cov(Z(:,n-1)*Z(:,n)');     
     Qw(:,:,n) = diag([varXpos varXvel varXacc varYpos varYvel varYacc varWpos varWvel varWacc]);
       YK(:,n) = Hn*YK(:,n-1)+Z(:,n);
       XK(:,n) = An*YK(:,n)+Wn(:,n);
             if sK == GPS_freq;
                 XK(1,n) = XK(1,n);
                 XK(4,n) = XK(4,n);
                      sK = 0;
             else
                 XK(1,n) = XK(1,n-1);
                 XK(4,n) = XK(4,n-1);
             end
   YpredK(:,n) = Hn*YupdateK(:,n-1);
   XpredK(:,n) = An*YpredK(:,n);
 RpredK(:,:,n) = Hn*RupdateK(:,:,n-1)*Hn'+Qz(:,:,n);
     BK(:,:,n) = (RpredK(:,:,n)*An')/(An*RpredK(:,:,n)*An'+Qw(:,:,n));
%              if sK == GPS_freq; % GPS_freq is the slow frequency of the GPS
%                    BK(:,1,n) = BK(:,1,n);
%                    BK(:,4,n) = BK(:,4,n);
%                           sK = 0;
%              else
%                    BK(:,1,n) = BK(:,1,n-1);
%                    BK(:,4,n) = BK(:,4,n-1);
%              end
 YupdateK(:,n) = YpredK(:,n)+BK(:,:,n)*(XK(:,n)-XpredK(:,n));
RupdateK(:,:,n) = (eye(9)-BK(:,:,n)*An)*RpredK(:,:,n);
            sK = sK + 1;
% Below - rotation udpate, so the route can be plotted:
  k_rotK(:,:,n) = [cos(YupdateK(7,n-1)) -sin(YupdateK(7,n-1));sin(YupdateK(7,n-1)) cos(YupdateK(7,n-1))];
 k_newposK(:,n) = k_newposK(:,n-1) + k_rotK(:,:,n)*[YupdateK(2,n-1);YupdateK(5,n-1)].*ts; % k_newposD(:,n-1)
  y_rotK(:,:,n) = [cos(YK(7,n-1)) -sin(YK(7,n-1));sin(YK(7,n-1)) cos(YK(7,n-1))];
 y_newposK(:,n) = y_newposK(:,n-1) + y_rotK(:,:,n)*[YK(2,n-1);YK(5,n-1)].*ts; 
  x_rotK(:,:,n) = [cos(XK(7,n-1)) -sin(XK(7,n-1));sin(XK(7,n-1)) cos(XK(7,n-1))];
 x_newposK(:,n) = y_newposK(:,n) + y_rotK(:,:,n)*[Wn(1,n);Wn(4,n)];
end

%% Output definintions - Multirate (Only changing at the new update steps!).
Y_kal_pos_XK = YupdateK(1,:)'; % Updated Y - x position
Y_kal_vel_XK = YupdateK(2,:)';
Y_kal_acc_XK = YupdateK(3,:)'; 

Y_kal_pos_YK = YupdateK(4,:)'; % Updated Y - y position
Y_kal_vel_YK = YupdateK(5,:)';
Y_kal_acc_YK = YupdateK(6,:)'; 

Y_kal_pos_WK = YupdateK(7,:)'; % Updated Y - angle
Y_kal_vel_WK = YupdateK(8,:)';
Y_kal_acc_WK = YupdateK(9,:)'; 

% Measured:
X_pos_XK = XK(1,:)'; % Observation X - x position
X_vel_XK = XK(2,:)';
X_acc_XK = XK(3,:)';

X_pos_YK = XK(4,:)'; % Observation X - y position
X_vel_YK = XK(5,:)';
X_acc_YK = XK(6,:)';

X_pos_WK = XK(7,:)'; % Observation X - angle
X_vel_WK = XK(8,:)';
X_acc_WK = XK(9,:)';

% Actual:
Y_pos_XK = YK(1,:)'; % True Y - x position
Y_vel_XK = YK(2,:)';
Y_acc_XK = YK(3,:)';

Y_pos_YK = YK(4,:)'; % True Y - x position
Y_vel_YK = YK(5,:)';
Y_acc_YK = YK(6,:)';

Y_pos_WK = YK(7,:)'; % True Y - x position
Y_vel_WK = YK(8,:)';
Y_acc_WK = YK(9,:)';

%% Plot - Multirate Sampling (Using same samplings input as last time). 
h9 = figure(9);
subplot(3,1,1)
hold on
plot(X_pos_XK,'g+','MarkerSize',2);
plot(Y_kal_pos_XK,'b','LineWidth',1);
plot(Y_pos_XK,'m','LineWidth',1);
hold off
title('X-Position Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Position [m]');
grid on

subplot(3,1,2)
hold on
plot(X_pos_YK,'g+','MarkerSize',2);
plot(Y_kal_pos_YK,'b','LineWidth',1);
plot(Y_pos_YK,'m','LineWidth',1);
hold off
title('Y-Position Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Position [m]');
grid on

subplot(3,1,3)
hold on
plot(X_pos_WK,'g+','MarkerSize',2);
plot(Y_kal_pos_WK,'b','LineWidth',1);
plot(Y_pos_WK,'m','LineWidth',1);
hold off
title('Angle Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angle [rad]');
grid on

% Plot of velocity (x,y,w)
h10 = figure(10);
subplot(3,1,1)
hold on
plot(X_vel_XK,'g+','MarkerSize',2);
plot(Y_kal_vel_XK,'b','LineWidth',1);
plot(Y_vel_XK,'m','LineWidth',1);
hold off
title('X-Velocity Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

subplot(3,1,2)
hold on
plot(X_vel_YK,'g+','MarkerSize',2);
plot(Y_kal_vel_YK,'b','LineWidth',1);
plot(Y_vel_YK,'m','LineWidth',1);
hold off
title('Y-Velocity Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

subplot(3,1,3)
hold on
plot(X_vel_WK,'g+','MarkerSize',2);
plot(Y_kal_vel_WK,'b','LineWidth',1);
plot(Y_vel_WK,'m','LineWidth',1);
hold off
title('Angular Velocity Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular velocity [rad/s]');
grid on

% Plot of acceleration (x,y,w)
h11 = figure(11);
subplot(3,1,1)
hold on
plot(X_acc_XK,'g+','MarkerSize',2);
plot(Y_kal_acc_XK,'b','LineWidth',1);
plot(Y_acc_XK,'m','LineWidth',1);
hold off
title('X-Acceleration Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

subplot(3,1,2)
hold on
plot(X_acc_YK,'g+','MarkerSize',2);
plot(Y_kal_acc_YK,'b','LineWidth',1);
plot(Y_acc_YK,'m','LineWidth',1);
hold off
title('Y-Acceleration Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

subplot(3,1,3)
hold on
plot(X_acc_WK,'g+','MarkerSize',2);
plot(Y_kal_acc_WK,'b','LineWidth',1);
plot(Y_acc_WK,'m','LineWidth',1);
hold off
title('Angular Acceleration Estimation - Multirate (no input change)')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular acceleration [rad/s]');
grid on

% Plot of actual X-Y position
h12 = figure(12);
hold on
plot(x_newposK(1,:),x_newposK(2,:),'g+','MarkerSize',2);
plot(k_newposK(1,:),k_newposK(2,:),'b','LineWidth',1);
plot(y_newposK(1,:),y_newposK(2,:),'m','LineWidth',1);
hold off
title('XY Position - Multirate (Input correlation)')
legend('Measured','Filtered','True')
xlabel('Position [m]')
ylabel('Position [m]')
grid on

%% Kalman Filtering with Lost Packages:
% The Kalman gain is used to see if a packet is lost during the
% transmission, and if one is lost / corrupted, the gain should be set to
% zero, as this will make the system rely on estimates. 
% Resetting the parameters:
YL = zeros(9,N);
XL = zeros(9,N);
YpredL = zeros(9,N);
XpredL = zeros(9,N);
RpredL = zeros(9,9,N);
BL = zeros(9,9,N);
YupdateL = zeros(9,N);
RupdateL = zeros(9,9,N);
k_newposL = zeros(2,N);
y_newposL = zeros(2,N);
x_newposL = zeros(2,N);
k_rotL = zeros(2,2,N);
y_rotL = zeros(2,2,N);
x_rotL = zeros(2,2,N);
packLost = zeros(9,N);

sL = 1;

for n = 2:N;
            %sC = isinteger(n/10) % Sensor Count, used to zero out unsampled system inputs. 
      % Wn(:,n) = randn(9,1).*SqM';
     %Qz(:,:,n) = cov(Z(:,n-1)*Z(:,n)');     
     Qw(:,:,n) = diag([varXpos varXvel varXacc varYpos varYvel varYacc varWpos varWvel varWacc]);
       YL(:,n) = Hn*YL(:,n-1)+Z(:,n);
       XL(:,n) = An*YL(:,n)+Wn(:,n);
   YpredL(:,n) = Hn*YupdateL(:,n-1);
   XpredL(:,n) = An*YpredL(:,n);
 RpredL(:,:,n) = Hn*RupdateL(:,:,n-1)*Hn'+Qz(:,:,n);
     BL(:,:,n) = (RpredL(:,:,n)*An')/(An*RpredL(:,:,n)*An'+Qw(:,:,n));
 packLost(:,n) = rand(9,1)<0.5 ; % Looses 10 percent of the packages. 
             if sL == GPS_freq;
                   BL(:,:,n) = BL(:,:,n);
                          sL = 0;
             else                
                   BL(:,1,n) = zeros(9,1);
                   BL(:,4,n) = zeros(9,1);
             end
       packRow = find(packLost(:,n)==0);
BL(:,packRow,n) = zeros(9,numel(packRow));
 YupdateL(:,n) = YpredL(:,n)+BL(:,:,n)*(XL(:,n)-XpredL(:,n));
RupdateL(:,:,n) = (eye(9)-BL(:,:,n)*An)*RpredL(:,:,n);
            sL = sL + 1;
% Below - rotation udpate, so the route can be plotted:
  k_rotL(:,:,n) = [cos(YupdateL(7,n-1)) -sin(YupdateL(7,n-1));sin(YupdateL(7,n-1)) cos(YupdateL(7,n-1))];
 k_newposL(:,n) = k_newposL(:,n-1) + k_rotL(:,:,n)*[YupdateL(2,n-1);YupdateL(5,n-1)].*ts; % k_newposD(:,n-1)
  y_rotL(:,:,n) = [cos(YL(7,n-1)) -sin(YL(7,n-1));sin(YL(7,n-1)) cos(YL(7,n-1))];
 y_newposL(:,n) = y_newposL(:,n-1) + y_rotL(:,:,n)*[YL(2,n-1);YL(5,n-1)].*ts; 
  x_rotL(:,:,n) = [cos(XL(7,n-1)) -sin(XL(7,n-1));sin(XL(7,n-1)) cos(XL(7,n-1))];
 x_newposL(:,n) = y_newposL(:,n) + y_rotL(:,:,n)*[Wn(1,n);Wn(4,n)];
end

%% Output Definitions - Lost Package Scenario
Y_kal_pos_XL = YupdateL(1,:)'; % Updated Y - x position
Y_kal_vel_XL = YupdateL(2,:)';
Y_kal_acc_XL = YupdateL(3,:)'; 

Y_kal_pos_YL = YupdateL(4,:)'; % Updated Y - y position
Y_kal_vel_YL = YupdateL(5,:)';
Y_kal_acc_YL = YupdateL(6,:)'; 

Y_kal_pos_WL = YupdateL(7,:)'; % Updated Y - angle
Y_kal_vel_WL = YupdateL(8,:)';
Y_kal_acc_WL = YupdateL(9,:)'; 

% Measured:
X_pos_XL = XL(1,:)'; % Observation X - x position
X_vel_XL = XL(2,:)';
X_acc_XL = XL(3,:)';

X_pos_YL = XL(4,:)'; % Observation X - y position
X_vel_YL = XL(5,:)';
X_acc_YL = XL(6,:)';

X_pos_WL = XL(7,:)'; % Observation X - angle
X_vel_WL = XL(8,:)';
X_acc_WL = XL(9,:)';

% Actual:
Y_pos_XL = YL(1,:)'; % True Y - x position
Y_vel_XL = YL(2,:)';
Y_acc_XL = YL(3,:)';

Y_pos_YL = YL(4,:)'; % True Y - x position
Y_vel_YL = YL(5,:)';
Y_acc_YL = YL(6,:)';

Y_pos_WL = YL(7,:)'; % True Y - x position
Y_vel_WL = YL(8,:)';
Y_acc_WL = YL(9,:)';

%% Plot of the Lost Package Scenario
h13 = figure(13);
subplot(3,1,1)
hold on
plot(X_pos_XL,'g+','MarkerSize',2);
plot(Y_kal_pos_XL,'b','LineWidth',1);
plot(Y_pos_XL,'m','LineWidth',1);
hold off
title('X-Position Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Position [m]');
grid on

subplot(3,1,2)
hold on
plot(X_pos_YL,'g+','MarkerSize',2);
plot(Y_kal_pos_YL,'b','LineWidth',1);
plot(Y_pos_YL,'m','LineWidth',1);
hold off
title('Y-Position Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Position [m]');
grid on

subplot(3,1,3)
hold on
plot(X_pos_WL,'g+','MarkerSize',2);
plot(Y_kal_pos_WL,'b','LineWidth',1);
plot(Y_pos_WL,'m','LineWidth',1);
hold off
title('Angle Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angle [rad]');
grid on

% Plot of velocity (x,y,w)
h14 = figure(14);
subplot(3,1,1)
hold on
plot(X_vel_XL,'g+','MarkerSize',2);
plot(Y_kal_vel_XL,'b','LineWidth',1);
plot(Y_vel_XL,'m','LineWidth',1);
hold off
title('X-Velocity Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

subplot(3,1,2)
hold on
plot(X_vel_YL,'g+','MarkerSize',2);
plot(Y_kal_vel_YL,'b','LineWidth',1);
plot(Y_vel_YL,'m','LineWidth',1);
hold off
title('Y-Velocity Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on

subplot(3,1,3)
hold on
plot(X_vel_WL,'g+','MarkerSize',2);
plot(Y_kal_vel_WL,'b','LineWidth',1);
plot(Y_vel_WL,'m','LineWidth',1);
hold off
title('Angular Velocity Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular velocity [rad/s]');
grid on

% Plot of acceleration (x,y,w)
h15 = figure(15);
subplot(3,1,1)
hold on
plot(X_acc_XL,'g+','MarkerSize',2);
plot(Y_kal_acc_XL,'b','LineWidth',1);
plot(Y_acc_XL,'m','LineWidth',1);
hold off
title('X-Acceleration Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

subplot(3,1,2)
hold on
plot(X_acc_YL,'g+','MarkerSize',2);
plot(Y_kal_acc_YL,'b','LineWidth',1);
plot(Y_acc_YL,'m','LineWidth',1);
hold off
title('Y-Acceleration Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on

subplot(3,1,3)
hold on
plot(X_acc_WL,'g+','MarkerSize',2);
plot(Y_kal_acc_WL,'b','LineWidth',1);
plot(Y_acc_WL,'m','LineWidth',1);
hold off
title('Angular Acceleration Estimation - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Sample [n]') ;ylabel('Angular acceleration [rad/s]');
grid on

% Plot of actual X-Y position
h16 = figure(16);
hold on
plot(x_newposL(1,:),x_newposL(2,:),'g+','MarkerSize',2);
plot(k_newposL(1,:),k_newposL(2,:),'b','LineWidth',1);
plot(y_newposL(1,:),y_newposL(2,:),'m','LineWidth',1);
hold off
title('XY Position - Lost Packages')
legend('Measured','Filtered','True')
xlabel('Position [m]')
ylabel('Position [m]')
grid on

%% Calculation differente between Monorate and Multirate
% The difference in X-position:
diffX_pos = Y(1,:)' - Y_kal_pos_X;
diffX_posD = YD(1,:)' - Y_kal_pos_XD;
diffX_posK = YK(1,:)' - Y_kal_pos_XK;
diffX_posL = YL(1,:)' - Y_kal_pos_XL; % Lost packages

% The difference in Y-position:
diffY_pos = Y(4,:)' - Y_kal_pos_Y;
diffY_posD = YD(4,:)' - Y_kal_pos_YD;
diffY_posK = YK(4,:)' - Y_kal_pos_YK;
diffY_posL = YL(4,:)' - Y_kal_pos_YL;

% The difference in W-position:
diffW_pos = Y(7,:)' - Y_kal_pos_W;
diffW_posD = YD(7,:)' - Y_kal_pos_WD;
diffW_posK = YK(7,:)' - Y_kal_pos_WK;
diffW_posL = YL(7,:)' - Y_kal_pos_WL;

% The difference in X-velocity:
diffX_vel = Y(2,:)' - Y_kal_vel_X;
diffX_velD = YD(2,:)' - Y_kal_vel_XD;
diffX_velK = YK(2,:)' - Y_kal_vel_XK;
diffX_velL = YL(2,:)' - Y_kal_vel_XL;

% The difference in Y-velocity:
diffY_vel = Y(5,:)' - Y_kal_vel_Y;
diffY_velD = YD(5,:)' - Y_kal_vel_YD;
diffY_velK = YK(5,:)' - Y_kal_vel_YK;
diffY_velL = YL(5,:)' - Y_kal_vel_YL;

% The difference in W-velocity:
diffW_vel = Y(8,:)' - Y_kal_vel_W;
diffW_velD = YD(8,:)' - Y_kal_vel_WD;
diffW_velK = YK(8,:)' - Y_kal_vel_WK;
diffW_velL = YL(8,:)' - Y_kal_vel_WL;

% The difference in X-acceleration:
diffX_acc = Y(3,:)' - Y_kal_acc_X;
diffX_accD = YD(3,:)' - Y_kal_acc_XD;
diffX_accK = YK(3,:)' - Y_kal_acc_XK;
diffX_accL = YL(3,:)' - Y_kal_acc_XL;

% The difference in Y-acceleration:
diffY_acc = Y(6,:)' - Y_kal_acc_Y;
diffY_accD = YD(6,:)' - Y_kal_acc_YD;
diffY_accK = YK(6,:)' - Y_kal_acc_YK;
diffY_accL = YL(6,:)' - Y_kal_acc_YL;

% The difference in W-acceleration:
diffW_acc = Y(9,:)' - Y_kal_acc_W;
diffW_accD = YD(9,:)' - Y_kal_acc_WD;
diffW_accK = YK(9,:)' - Y_kal_acc_WK;
diffW_accL = YL(9,:)' - Y_kal_acc_WL;

% The difference in absolute position:
diff_pos = y_newpos' - k_newpos';
diff_posD = y_newposD' - k_newposD';
diff_posK = y_newposK' - k_newposK';
diff_posL = y_newposL' - k_newposL';

% Absolute distance between Y and filtered
for jj = 1:N
    diff_abs(jj)  = sqrt(((k_newpos(1,jj) - y_newpos(1,jj))^2)+((k_newpos(2,jj) - y_newpos(2,jj))^2));
    diff_absD(jj) = sqrt(((k_newposD(1,jj) - y_newposD(1,jj))^2)+((k_newposD(2,jj) - y_newposD(2,jj))^2));
    diff_absK(jj) = sqrt(((k_newposK(1,jj) - y_newposK(1,jj))^2)+((k_newposK(2,jj) - y_newposK(2,jj))^2));
    diff_absL(jj) = sqrt(((k_newposL(1,jj) - y_newposL(1,jj))^2)+((k_newposL(2,jj) - y_newposL(2,jj))^2));
end

%% Plot of the error between monorate and multirate:
% Position
h17 = figure(17);
subplot(3,1,1) % X
plot(diffX_pos,'b'); hold on
plot(diffX_posD,'r'); 
plot(diffW_posL,'m');
plot(diffX_posK,'g'); hold off
title('Difference Monorate/Multirate - X-Position')
legend('Monorate','Multirate','Lost Packages','Multirate NI')
grid on
ylabel('Error [m]');
subplot(3,1,2) % Y
plot(diffY_pos,'b'); hold on
plot(diffY_posD,'r'); 
plot(diffY_posD,'m');
plot(diffY_posK,'g'); hold off
title('Difference Monorate/Multirate - Y-Position')
legend('Monorate','Multirate','Lost Packages','Multirate NI')
grid on
ylabel('Error [m]');
subplot(3,1,3) % W
plot(diffW_pos,'b'); hold on
plot(diffW_posD,'r');
plot(diffW_posL,'m');
plot(diffW_posK,'g'); hold off
title('Difference Monorate/Multirate - W-Position')
legend('Monorate','Multirate','Lost Packages','Multirate NI')
grid on
ylabel('Error [m]');
xlabel('Sample [n]');
hold off
grid on

% Velocity
h18 = figure(18);
subplot(3,1,1) % X
plot(diffX_vel,'b'); hold on
plot(diffX_velD,'r'); 
plot(diffX_velL,'m');
plot(diffX_velK,'g'); hold off
title('Difference Monorate/Multirate - X-Velocity')
legend('Monorate','Multirate','Lost Packages','Multirate NI')
grid on
ylabel('Error [m/s]');
subplot(3,1,2) % Y
plot(diffY_vel,'b'); hold on
plot(diffY_velD,'r'); 
plot(diffY_velL,'m');
plot(diffY_velK,'g'); hold off
title('Difference Monorate/Multirate - Y-Velocity')
legend('Monorate','Multirate','Lost Packages','Multirate NI')
grid on
ylabel('Error [m/s]');
subplot(3,1,3) % W
plot(diffW_vel,'b'); hold on
plot(diffW_velD,'r'); 
plot(diffW_velL,'m'); 
plot(diffW_velK,'g'); hold off
title('Difference Monorate/Multirate - W-Velocity')
legend('Monorate','Multirate','Lost Packages','Multirate NI')
ylabel('Error [m/s]');
xlabel('Sample [n]');
hold off
grid on

% Acceleration
h19 = figure(19);
subplot(3,1,1) % X
plot(diffX_accD,'r'); hold on
plot(diffX_acc,'b');
plot(diffX_accL,'m'); 
plot(diffX_accK,'g'); hold off
title('Difference Monorate/Multirate - X-Acceleration')
legend('Multirate','Monorate','Lost Packages','Multirate NI')
grid on
ylabel('Error [m/s^2]');
subplot(3,1,2) % Y
plot(diffY_accD,'r'); hold on
plot(diffY_acc,'b'); 
plot(diffY_accL,'m'); 
plot(diffY_accK,'g'); hold off
title('Difference Monorate/Multirate - Y-Acceleration')
legend('Multirate','Monorate','Lost Packages','Multirate NI')
grid on
ylabel('Error [m/s^2]');
subplot(3,1,3) % W
plot(diffW_accD,'r'); hold on
plot(diffW_acc,'b'); 
plot(diffW_accL,'m');
plot(diffW_accK,'g'); hold off
title('Difference Monorate/Multirate - W-Acceleration')
legend('Multirate','Monorate','Lost Packages','Multirate NI')
ylabel('Error [m/s^2]');
xlabel('Sample [n]');
hold off
grid on

%Absolute position:
h20 = figure(20);
subplot(2,1,1)
plot(diff_pos(:,1),'b'); hold on
plot(diff_posD(:,1),'r');
plot(diff_posL(:,1),'m');
plot(diff_posK(:,1),'g'); hold off
title('Error in X-Position');
legend('Monorate','Multirate','Lost Packages','Multirate NI')
grid on
subplot(2,1,2)
plot(diff_pos(:,2),'b'); hold on
plot(diff_posD(:,2),'r');
plot(diff_posL(:,2),'m');
plot(diff_posK(:,2),'g'); hold off
title('Error in Y-Position');
legend('Monorate','Multirate','Lost Packages','Multirate NI')
grid on

h21 = figure(21);
plot(diff_abs,'b'); hold on
plot(diff_absD,'r');
plot(diff_absL,'m');
plot(diff_absK,'g'); hold off
title('Absolute Position Error');
legend('Monorate','Multirate','Lost Packages','Multirate NI');
xlabel('Sample [n]');
ylabel('Distance [m]');
grid on

%% NOT USED! - Changing the Covariance Matrices and inputs:
% As the inputs to the system is seen to vary a lot, the system is is now
% computed where the inputs are considered a normal distribution of
% numbers, thus giving the following two distributions: 

% Distribution of the force:
% The force can be seen as a normal distribution where the mean can be
% considered to be the force the ship needs to apply to maintain a velocity
% of 1 m/s. Through simulations, this have proven to be 5.3544 Newtons, and
% as this value can increase or decrease from small numbers to large
% % numbers, the variance is set to 50. This gives the following
% % distribution:
% % Force ~ N(5.3544,50^2)
% my_force = 5.3544;
% si_force = 50;
% 
% % Distribution of the torque:
% % The torque can be distributed in the same manner, however the torque is
% % with a zero mean, as the ship normally sails straight ahead. The angle 
% % the ship can turn can be seen as pi degrees to either side, as this gives
% % the value of 
% % This gives the following distribution for the torque function:
% % Torque ~ N(0,pi^2)
% my_torqe = 0;
% si_torqe = pi;
% 
% % As Force and Torque are given in the same vector, the distribution
% % function will be joint, and the probability that both values occur, will
% % be a multiplication of the two probabilities. Thus stating: 
% % P(xa,xb) = P(xa)P(xb). Thus giving the expected value of the input as: 
% % E[P([xa,xb] = vector(K)] = K * P(xa)*P(xb) - which makes way for
% % computing the autocovariance function as:
% % C = E[(X1 - my1)(X2 - my2)] -> E[X1X2] - my1my2
% 
% 
% % These inputs are then insered into a matrix:
% 
% 
% for j = 2:N
%     prop_force = normpdf(Z(3,n),my_force,si_force);
%     prop_torqe = normpdf(Z(9,n),my_torqe,si_torqe);
%     inputP = [zeros(2,N+1);prop_force;zeros(5,N+1);prop_torqe];
%     mean_forc = (mean_forc + Z(3,n))/n;
%     mean_torq = (mean_torq + Z(9,n))/n;
%     covQw = bsxfun(@minus,Z(:,n-1)*Z(:,n)'*(inputP(:,n-1)*inputP(:,n)'),[zeros(2,1);mean_forc;zeros(5,1);mean_torq]);
% end

%% Estiamting a Wind Bias:
% As Wind might push the ship out of course (constantly in the same
% direction) this can be considered a bias to the system. This is then to
% be subtracted, so the system only computes on the actual data, rather
% than the wind-biased data. 

%% Combined Kalman filter with test inputs:
% Below is a simulation of a walk around the parking lot, with the IMU and
% the GPS used as reference for the ship (no bias, as the ship doesn't
% drift when running on wheels!). 

%% Figure export - CURRENTLY COMMENTED OUT!:
% print(h1,'-depsc2','-painters','KF_pos_monorate.eps');
% print(h2,'-depsc2','-painters','KF_vel_monorate.eps');
% print(h3,'-depsc2','-painters','KF_acc_monorate.eps');
% print(h4,'-depsc2','-painters','KF_xy_monorate.eps');
% 
% print(h5,'-depsc2','-painters','KF_pos_multirate.eps');
% print(h6,'-depsc2','-painters','KF_vel_multirate.eps');
% print(h7,'-depsc2','-painters','KF_acc_multirate.eps');
% print(h8,'-depsc2','-painters','KF_xy_multirate.eps');
% 
% print(h9,'-depsc2','-painters','KF_pos_mnirate.eps');
% print(h10,'-depsc2','-painters','KF_vel_mnirate.eps');
% print(h11,'-depsc2','-painters','KF_acc_mnirate.eps');
% print(h12,'-depsc2','-painters','KF_xy_mnirate.eps');
% 
% print(h13,'-depsc2','-painters','poserror.eps');
% print(h14,'-depsc2','-painters','velerror.eps');
% print(h15,'-depsc2','-painters','accerror.eps');
% print(h16,'-depsc2','-painters','xyerror.eps');
