all: counter-example-open.pdf counter-example-proper.pdf counter-example-strict.pdf counter-example-strong.pdf separating-bounded-convex-sets.pdf separating-convex-set-from-point.pdf separating-hyperplane.pdf separating-open-set-from-convex-set.pdf separating-open-set-from-point.pdf

%.svg: %.pdf
	pdf2svg $< $@

%.pdf: %.tex
	pdflatex --shell-escape $<

clean:
	rm -rf auto
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.rip *.fls *.fdb_latexmk *.synctex.gz *.gnuplot *.table *.bbl *.blg *.pdf *.svg *~
