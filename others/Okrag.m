x=[1.7745828; 1.5564247; 1.4031123; 3.9001242; 1.3169531; 3.5428623; 1.2130591;
   1.0662723; 0.0019728; -0.0916895; 4.0942799; 0.4960777; 1.7870018;
   3.5777697; 2.6105061; 3.2787335; 1.2084442; 2.2590815; 3.2846900;
   4.2947338; 2.0773552; 0.5919104; 4.0648706; 1.1978026; 3.1357813];

y=[0.223926; 4.679744; 3.118928; 1.671998; 4.489287; 0.202165; 1.727469;
   0.326929; 2.908360; 4.218851; 2.602819; 3.197936; 4.512759;
   2.987913; 3.499582; 3.457453; -0.516197; 4.796360; 0.027931;
   2.384780; 5.067981; 4.623044; 0.792238; 3.187952; 1.389320];


figure(1)
plot(x,y, '.')
hold on
axis equal;

function err = kolko(T, X, Y)
  inside = sqrt((X - T(1)) .^ 2 + (Y - T(2)) .^ 2) - T(3);
  err = sumsq(inside);
endfunction


x0 = sqp([0,0,0], @(T)(kolko(T, x, y)));


alpha = linspace(0, 2*pi, 100);
new_x = x0(1) + x0(3) * cos(alpha);
new_y = x0(2) + x0(3) * sin(alpha)



plot(new_x, new_y);
hold off

figure(2)

alpha = 1 * pi * rand(20,1);
x0=7;
y0=3;
r=4;
sigma=.3;
x= x0 + r*cos(alpha) + normrnd(0,sigma,size(alpha));
y= y0 + r*sin(alpha) + normrnd(0,sigma,size(alpha));

plot(x,y, '.')
axis equal;
hold on

x0 = sqp([0,0,0], @(T)(kolko(T, x, y)));


alpha = linspace(0, 2*pi, 100);
new_x = x0(1) + x0(3) * cos(alpha);
new_y = x0(2) + x0(3) * sin(alpha)

plot(new_x, new_y);
hold off

