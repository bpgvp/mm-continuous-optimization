#
# Make the all the tikz figures
#

TOPTARGETS := all clean

SUBDIRS := Lectures

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS)
