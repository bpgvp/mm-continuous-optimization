#
# Build this lecture (figures first) and remove all generated files.
#

SUBDIRS := figures

all: $(SUBDIRS)
	pdflatex --shell-escape L3-Separation.tex
	pdflatex --shell-escape L3-Separation.tex

clean: $(SUBDIRS)
	rm -rf auto svg-inkscape
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.rip *.fls *.fdb_latexmk *.synctex.gz *.gnuplot *.table *.bbl *.blg *.pdf _region_.* *~

$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: all clean $(SUBDIRS)
