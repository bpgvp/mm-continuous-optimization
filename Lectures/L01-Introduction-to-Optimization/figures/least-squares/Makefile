all: least-squares.pdf

%.svg: %.pdf
	pdf2svg $< $@

%.pdf: %.tex
	pdflatex $<

clean:
	rm -rf *.aux *.csv *.log *.pdf *.svg *.out
