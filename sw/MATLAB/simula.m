%% Simulation of Kalman Filter for Position Measurements (3-dimensional)
% CA1 - 730
% Nick Østergaard, Frederik Juul, Tudor Muresan, Rasmus L. Christensen and
% Attila Fodor

clc, clear all, close all; % The latter must be changed if you want to make a movie!
format short
% Simulation parameters
N = 10000; % Number of samples
ts = .01;
no_samples = 1:1:N/ts;
%% Computation of system constants used for simulation:

% The mass and inertia of the ship is defined here: 
m = 13; % Mass of the ship
I = (1/12)*m*(0.25*0.25+1.05*1.05)*2;

% For simulation purposes the below can be used as a reference, this system
% will have a big drag in sway and heave direction, whilst the one in the
% forward direction is low. 
Cd = 0.5;
rho = 999.9925;
rho_air = 1.2690;
A_h = 0.5*0.232*0.1;
depth = 0.09;
rf = 0.5;
rr = 0.55;
D = 0.05;
Kt = 0.5;
l = 0.5;
Cd_y = 0.9;
A_y = 1.05*0.1;

% The system is to be extended, so the noise is zero meaned. 

% Variances of the measurement instruments:
varPOSX = 3;
varVELX = 0.01; % Variance of velocity measurements
varACCX = 0.009; % variance of acceleration measurements
varPOSY = 3;
varVELY = 0.01;
varACCY = 0.009;
varANGA = 0.7; % variance of angular acceleration
varANGV = 0.1; % variance of angular velocity
varANG = 0.01; % variance of the angle measurement

varWN = [sqrt(varPOSX) sqrt(varVELX) sqrt(varACCX) sqrt(varPOSY) sqrt(varVELY) sqrt(varACCY) sqrt(varANGA) sqrt(varANGV) sqrt(varANG)]'; % variance vector

%% Generation of Simulation Data:
% The below generates a function where the ship applies equal revolutions to the
% ship for the first 500 samples, then increases revolutions on one
% propeller, and then back again. 
n1 = [100*ones(1,0.1*N) 105*ones(1,0.1*N) 100*ones(1,0.1*N) 95*ones(1,0.1*N) 100*ones(1,0.1*N) 105*ones(1,0.1*N) 100*ones(1,0.1*N) 95*ones(1,0.1*N) 100*ones(1,0.1*N) 105*ones(1,0.1*N)]'; % Engine one is set to constantly apply 500 revolutions.
n2 = [100*ones(1,0.1*N) 95*ones(1,0.1*N) 100*ones(1,0.1*N) 105*ones(1,0.1*N) 100*ones(1,0.1*N) 95*ones(1,0.1*N) 100*ones(1,0.1*N) 105*ones(1,0.1*N) 100*ones(1,0.1*N) 95*ones(1,0.1*N)]'; % Engine two applies 500 revolutions, then changes to 700 then back to 500 again. 
U = [n1 n2]';

%% Kalman Filtering



% The observation matrix adds noise to the measurements. 
% X(n) = A(n) * Y(n) + W(n), where A(n) is defined as:
An = eye(9); % The identity function, as we measure all the constants directly.

% The W(n) term is the noise in the sensors. This is assumed to be white
% gaussian uncorrelated noise. The noise is given as the following:
Wn = [zeros(9,N)];
Wn(:,1) = [randn(9,1)].*varWN; % Initiation of the system.

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
ranv = [0 0 1 0 0 1 0 0 0]';
phi = pi/16;
for ii = 1:N
            k1 = rho*(D^4)*Kt*abs(n1(ii));
            k2 = rho*(D^4)*Kt*abs(n2(ii));
            k3 = rho*(D^4)*Kt*abs(n1(ii))*l*sin(phi);
            k4 = rho*(D^4)*Kt*abs(n2(ii))*l*sin(phi);
            Bl = [0 0;
                  0 0;...
                  k1/m k2/m;
                  0 0;
                  0 0;
                  0 0;
                  k3/I -k4/I;
                  0 0;
                  0 0];
                  %0 0;
                  %0 0];
      Zn(:,ii) = Bl*U(:,ii); % Input stream to the system.
end



%% Kalman Filtering
% Initiation of the Kalman filter - the ship is assumed to start at [0,0]
Ypred = zeros(9,N); % Prediction of Y
Xpred = zeros(9,N); % Prediction of X
Rpred = zeros(9,9,N); % Prediction of R
B = zeros(9,9,N); % Kalman filter gain B

Yupdate = zeros(9,N); % Update step of Y
Rupdate = zeros(9,9,N); % Update step of R

X = zeros(9,N);
Y = zeros(9,N);
Y2 = zeros(9,N);
Wind = zeros(9,N);
k_newpos = zeros(2,N);
y_newpos = zeros(2,N);
x_newpos = zeros(2,N);
yw_newpos = zeros(2,N);
k_newpos(:,1) = [-90;-90];
x_newpos(:,1) = [-90;-90];
y_newpos(:,1) = [-90;-90];
yw_newpos(:,1) = [-90;-90];

% Covariance matrix of Z(n)
% The Covariance matrix is given as:
  
% Covariance matrix W(n)


% Environmental disturbance parameters:
wA = 1/5*pi; % Wind Angle
wS = 2.5; % Wind speed

cA = -1/8*pi; % Current Angle
cS = 0.1; % Current Speed

% Describe the H matrix. (inputs and outputs!)


for n = 2:1:N
     % Simulation parameters are changed, as the system dynamic change at
     % each time step (for nonlinear dynamics).
     Rw(:,:,n) = [cos(Y(9,n-1)) -sin(Y(9,n-1));sin(Y(9,n-1)) cos(Y(9,n-1))];
     
     % Below is the computation of the Wind Disturbance
   Wind_l(:,n) = ([0 0 wS*cos(wA) 0 0 wS*sin(wA) 0 0 0]'+ranv.*randn(9,1)*sqrt(0.000001)); % Local Frame wind velocity
   Wind_f(:,n) = [rho_air*Cd*A_h*0.5*Wind_l(3,n)^2;rho_air*Cd_y*A_h*0.5*Wind_l(6,n)^2];
   Wind_b(:,n) = Rw(:,:,n)\[Wind_f(1,n);Wind_f(2,n)];
     Wind(:,n) = [0 0 Wind_b(1,n) 0 0 Wind_b(2,n) 0 0 0]';
     
      % Below is a computation of the Current Disturbance
%    Curr_f(:,n) = [rho*Cd*A_h*0.5*Curr_l(3,n)^2;rho*Cd_y*A_h*0.5*Curr_l(6,n)^2];
%    Curr_b(:,n) = inv(Rw(:,:,n))*[Curr_f(1,n);Curr_f(2,n)];
%      Curr(:,n) = [0 0 Curr_b(1,n) 0 0 Curr_b(2,n) 0 0 0]';
     
      % The noise terms are added together.
       Zn2(:,n) = Zn(:,n) + Wind(:,n);% + Curr(:,n);
       
      % Drag in the different directions:
       alphaVX = abs(Y(2,n-1))*Cd*A_h*0.5*rho;
       alphaVY = abs(Y(5,n-1))*Cd_y*A_y*0.5*rho;
        alphaW = 1/8*Cd*rho*depth*(rf^4+rr^4)*abs(Y(8,n-1));
        
      % Computation of the H(n) matrix as this changes over time.
            Hn = [1 ts ts^2/2 0 0 0 0 0 0;...
                  0 1 ts 0 0 0 0 0 0;...
                  0 -alphaVX/m 0 0 0 0 0 0 0;...
                  0 0 0 1 ts ts^2/2 0 0 0;...
                  0 0 0 0 1 ts 0 0 0;...
                  0 0 0 0 -alphaVY/m 0 0 0 0;...
                  0 0 0 0 0 0 0 -alphaW/I 0;...
                  0 0 0 0 0 0 ts 1 0;...
                  0 0 0 0 0 0 ts^2/2 ts 1];
              
     % Kalman filter is computed below:
       Wn(:,n) = randn(9,1).*varWN; % Measuremnet noise (all the sensors are IID uncorrelated).
            Qw = diag([varPOSX varVELX varACCX varPOSY varVELY varACCY varANGA varANGV varANG]); % Uncorrelated Zero-mean processes!
            Qz = cov(Zn2(:,n-1)*Zn2(:,n)'); % Covariance of Zn (the input to the system, noiseless in this case!)
        Y(:,n) = Hn*Y(:,n-1)+Zn(:,n);
       Y2(:,n) = Hn*Y2(:,n-1)+Zn2(:,n); % System with added environment vector
        X(:,n) = An*Y(:,n)+Wn(:,n);
    Ypred(:,n) = Hn*Yupdate(:,n-1);
    Xpred(:,n) = An*Ypred(:,n);
  Rpred(:,:,n) = Hn*Rupdate(:,:,n-1)*Hn'+Qz;
      B(:,:,n) = (Rpred(:,:,n)*An')/(An*Rpred(:,:,n)*An'+Qw);
  Yupdate(:,n) = Ypred(:,n)+B(:,:,n)*(X(:,n)-Xpred(:,n));
Rupdate(:,:,n) = (eye(9)-B(:,:,n)*An)*Rpred(:,:,n);
%Rupdate(:,:,n) = (eye(9) - B(:,:,n)*An)*Rpred(:,:,n)*(eye(9) - B(:,:,n)*An)'+(B(:,:,n)*Qw*B(:,:,n)'); % Joseph Form if system is
%numerically unstable
   y_newpos(:,n) = y_newpos(:,n-1) + Rw(:,:,n)*[Y(2,n-1);Y(5,n-1)].*ts;
  yw_newpos(:,n) = yw_newpos(:,n-1) + Rw(:,:,n)*[Y2(2,n-1);Y2(5,n-1)].*ts;
   k_newpos(:,n) = k_newpos(:,n-1) + Rw(:,:,n)*[Yupdate(2,n-1);Yupdate(5,n-1)].*ts;
   x_newpos(:,n) = x_newpos(:,n-1) + Rw(:,:,n)*[X(2,n-1);X(5,n-1)].*ts;
end

Y_kal_pos_X = Yupdate(1,:)';  % Kalman filtered ouput
Y_kal_vel_X = Yupdate(2,:)';
Y_kal_acc_X = Yupdate(3,:)';
Y_kal_pos_Y = Yupdate(4,:)';
Y_kal_vel_Y = Yupdate(5,:)';
Y_kal_acc_Y = Yupdate(6,:)';
Y_kal_angA = Yupdate(7,:)'; 
Y_kal_angV = Yupdate(8,:)';
Y_kal_ang = Yupdate(9,:)'; % 

X_pos_X = X(1,:)'; % Measured output
X_vel_X = X(2,:)';
X_acc_X = X(3,:)';
X_pos_Y = X(4,:)';
X_vel_Y = X(5,:)';
X_acc_Y = X(6,:)';
X_angA = X(7,:)';
X_angV = X(8,:)';
X_ang = X(9,:)';

Y_pos_X = Y(1,:)'; % True position
Y_vel_X = Y(2,:)';
Y_acc_X = Y(3,:)';
Y_pos_Y = Y(4,:)';
Y_vel_Y = Y(5,:)';
Y_acc_Y = Y(6,:)';
Y_angA = Y(7,:)';
Y_angV = Y(8,:)';
Y_ang = Y(9,:)';

% Plot of the position
h1 = figure(1);
hold on
plot(X_pos_X,'g+','MarkerSize',2);
plot(Y_kal_pos_X,'b','LineWidth',1);
plot(Y_pos_X,'m','LineWidth',1);
hold off
title('Distance')
legend('Observed','Filtered','True')
xlabel('Sample [n]') ;ylabel('Distance [m]');
grid on
% 
% Figure plot of the velocity
h2 = figure(2);
hold on
plot(X_vel_X,'g+','MarkerSize',2);
plot(Y_kal_vel_X,'b','LineWidth',1);
plot(Y_vel_X,'m','LineWidth',1);
hold off
title('Velocity')
legend('Observed','Filtered','True')
xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
grid on
% 
% Figure plot of the acceleration
h3 = figure(3);
hold on
plot(X_acc_X,'g+','MarkerSize',2);
plot(Y_kal_acc_X,'b','LineWidth',1);
plot(Y_acc_X,'m','LineWidth',1);
hold off
title('Acceleration')
legend('Observed','Filtered','True')
xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
grid on
% 
% % Figure plot of the angular acceleration
% h4 = figure(4);
% hold on
% plot(X_angA,'g+','MarkerSize',2);
% plot(Y_kal_angA,'b','LineWidth',1);
% plot(Y_angA,'m','LineWidth',1);
% hold off
% title('Angular Acceleration')
% legend('Observed','Filtered','True')
% xlabel('Sample [n]') ;ylabel('Angular Acceleration [radians/s^2]');
% grid on
% 
% % Figure plot of the angular velocity
% h5 = figure(5);
% hold on
% plot(X_angV,'g+','MarkerSize',2);
% plot(Y_kal_angV,'b','LineWidth',1);
% plot(Y_angV,'m','LineWidth',1);
% hold off
% title('Angular Velocity')
% legend('Observed','Filtered','True')
% xlabel('Sample [n]') ;ylabel('Angular Velocity [radians/s]');
% grid on
% 
% % Figure plot of the angle
% h6 = figure(6);
% hold on
% plot(X_ang,'g+','MarkerSize',2);
% plot(Y_kal_ang,'b','LineWidth',1);
% plot(Y_ang,'m','LineWidth',1);
% hold off
% title('Angle')
% legend('Observed','Filtered','True')
% xlabel('Sample [n]') ;ylabel('Angle [radians]');
% grid on
% 

% Plot of XY Position
h7 = figure(7)
hold on
plot(X_pos_X,X_pos_Y,'g+','MarkerSize',2);
plot(Y_kal_pos_X,Y_kal_pos_Y,'b','LineWidth',1);
plot(Y_pos_X,Y_pos_Y,'m','LineWidth',1);
hold off
title('XY Plot')


% % Figure plot of Y-position
% h7 = figure(7);
% hold on
% plot(X_pos_Y,'g+','MarkerSize',2);
% plot(Y_kal_pos_Y,'b','LineWidth',1);
% plot(Y_pos_Y,'m','LineWidth',1);
% hold off
% title('Y-Distance')
% legend('Observed','Filtered','True')
% xlabel('Sample [n]') ;ylabel('Distance [m]');
% grid on
% 
% % Figure plot of the velocity
% h8 = figure(8);
% hold on
% plot(X_vel_Y,'g+','MarkerSize',2);
% plot(Y_kal_vel_Y,'b','LineWidth',1);
% plot(Y_vel_Y,'m','LineWidth',1);
% hold off
% title('Y-Velocity')
% legend('Observed','Filtered','True')
% xlabel('Sample [n]') ;ylabel('Velocity [m/s]');
% grid on
% 
% % Figure plot of the acceleration
% h9 = figure(9);
% hold on
% plot(X_acc_Y,'g+','MarkerSize',2);
% plot(Y_kal_acc_Y,'b','LineWidth',1);
% plot(Y_acc_Y,'m','LineWidth',1);
% hold off
% title('Y-Acceleration')
% legend('Observed','Filtered','True')
% xlabel('Sample [n]') ;ylabel('Acceleration [m/s^2]');
% grid on
% 
% True Position
[wX,wY] = meshgrid(min([yw_newpos(1,:) y_newpos(2,:)])-1:3:max([yw_newpos(1,:) y_newpos(2,:)]+1));
[cX,cY] = meshgrid(min([yw_newpos(1,:) y_newpos(2,:)])-1:3:max([yw_newpos(1,:) y_newpos(2,:)]+1));

h10 = figure(10);
hold on
plot(x_newpos(1,:),x_newpos(2,:),'g+','MarkerSize',2);
plot(k_newpos(1,:),k_newpos(2,:),'b','LineWidth',1);
plot(y_newpos(1,:),y_newpos(2,:),'r','LineWidth',1);
plot(y_newpos(1,:),y_newpos(2,:),'m','LineWidth',1);
plot(y_newpos(1,1),y_newpos(2,1),'k*','MarkerSize',15);
plot(y_newpos(1,.2*N),y_newpos(2,0.2*N),'k*','MarkerSize',15);
plot(y_newpos(1,0.7*N),y_newpos(2,0.7*N),'k*','MarkerSize',15);
plot(y_newpos(1,0.9*N),y_newpos(2,0.9*N),'k*','MarkerSize',15);
plot(y_newpos(1,N),y_newpos(2,N),'k*','MarkerSize',15);
%quiver(wX,wY,Wind_l(3,j).*ones(size(wX)),Wind_l(6,j).*ones(size(wY)),0.1,'yellow');
%quiver(cX,cY,Curr_l(3,j).*ones(size(cX)),Curr_l(6,j).*ones(size(cY)),0.1,'cyan');
hold off
grid on
axis equal
title('XY-Position - Local Frame')
legend('Observed','Filtered','True','Change',sprintf('Distance %.1f',Y_pos_X(N)))
xlabel('X-position [m]') ;ylabel('Y-position [m]');
print(h10,'-depsc2','-painters','xypos.eps')

% h11 = figure(11);
% 
% % Generation of Simulated Ocean floor:
% konstant1 = 0.02;
% konstant2 = 0.04;
% [X_sea,Y_sea] = meshgrid(linspace(-100,100));
% seabed = -(5+cos(konstant1*X_sea).*(3+cos(konstant2*Y_sea)));
%surf(X_sea,Y_sea,seabed) % Plots it further down!

% Adding a Z = 0 element to the positions!


% % Running Simulation:
% for j = 1:N
%     theta = Y(9,j); % Angle between local frame and ship!
%     velocity = (Y2(2,j)); % Velocity of the ship
%     yvelocity = (Y2(5,j)); % Velocity of the ship in the Y-direction (wind, current etc.)
%     xyzpos = [y_newpos(1,:);y_newpos(2,:);zeros(1,numel(y_newpos(2,:)))];
%     %drawnow
%     %koordA = [y_newpos(1,j)+lengthA*cos(Y(9,j));y_newpos(2,j)+lengthA*sin(Y(9,j))]
%     %koordB = [y_newpos(1,j)+lengthB*cos(Y(9,j));y_newpos(2,j)+lengthB*sin(Y(9,j))]
%     R = [cos(Y(9,j)) -sin(Y(9,j)) 0;sin(Y(9,j)) cos(Y(9,j)) 0;0 0 1]'; % Rotation matrix - TRANSPOSED!!!!!!
%     L = [-0.5 0.55 -0.5 -0.3 -0.5;...
%          0.125 0 -0.125 0 0.125;
%          0 0 0 0 0]'; % Ship Triangle matrix
%     Pos = bsxfun(@plus,(L*R)',xyzpos(:,j)); % Triangle orientation update
%     % Ship forces:
%     L2 = [Y2(3,j)*m 0 0;0 Y2(6,j)*m 0;0 0 0];
%     force = bsxfun(@plus,(L2*R)',xyzpos(:,j));
%     if abs(Y(8,j)) > 0
%         r=velocity/Y(8,j);
%     end
% % subplot(2,2,[1 3])
%     plot3(Pos(1,:),Pos(2,:),Pos(3,:),'m',xyzpos(1,j),xyzpos(2,j),xyzpos(3,j),'m*')%,[xyzpos(1,j);force(1,1)],[xyzpos(2,j);force(2,1)],'k',[xyzpos(1,j);force(1,2)],[xyzpos(2,j);force(2,2)],'k');
%     hold on
%     plot3(xyzpos(1,:),xyzpos(2,:),xyzpos(3,:),'k');
% 
% % Change in revolution points plotted
%      plot3(xyzpos(1,1),xyzpos(2,1),xyzpos(3,1),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.1*N),xyzpos(2,0.1*N),xyzpos(3,0.1*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.2*N),xyzpos(2,0.2*N),xyzpos(3,0.2*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.3*N),xyzpos(2,0.3*N),xyzpos(3,0.3*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.4*N),xyzpos(2,0.4*N),xyzpos(3,0.4*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.5*N),xyzpos(2,0.5*N),xyzpos(3,0.5*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.6*N),xyzpos(2,0.6*N),xyzpos(3,0.6*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.7*N),xyzpos(2,0.7*N),xyzpos(3,0.7*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.8*N),xyzpos(2,0.8*N),xyzpos(3,0.8*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,.9*N),xyzpos(2,0.9*N),xyzpos(3,0.9*N),'k*','MarkerSize',15);
%      plot3(xyzpos(1,N),xyzpos(2,N),xyzpos(3,N),'k*','MarkerSize',15);
% 
% % Lines to bottom (from the above points:
%      plot3([xyzpos(1,1);xyzpos(1,1)],[xyzpos(2,1);xyzpos(2,1)],[xyzpos(3,1);-7],'k');
%      plot3([xyzpos(1,0.1*N);xyzpos(1,0.1*N)],[xyzpos(2,0.1*N);xyzpos(2,0.1*N)],[xyzpos(3,0.1*N);-7],'k');
%      plot3([xyzpos(1,0.2*N);xyzpos(1,0.2*N)],[xyzpos(2,0.2*N);xyzpos(2,0.2*N)],[xyzpos(3,0.2*N);-7],'k');
%      plot3([xyzpos(1,0.3*N);xyzpos(1,0.3*N)],[xyzpos(2,0.3*N);xyzpos(2,0.3*N)],[xyzpos(3,0.3*N);-7],'k');
%      plot3([xyzpos(1,0.4*N);xyzpos(1,0.4*N)],[xyzpos(2,0.4*N);xyzpos(2,0.4*N)],[xyzpos(3,0.4*N);-7],'k');
%      plot3([xyzpos(1,0.5*N);xyzpos(1,0.5*N)],[xyzpos(2,0.5*N);xyzpos(2,0.5*N)],[xyzpos(3,0.5*N);-7],'k');
%      plot3([xyzpos(1,0.6*N);xyzpos(1,0.6*N)],[xyzpos(2,0.6*N);xyzpos(2,0.6*N)],[xyzpos(3,0.6*N);-7],'k');
%      plot3([xyzpos(1,0.7*N);xyzpos(1,0.7*N)],[xyzpos(2,0.7*N);xyzpos(2,0.7*N)],[xyzpos(3,0.7*N);-7],'k');
%      plot3([xyzpos(1,0.8*N);xyzpos(1,0.8*N)],[xyzpos(2,0.8*N);xyzpos(2,0.8*N)],[xyzpos(3,0.8*N);-7],'k');
%      plot3([xyzpos(1,0.9*N);xyzpos(1,0.9*N)],[xyzpos(2,0.9*N);xyzpos(2,0.9*N)],[xyzpos(3,0.9*N);-7],'k');
%      plot3([xyzpos(1,N);xyzpos(1,N)],[xyzpos(2,N);xyzpos(2,N)],[xyzpos(3,N);-7],'k');
%      surf(X_sea,Y_sea,seabed);
%      
% % Force plot of Wind and Current is below:
%     %quiver(wX,wY,Wind_l(3,j).*ones(size(wX)),Wind_l(6,j).*ones(size(wY)),0.1);
%     %quiver(cX,cY,Curr_l(3,j).*ones(size(cX)),Curr_l(6,j).*ones(size(cY)),0.1,'cyan');
%     
% % The below generates the turning radius circle
%     if abs(Y(8,j)) > 0
%         theta2 = -9*pi/16:0.01:-7/16*pi; % Size of Turning Radius
%         %theta2 = 0:0.01:2*pi;
%             cirB = R'*[r*cos(theta2);r*sin(theta2)+r;zeros(1,numel(theta2))];
%             cirA = bsxfun(@plus,cirB,xyzpos(:,j));
%             plot3(cirA(1,:),cirA(2,:),cirA(3,:),'r','LineStyle','--');
%     end
%     hold off
%     
%     %pause(0.00001)
%     %clc
%     grid on
%     title('XY-Position Local Frame')
%     xlabel('X Position [m]')
%     ylabel('Y Position [m]')
%     zlabel('Z Position, depth [m]')
%     axis equal
%     view([30 31])
%    % xlim([min([yw_newpos(1,:) y_newpos(1,:)])-1 max([yw_newpos(1,:) y_newpos(1,:)])+1]);
%    % ylim([min([yw_newpos(2,:) y_newpos(2,:)])-1 max([yw_newpos(2,:) y_newpos(2,:)])+1]);
%     
% %     subplot(2,2,2)
% %     drawnow
% %     plot(j,Y2(2,j),'b*',j,Y2(5,j),'r*','MarkerSize',10); hold on
% %     plot(Y2(2,:),'b','LineWidth',1);
% %     plot(Y2(5,:),'r','LineWidth',1);
% %     hold off
% %     grid on
% %     title('Velocity');
% %     ylabel('Velocity [m/s]');
% %     
% %     subplot(2,2,4)
% %     drawnow
% %     plot(j,Y2(3,j),'b*',j,Y2(6,j),'r*','MarkerSize',10); hold on
% %     plot(Y2(3,:),'b','LineWidth',1);
% %     plot(Y2(6,:),'r','LineWidth',1);
% %     hold off
% %     grid on
% %     title('Acceleration');
% %     ylabel('Acceleration [m/s^2]');
% %     xlabel('Sample [n]');
% meas(j) = (-(5+cos(konstant1*xyzpos(1,j)).*(2+cos(konstant2*xyzpos(2,j)))));
%     
%     % M((j)) = getframe(h11); % Converting it into a movie
% end
% print(h11,'-depsc2','-painters','plot.eps')
% %movie2avi(M,'aauship.avi', 'compression', 'None'); % Conversion into a
% %movie
% h12 = figure(12);
% plot(meas(:))
% hold off
% xlabel('Sample [n]')
% ylabel('Measured Depth [m]')
% grid on
% print(h12,'-depsc2','-painters','depth.eps')

h13 = figure(13);
subplot(2,1,1)
plot(U(1,:)')
title('Engine 1 input');
ylim([95 110])
ylabel('Revolutions [rps]');
grid on
subplot(2,1,2)
plot(U(2,:)')
title('Engine 2 input');
xlabel('Sample [n]')
ylabel('Revolutions [rps]');
ylim([95 110])
grid on
print(h13,'-depsc2','-painters','revol.eps')



%% Controller Computation - NOT DONE YET!
A = Hn;
B = [Zn(:,N-1) Zn(:,N)];
Qopt = diag([1/((100)^2) 1/(5^2) 1/(10^2) 1/((100)^2) 1/(5^2) 1/(10^2) 1/((2*pi)^2) 1/(5^2) 1/(10^2)])
Ropt = diag([0 0 1/(4^2) 0 0 0 1/(1^2) 0 0 0])
