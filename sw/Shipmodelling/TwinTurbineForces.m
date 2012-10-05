clc
safety=inline('abs(n)<=pi/2');
theta=pi/2
Fl = -4;
Fr = 4;
Ftl = cos(theta)*Fl;
Ftr = cos(-theta)*Fr;
Fxl = cos(theta)*Ftl;
Fxr = cos(-theta)*Ftr;
Fx = safety(theta)*(Fxr+Fxl)
Fyl = Ftl-Fxl;
Fyr = Ftr-Fxr;
Fy = safety(theta)*(Fyl-Fyr)


FRl=Fl-Ftl;
FRr=Fr-Ftr;
FR=safety(theta)*(FRr-FRl)
