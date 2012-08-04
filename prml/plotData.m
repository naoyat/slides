function plotData(x, y, w, t)

a = w(1,1);
b = w(1,2);

figure; hold on;
title(sprintf('iter #%d', t));
axis([-1 1 -1 1]);

pos = find(y > 0);
neg = find(y < 0);
plot(x(pos,1), x(pos,2), '+b');
plot(x(neg,1), x(neg,2), '+r');

s = (x * w') .* y;
bad = find(s < 0);
plot(x(bad,1), x(bad,2), 'og', 'markersize', 10);

% ax + by = 0
%       y = -a/b x
%  x      = -b/a y

if a == 0
  plot([-1 1], [0 0], '-k', 'LineWidth', 1);
else if abs(a) < abs(b)
  plot([-1 1], [a/b -a/b], '-k', 'LineWidth', 1);
else
  plot([b/a -b/a], [-1 1], '-k', 'LineWidth', 1);
end

hold off;
end