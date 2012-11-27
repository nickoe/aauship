%% Kalman Filter Implementation for AAUSHIP1:
% Rasmus Christensen 26/11/2012 - 12gr730 - AAUSHIP Kalaman Filter (c) 
%
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
% Y(n) = A(n) * Y(n-1) + W(n), where W(n) is driving noise/input to the
% system. 
%
% Then the measuremen vector X can be defined as:
% X(n) = H(n) * Y(n) + Z(n), where Z(n) expresses the noisy measurements. 
%
% The desired measurements can be described as (the definition of the A
% matrix):

%% System Definition:
A = [1 ts ts^2/2 0 0 0 0 0 0;... % The X position
     0 1 ts 0 0 0 0 0 0;... % The X velocity
     0 -betaX 0 0 0 0 0 0 0;... % The X acceleration is a sum of forward motion (F_forward - F_drag)
     0 0 0 1 ts ts^2/2 0 0 0;... % The Y Position
     0 0 0 0 1 ts 0 0 0;... % The Y Velocity
     0 0 0 0 -betaY 0 0 0 0;... % The Y acceleration is a sum of the sideways motion (F_ymotion (wind?) - F_dragY)
     0 0 0 0 0 0 1 ts ts^2/2;... % The angle
     0 0 0 0 0 0 0 1 ts;... % The angular velocity
     0 0 0 0 0 0 0 -betaW 0]; % The angular acceleration is a sum of the drag an induced torque!
 
H = eye(9); % An eye matrix, as all the outputs scales equally - everything is in metric units!

%% Noise Terms:
% The W(n) is the "driving noise" - as the system input is a forward force
% and a torque, these are input here as well. The "input" matrix for the
% driving noise W(n) is then equal to: 
W = [0 0;...
     0 0;...
     1/m 0;... % From force to input acceleration
     0 0;...
     0 0;...
     0 0;...
     0 0;...
     0 0;...
     0 1/I]; % From torque to angular acceleration

% Z is the measurement noise on the system, this can be estimated to be
% white gaussian noise, with zero mean (for most cases) and with a
% variance, that are estimated in Appendix #XX.
varXpos = 2;
varXvel = 2;
varXacc = 2;

varYpos = 2;
varYvel = 2;
varYacc = 2;

varWpos = 2;
varWvel = 2;
varWacc = 2;

Z = randn(9,1) + sqrt([varXpos varXvel varXacc varYpos varYvel varYacc varWpos varWvel varWacc])'; % Random number at each iteration with a given variance. 

%% Covariance Matrices: 
% As the vector Kalman filter have several system inputs, the noise added
% to the system generates a covariance matrix. These are computed below.

%% Running Computation of the Kalman filter:


%% Removing including sampling removal:
% As not all of the measurements are sampled at the same time (some are
% slower, as the GPS for instance) - the samples where no GPS reading is
% available will have to increase the level of the noise. Below is a list
% of the sampling speeds of the sensors mounted on the ship:
% GPS = 1Hz;
% IMU = 20Hz;
% This calls for attention to the GPS measurements, as these are not
% sampled as often as the IMU! When this is done, the computation of the
% Kalman filter becomes: 

%% Estiamting a Wind Bias:
% As Wind might push the ship out of course (constantly in the same
% direction) this can be considered a bias to the system. This is then to
% be subtracted, so the system only computes on the actual data, rather
% than the wind-biased data. 

%% Combined Kalman filter with test inputs:
% Below is a simulation of a walk around the parking lot, with the IMU and
% the GPS used as reference for the ship (no bias, as the ship doesn't
% drift when running on wheels!). 