#
# Build all lecture slides. Each goal is delegated to the per-lecture
# Makefiles under Lectures/, which build the figures and slides and clean
# up all generated (non-committed) files.
#

TOPTARGETS := all clean

SUBDIRS := Lectures

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS)
