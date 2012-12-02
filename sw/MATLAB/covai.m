%% Distributions:
% F = N(5.3544,50^2)
% T = N(0,pi^2)

K = 1000;

my_F = [zeros(2,1);5.3544;zeros(6,1)];
my_T = [zeros(9,1)];
si_F = [zeros(2,1);50^2;zeros(6,1)];
si_T = [zeros(8,1);pi^2];
out = zeros(9,K);
Rxx = zeros(9,9,K);

for n = 1:K
    out(:,n) = randn(9,1).*sqrt(si_F+si_T) + (my_F+my_T);
end
cov(out(:,n-1)*out(:,n)');


for j = 1:N
    covari(j,:) = autocorr(Z(:,j));
    Rxx(:,:,j) = toeplitz(covari(j,:)) - mean(Z(:,j));
end