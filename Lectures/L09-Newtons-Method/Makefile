#
# Build this lecture and remove all generated files.
#

all:
	pdflatex --shell-escape L9-Newtons-Method.tex
	pdflatex --shell-escape L9-Newtons-Method.tex

clean:
	rm -rf auto svg-inkscape
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.rip *.fls *.fdb_latexmk *.synctex.gz *.gnuplot *.table *.bbl *.blg *.pdf _region_.* *~

.PHONY: all clean
