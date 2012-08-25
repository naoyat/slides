all: t_anim/t_anim.gif rbt_anim/rbt_anim.gif

util/topcenter: util/topcenter.c
	cd util ; make topcenter ; cd ..

t_anim/t_anim.gif: util/topcenter
	cd t_anim ; make t_anim.gif ; cd ..

rbt_anim/rbt_anim.gif: util/topcenter
	cd rbt_anim ; make rbt_anim.gif ; cd ..

clean:
	cd util ; make clean ; cd ..
	cd t_anim ; make clean ; cd ..
	cd rbt_anim ; make clean ; cd ..
