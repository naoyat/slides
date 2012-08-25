MAXNUM = 30

all: t_anim.gif

t_gen: t_gen.cc
	g++ -O2 -o $@ $<

t_000.dot: t_gen
	./t_gen rand $(MAXNUM)

t_000.png: t_000.dot
	for f in t_*.dot ; do dot -Tpng "$$f" -o `basename $$f .dot`.png ; done

t_anim.gif: t_000.png t_anim_gen.awk ../util/topcenter
	awk -v maxnum=$(MAXNUM) -f t_anim_gen.awk

clean:
	rm -f t_gen t_*.dot t_*.png t_*.gif
	rm -f t_gen t_anim.gif *~

