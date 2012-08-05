% データ読み込み
data = load('fig47rnd.txt');
x = data(:, 1:2);
y = data(:, 3);

% w を適当に初期化
w = rand(1,2) * 0.001;

% η:学習率パラメータ
eta = 1;

% 確率的勾配降下法
maxiter = 100;
converged = maxiter + 1;

for t = 1:maxiter
  plotData(x, y, w, t);

  s = (x * w') .* y;
  bad = find(s < 0);
  if length(bad) == 0
    converged = t-1;
    break;
  end

  delta = sum((x(bad,:) .* [y(bad) y(bad)]) * eta);
  w += delta;
end

if (converged <= maxiter)
  fprintf("%d 回で収束\n", converged);
else
  fprintf("%d 回では収束せず\n", maxiter);
end
