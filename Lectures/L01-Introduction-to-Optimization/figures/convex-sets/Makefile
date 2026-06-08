all: convex-sets-I.pdf convex-sets-II.pdf convex-sets-III.pdf convex-sets-IV.pdf

%.svg: %.pdf
	pdf2svg $< $@

%.pdf: %.tex
	pdflatex $<

clean:
	rm -rf *.aux *.csv *.log *.pdf *.svg *.out
