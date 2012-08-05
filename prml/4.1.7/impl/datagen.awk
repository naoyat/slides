BEGIN {
  srand()
  a = rand() - 0.5
  b = rand() - 0.5
  for (i=0; i<30; ++i) {
    x = rand()*2 - 1
    y = rand()*2 - 1
    xn = x + (rand()*0.5 - 0.25)
    yn = y + (rand()*0.5 - 0.25)
    s = (a*xn + b*yn >= 0) ? 1 : -1;
    printf("%g\t%g\t%d\n", x,y,s)
  }
  exit
}
