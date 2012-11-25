%% Revolution Calculator:
% Forward system (both n are positive)

K = 0.05^4*0.5*1000;
theta = pi/16;
C1 = 0.5*sin(theta);
C2 = 0.5*sin(-theta);

A = [K K;K*C1 K*C2];
b = [-100;-10];
x = A\b;
y=[sign(x(1))*sqrt(abs(x(1)));sign(x(2))*sqrt(abs(x(2)))]

F = K*sign(y(1))*y(1)^2 + K*sign(y(2))*y(2)^2;
T = K*C1*sign(y(1))*y(1)^2 + K*C2*sign(y(2))*y(2)^2;