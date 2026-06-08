all: wolfe-condition.pdf

%.svg: %.pdf
	pdf2svg $< $@

%.pdf: %.tex
	pdflatex --shell-escape $<

clean:
	rm -rf auto
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.rip *.fls *.fdb_latexmk *.synctex.gz *.gnuplot *.table *.bbl *.blg *.pdf *.svg *~
