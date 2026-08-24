 1;
 %Definiujemy parametry
 epsilon = [1e-5, 0.02, 0.5, 3];
 delta = 2e-4;
 q = 1e-4;
 f = [0.1,0.6,1.6];
 color = ['r', 'g', 'b', 'm'] %Kolorki...


 bifur = [];

 %Definiujemy przedzial czasowy i warunki początkowe
 tspan = linspace(0,100, 1000);
 U0 = [0.1; 0.3; 0.6];

 function wyn = oreg(U, T, epsilon, delta, q, f)
   x = U(1);
   y = U(2);
   z = U(3);

   %Definiujemy system
   dxdt = (q .* y - x .* y + x .* (1 - x)) ./ epsilon;
   dydt = (-q .* y - x .* y + 2 .* f .* z) ./ delta;
   dzdt = x - z;

   %Tworzymy wektor
   wyn = [dxdt; dydt; dzdt];

 endfunction

 %Petla która tworzy wykresy dla poszczególnych parametrów
 for i = 1:size(epsilon)(2)

   for j = 1:size(f)(2)
     figure(i, 'position', [100, 100, 800, 600]);

     %Definiujemy prawą stronę
     rhs = @(U, T) oreg(U, T, epsilon(i), delta, q, f(j));
     [U, t] = lsode(rhs, U0, tspan);

     %Wyciągamy poszczególne koordynaty
     x = U(:, 1);
     y = U(:, 2);
     z = U(:, 3);

     %Rysujemy...
     subplot(2, 2, j)

     plot3(x, y, z, 'LineWidth', 0.8, color(j));
     title(sprintf("Wykres 3D dla f = %.2f", f(j)));
     xlabel('x(t)');
     ylabel('y(t)');
     zlabel('z(t)');
     grid on;
     axis auto;

     %Dla drugiego wykresu tworzymy rzuty na poszczególne płaszczyzny
     if (j == 2)
       figure(10 + i, 'position', [100, 100, 800, 600]);

       % 1. Rzut na płaszczyznę x-y
       subplot(2, 2, 1);
       plot(x, y);
       title('Rzut na x-y');
       xlabel('x(t)');
       ylabel('y(t)');
       grid on;
       axis tight;

       % 2.  Rzut na płaszczyznę x-z
       subplot(2, 2, 2);
       plot(x, z);
       title('Rzut na x-z');
       xlabel('x(t)');
       ylabel('z(t)');
       grid on;
       axis tight;

       % 3.  Rzut na płaszczyznę y-z
       subplot(2, 2, 3);
       plot(y, z);
       title('Rzut na y-z');
       xlabel('y(t)');
       ylabel('z(t)');
       grid on;
       axis tight;

       % 4. Ponownie narysowany wykres 3D z innej perspektywy
       subplot(2, 2, 4);
       plot3(x, y, z, 'k-');
       title('Wykres 3D');
       xlabel('x');
       ylabel('y');
       zlabel('z');
       grid on;
       view(30, 30);
       axis tight;
     endif

   endfor
 endfor

 f_val = linspace(0.2, 3, 20);
 for i = 1:length(f_val)


   %Definiujemy prawą stronę
   rhs = @(U, T) oreg(U, T, 0.02, delta, q, f_val(i));
   [U, t] = lsode(rhs, U0, tspan);
   x = U(:, 1);
   y = U(:, 2);
   z = U(:, 3);
   bifur(end+1) = x(end) + y(end) + z(end);


 endfor
 figure(100, 'position', [100, 100, 800, 600]);
 plot(f_val, bifur);
 title('Bifurkacja dla epsilona = 0.02 wobec f')
 xlabel('Parameter f');
 ylabel('x(t) + y(t) + z(t)');
