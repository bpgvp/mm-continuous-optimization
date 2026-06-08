all: affine-hull.pdf affine-hull-2d.pdf

%.svg: %.pdf
	pdf2svg $< $@

%.pdf: %.tex
	pdflatex $<

clean:
	rm -rf *.aux *.csv *.log *.pdf *.svg *.out *.synctex.gz *.toc
