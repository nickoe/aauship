nd = inline('1/(v*sqrt(2*pi))*exp(-(x-m).^2/(2*v.^2))','x','m','v');
figure(1)
f = figure(1)
r = -5:0.01:5;
plot([0 0 abs(r(find(r == 0):numel(r)))],[0 nd(0,0,1)*2 nd(abs(r(find(r == 0):numel(r))),0,1)*2],'b')
hold on
plot(r,nd(r,0,1),'r')
samples = randn(500000,1);
evar = var(abs(samples))
emean = mean(abs(samples))
plot(r,nd(r,emean,evar),'g')
hold off
legend('Distribution of absolute values','Actual distribution','Estimated distribution')

print(f, '-depsc2','-painters','absdistrib.eps')