BEGIN {
  N = maxnum+1
  delay = 33
  outfile = sprintf("rbt_anim_%s_%d.gif", mode, maxnum)

  lmax = 0
  rmax = 0
  hmax = 0
  for (i=0; i<N; i++) {
    system(sprintf("convert rbt_%s_%03d.png rbt_%03d.bmp", mode, i, i))
    cmd = sprintf("../util/topcenter rbt_%03d.bmp", i)
    cmd | getline
    if ($3 < 0) $3 = 0
    if ($4 < 0) $4 = 0
    w[i] = $1; h[i] = $2; x[i] = $3; y[i] = $4;
    if ($3 > lmax) lmax = $3;
    if ($1 - $3 > rmax) rmax = $1 - $3
    if ($2 > hmax) hmax = $2
    close(cmd)
    system(sprintf("rm -f rbt_%03d.bmp", i))
  }

  width = lmax + rmax
  height = hmax

  for (i=0; i<N; i++) {
    xoffset = lmax - x[i]
    system(sprintf("convert -size %dx%d xc:White rbt_%s_%03d.png -geometry +%d+0 -composite rbt_%s_%03dw.gif",
                   width, height, mode, i, xoffset, mode, i))
  }

  cmd = sprintf("convert -delay %d", delay)
  for (i=0; i<N; i++) {
    cmd = cmd sprintf(" rbt_%s_%03dw.gif", mode, i)
  }
  cmd = cmd " -loop 0 " outfile
  system(cmd)

  exit;
}
