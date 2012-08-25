MAXNUM = 34

all: rbt_anim_asc_$(MAXNUM).gif

rbt_gen: rbt_gen.cc
	g++ -O2 -o $@ $<

rbt_asc_000.dot: rbt_gen
	./rbt_gen asc $(MAXNUM)
	./rbt_gen desc $(MAXNUM)
	./rbt_gen rand $(MAXNUM)

rbt_asc_000.png: rbt_asc_000.dot
	for f in rbt_*.dot ; do dot -Tpng "$$f" -o `basename $$f .dot`.png ; done

rbt_anim_asc_$(MAXNUM).gif: rbt_asc_000.png rbt_anim_gen.awk ../util/topcenter
	awk -v mode=asc -v maxnum=$(MAXNUM) -f rbt_anim_gen.awk
	awk -v mode=desc -v maxnum=$(MAXNUM) -f rbt_anim_gen.awk
	awk -v mode=rand -v maxnum=$(MAXNUM) -f rbt_anim_gen.awk

clean:
	rm -f rbt_gen rbt_*.dot rbt_*.png rbt_*.gif *~

