all: sdo-cone.pdf

%.svg: %.pdf
	pdf2svg $< $@

%.pdf: %.tex
	pdflatex $<

clean:
	rm -rf *.aux *.log *.pdf *.svg *.out *.synctex.gz *.toc *.table *.gnuplot
