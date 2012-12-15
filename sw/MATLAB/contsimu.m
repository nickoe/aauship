%% Continous Time Simulation:
clc; clear all; clf;

ts = 0.05;

m = 12;
I = (1/12)*m*(0.25*0.25+1.05*1.05);
betaX = 8.9/m;
betaW = 3.77/I;
% The discrete state space model of the system is described below:
% System Dynamics:
A = [-betaX 0 0;...
     0 0 1;...
     0 0 -betaW];

% Input Matrix:
B = [1/m 0;...
     0 0;...
     0 1/I];
 
% Output Matrix:
C = [1 0 0;...
     0 1 0];
 
sys = ss(A,B,C,0);
poles = pole(sys)
sysD = c2d(sys,ts);
disc_poles = pole(sysD)
 
% Optimal poles, continous case
Q = diag([1/2 1/(2*pi*2*pi) 1/10000]); %1/max velocity^2, 1/max angle^2, 1/max ang. vel.^2
R = diag([1/1000 1/250]);
F = lqr(A,B,Q,R);
%F = lqr(A,B,80*C'*C,eye(2));

% Reference Gain Continous Case
A_nf =[A B;C zeros(2,2)];
B_nf = [zeros(3,2);eye(2)];
N_f = inv(A_nf)*B_nf;
Nxf = N_f(1:3,:);
Nuf = N_f(4:5,:);
N = Nuf + F*Nxf;

sim('contsim')
h1 = figure(1);
plot(output(:,1)); hold on
plot(output(:,2),'g');
plot(reference(:,1),'k--')
plot(reference(:,2),'k--')
hold off
grid on
title('Velocity and Angle plot')
xlabel('Time [s]')
ylabel('Velocity [m/s] and Angle [rad]')

h2 = figure(2);
K = 0.05^4*0.5*1000;
theta = pi/16;
C1 = 0.5*sin(theta);
C2 = 0.5*sin(-theta);

L = [K K;K*C1 K*C2];
for n = 1:numel(output(:,1)');
    rev(:,n) = L\input(n,:)';
    sy(:,n) =[sign(rev(1,n))*sqrt(abs(rev(1,n)));sign(rev(2,n))*sqrt(abs(rev(2,n)))];
end
eng1 = smooth(sy(1,:),11);
eng2 = smooth(sy(2,:),11);

plot(sy(1,:)); hold on
plot(sy(2,:),'r'); 
hold off
grid on
title('Engine Input - Continous');
legend('Engine 1','Engine 2');
xlabel('Time [s]');
ylabel('Revolutions [rps]');

h3 = figure(3);
plot(eng1,'blue'); hold on
plot(eng2,'m');
hold off
grid on

%% Computation of System without fluctuation in the engines:
 eng_input = [eng1 eng2]';
x = zeros(3,numel(eng1));
y = zeros(2,numel(eng1));
 for  i = 2:numel(eng1)
     u_input(:,i) = L*[eng_input(1,i)*abs(eng_input(1,i));eng_input(2,i)*abs(eng_input(2,i))];
 end
 
%% Same as above, but discrete.
sysD_F = lqr(sysD,Q,R);

A_nfd =[sysD.a sysD.b;sysD.c sysD.d];
B_nfd = [zeros(3,2);eye(2)];
N_fd = inv(A_nfd)*B_nfd;
Nxfd = N_f(1:3,:);
Nufd = N_f(4:5,:);
sysD_N = Nufd + sysD_F*Nxfd;
sim('discsim')

h4 = figure(4);
plot(outputD(:,1)); hold on
plot(outputD(:,2),'g');
plot(referenceD(:,1),'k--')
plot(referenceD(:,2),'k--')
hold off
grid on
title('Velocity and Angle plot - Discrete')
xlabel('Sample [n]')
ylabel('Velocity [m/s] and Angle [rad]')

for nDn = 1:numel(outputD(:,1)');
    revDn(:,nDn) = L\inputD_non(nDn,:)';
    syDn(:,nDn) =[sign(revDn(1,nDn))*sqrt(abs(revDn(1,nDn)));sign(revDn(2,nDn))*sqrt(abs(revDn(2,nDn)))];
end

h4 = figure(5);
subplot(2,1,1)
plot(syDn(1,:)); hold on
plot(syDn(2,:),'r'); 
hold off
grid on
title('Engine Input - Discrete - Non Filtered');
legend('Engine 1','Engine 2');
%xlabel('Sample [n]');
ylabel('Revolutions [rps]');

for nD = 1:numel(outputD(:,1)');
    revD(:,nD) = L\inputD(nD,:)';
    syD(:,nD) =[sign(revD(1,nD))*sqrt(abs(revD(1,nD)));sign(revD(2,nD))*sqrt(abs(revD(2,nD)))];
end

subplot(2,1,2)
plot(syD(1,:)); hold on
plot(syD(2,:),'r'); 
hold off
grid on
title('Engine Input - Discrete - Filtered');
legend('Engine 1','Engine 2');
xlabel('Sample [n]');
ylabel('Revolutions [rps]');

%% Computation of actual position:
% Computation is done, as the "new" position is equal to the last position
% plus the change due to velocity and the change in angle. 
y_newpos = zeros(2,numel(outputD(:,1)));
for nn = 2:numel(outputD(:,1))
    Rw(:,:,nn) = [cos(outputD(nn-1,2));sin(outputD(nn-1,2))];
    y_newpos(:,nn) = y_newpos(:,nn-1) + Rw(:,:,nn)*outputD(nn-1,1).*ts;
end
h6 = figure(6);
plot(y_newpos(1,:),y_newpos(2,:))
grid on
title('Position in Local Frame')
xlabel('X Position [m]')
ylabel('Y Posiiton [m]')
legend('Sailed track')

%% FFT:
h7 = figure(7);
Sxx_filt = ((abs(fftshift(fft(syDn)))).^2)./numel(outputD(:,1));
plot(fft(Sxx_filt)')
grid on

%% Save file:
%save('inputD', 'inputD')

%% Save Discrete Control Matrices
saveAname = 1;
saveA = sysD.a;
saveBname = 2;
saveB = sysD.b;
saveCname = 3;
saveC = sysD.c;
saveNname = 4;
saveN = sysD_N;
saveFname = 5;
saveF = sysD_F;
save('Sys_ABCNF', 'saveAname', 'saveA', 'saveBname', 'saveB', 'saveCname', 'saveC', 'saveNname', 'saveN', 'saveFname', 'saveF','-ascii', '-tabs');
clear save*