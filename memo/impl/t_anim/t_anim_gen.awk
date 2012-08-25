BEGIN {
  N = maxnum*2 + 3
  delay = 33
  outfile = "t_anim.gif"

  lmax = 0
  rmax = 0
  hmax = 0
  for (i=0; i<N; i++) {
    system(sprintf("convert t_%03d.png t_%03d.bmp", i, i))
    cmd = sprintf("../util/topcenter t_%03d.bmp", i)
    cmd | getline
    if ($3 < 0) $3 = 0
    if ($4 < 0) $4 = 0
    w[i] = $1; h[i] = $2; x[i] = $3; y[i] = $4;
    if ($3 > lmax) lmax = $3;
    if ($1 - $3 > rmax) rmax = $1 - $3
    if ($2 > hmax) hmax = $2
    close(cmd)
    system(sprintf("rm -f t_%03d.bmp", i))
  }

  # system(sprintf("convert -size %dx%d xc:White white.bmp", lmax + rmax, hmax))

  width = lmax + rmax
  height = hmax

  for (i=0; i<N; i++) {
    xoffset = lmax - x[i]
    system(sprintf("convert -size %dx%d xc:White t_%03d.png -geometry +%d+0 -composite t_%03dw.gif",
                   width, height, i, xoffset, i))
  }

  cmd = sprintf("convert -delay %d", delay)
  for (i=0; i<N; i++) {
    cmd = cmd sprintf(" t_%03dw.gif", i)
  }
  cmd = cmd " -loop 0 " outfile
  system(cmd)

  exit;
}
