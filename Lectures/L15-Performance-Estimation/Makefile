#
# Build this lecture and remove all generated files.
#

all:
	pdflatex --shell-escape L15-Performance-Estimation.tex
	pdflatex --shell-escape L15-Performance-Estimation.tex

clean:
	rm -rf auto svg-inkscape
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.rip *.fls *.fdb_latexmk *.synctex.gz *.gnuplot *.table *.bbl *.blg *.pdf _region_.* *~

.PHONY: all clean
