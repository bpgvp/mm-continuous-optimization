#
# Make all the tikz figures
#

SUBDIRS := figures

all: $(SUBDIRS)
	pdflatex --shell-escape L1-Introduction.tex
	pdflatex --shell-escape L1-Introduction.tex

clean: $(SUBDIRS)
	rm -rf *.aux *.csv *.log *.pdf *.svg *.out *.nav *.toc *.rip *.vrb *.snm

$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(SUBDIRS)
