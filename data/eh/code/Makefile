all: \
	../input/2005_f2001 \
	../input/2006_f2001 \
	../input/2007_f2001 \
	../input/2008_f2001 \
	../input/2009_f2001 \
	../input/2011_f2001 \
	../input/2012_f2001 \
	../input/2013_f2001 \
	../input/2014_f2001 \
	../input/2011_f2014 \
	../input/2012_f2014 \
	../input/2013_f2014 \
	../input/2014_f2014 \
	../input/2015 \
	../input/2016 \
	../input/2017 \
	../input/2018

include ../../../generic.make

MAP := \
	bd22:2005_f2001 \
	bd25:2006_f2001 \
	bd26:2007_f2001 \
	bd23:2008_f2001 \
	bd24:2009_f2001 \
	bd27:2011_f2001 \
	bd28:2012_f2001 \
	bd29:2013_f2001 \
	bd30:2014_f2001 \
	bd31:2011_f2014 \
	bd32:2012_f2014 \
	bd33:2013_f2014 \
	bd34:2014_f2014 \
	bd35:2015 \
	bd39:2016 \
	bd41:2017 \
	bd43:2018

# SYMLINK RULE
../input/%.zip: ../../download/output/%.zip | ../input
	@if [ ! -e $@ ]; then ln -sf $< $@; fi

# UNZIP RULE
$(foreach m,$(MAP),\
$(eval ../input/$(word 2,$(subst :, ,$(m))): ../input/$(word 1,$(subst :, ,$(m))).zip ;\
	mkdir -p $$@ ;\
	unzip -o $$< -d $$@ ;\
))
