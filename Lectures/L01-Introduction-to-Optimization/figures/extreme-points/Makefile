all: extreme-points.pdf extreme-points-2.pdf

%.svg: %.pdf
	pdf2svg $< $@

%.pdf: %.tex
	pdflatex --shell-escape $<

clean:
	rm -rf *.aux *.log *.pdf *.svg *.out *.synctex.gz *.toc *.table *.gnuplot
