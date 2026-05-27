%
%  data for calculating Michaelis constant
%
% concentration of substract:
s = [0.25 	0.30 	0.40 	0.50 	0.70 	1.00 	1.40 	2.00]';
% production velocity:
v = [2.4 	2.6 	4.2 	3.8 	6.2 	6.4 	6.8 	7.4]';

% Linear approach:

X = 1. ./ s
Y = -1. ./ v
A=[X,Y];
b = -1*ones(size(X));
x = A \ b
Km = x(1);
a = x(2);


function err = michalis(T, X, Y)
  v_pred = (T(1) * X) ./ (X + T(2));
  err = sum((Y-v_pred) .^ 2);
endfunction

figure(3);
x0 = sqp([1,1], @(T)(michalis(T,s,v)));

plot(s, v, '.')
hold on
plot(s, (x0(1) *  s) ./ (x0(2) + s) );
hold off







