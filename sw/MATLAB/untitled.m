%% Maiden Voyage Plot
% Rasmus Christensen
imu = load('accdata00185.csv');

%% Filtering algorithm:
%imuF = zeros(numel(accX),13);

% for fN = 2:numel(imu(:,1))
%     for fA = 1:13
%         if abs(imu(fN,fA) - imu(fN-1,fA)) < 5
%             imuF(fN,fA) = imu(fN,fA);
%         else
%             imuF(fN,fA) = imu(fN-1,fA);
%         end
%     end
% end

accS = 0.00333;
gyrS = 1/20;
graA = 9.816;
magS = 1/1000;
temC = 0.14;

gyrY = imu(:,2)*gyrS; % X pointed starboard during test
gyrX = imu(:,3)*gyrS; % Y pointed backward during test
gyrZ = imu(:,4)*gyrS;

accY = imu(:,5)*accS; % X pointed starboard during test
accX = -imu(:,6)*accS; % Y pointed backward during test
accZ = imu(:,7)*accS;

accX = accZ.*accX;

accX = accX * graA;
accY = accY * graA;
accZ = accZ * graA;

magY = imu(:,8)*magS; % X pointed starboard during test
magX = imu(:,9)*magS; % Y pointed backward during test
magZ = imu(:,10)*magS;

temP = imu(:,11)*temC;

volT = imu(:,1);


%% Conversion from Magnetic Field Strength to Heading:
for i = 1:numel(magX)
    if magY(i) > 0
        heaX(i) = 90 - atan(magX(i)/magY(i));
    end
    if magY(i) < 0
        heaX(i) = 270 - atan(magX(i)/magY(i));
    end
    if magY(i) == 0 & magX(i) < 0
        heaX(i) = 180;
    end
    if magY(i) == 0 & magX(i) > 0
        heaX(i) = 0;
    end
end

time = [0:numel(accX)-1]/20;

%% Pitch Calculations:
for k = 1:numel(accX)
    pitch(k) = acos(graA/accZ(k))*(180/pi);
end

%% Plot of Data:
h1 = figure(1);
plot(time,accX); hold on
plot(time,accY,'r');
plot(time,temP);
plot(time,accZ,'g'); hold off
title('IMU Acceleration')
xlabel('Sample [n] (sampling speed 20 Hz)')
ylabel('Acceleration [m/s^2]')
legend('Normalized X Acceleration','Y Acceleration','Z Acceleration')

h2 = figure(2);
plot(time,gyrX); hold on
plot(time,gyrY,'r');
plot(time,gyrZ,'g'); hold off
title('IMU Angular velocity')
xlabel('Sample [n] (sampling speed 20 Hz)')
legend('X Angular Velocity','Y Angular Velocity','Z Angular Velocity')
%ylabel('Angular Velocity [radians/s]')

h3 = figure(3);
plot(time,heaX);
title('Heading Plot - Maiden Voyage')
%legend('Heading')
xlabel('Sample [n] (sampling speed 20 Hz)')
ylabel('Heading [degrees]');

h4 = figure(4);
stem(pitch'); hold on
title('Pitch of the ship');
plot(temP,'r'); hold off
