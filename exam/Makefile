#
# Makefile til projektet
# Kræver latexmk og ca. hele texlive-distributionen
#


# Navn på masterfil
TARGET=aalborgtheme
WORKTARGET=worksheet

# Alle DIA-diagrammer
FIGS_DIA=

# Alle SVG-filer
#FIGS_SVG=
# Alle EPS-filer (PS-illustrationer angivet i linien nedenunder)
#FIGS_EPS= \

# Alle PDF-filer
FIGS_PDF= 

# Alle JPEG-filer, kun endelsen jpeg genkendes. Kræver jpeg2ps,
# http://www.pdflib.com/download/free-software/jpeg2ps/
FIGS_JPEG=

# Initialisering til figurkonvertering
FIGS_EPS_GEN=$(FIGS_DIA:.dia=.eps) $(FIGS_PDF:.pdf=.eps) $(FIGS_JPEG:.jpeg=.eps) $(FIGS_SVG:.svg=.eps)
FIGS_PDF_GEN=$(FIGS_DIA:.dia=.pdf) $(FIGS_EPS:.eps=.pdf) $(FIGS_SVG:.svg=.pdf)


.SUFFIXES: .dia .eps .pdf .jpeg .svg .ps

debug:	$(FIGS_PDF_GEN)
	latexmk -pdf $(TARGET)

final:	$(FIGS_PDF_GEN)
	latexmk -pdf $(TARGET)
	latexmk -c
	rm -f $(TARGET).lox
	rm -f $(TARGET).out
	rm -f */*.aux
	rm -f */*.bak
	rm -f $(FIGS_EPS_GEN)
	rm -f $(FIGS_PDF_GEN)

dvi:	$(FIGS_EPS_GEN)
	latexmk $(TARGET)

ps:	$(FIGS_EPS_GEN)
	latexmk -ps $(TARGET)

pdf:	$(FIGS_PDF_GEN)

worksheet: arbejdsblad

arbejdsblad:	debug
	latexmk -pdf $(WORKTARGET)
	latexmk -c
	rm -f $(WORKTARGET).lox
	rm -f $(WORKTARGET).out
	rm -f */*.aux
	rm -f */*.bak
	rm -f $(FIGS_EPS_GEN)
	rm -f $(FIGS_PDF_GEN)

blazingfast:	$(FIGS_PDF_GEN)
	latexmk -pdf -silent $(TARGET)

clean:
	latexmk -C
	rm -f $(TARGET).lox
	rm -f $(TARGET).out
	rm -f */*.aux
	rm -f */*.bak
	rm -f $(FIGS_EPS_GEN)
	rm -f $(FIGS_PDF_GEN)
	rm -f illustrations/*.pdf_tex
	rm -f *.maf
	rm -f *.mtc*

cleanex:
	latexmk -C
	rm -f $(TARGET).lox
	rm -f $(TARGET).out
	rm -f */*.aux
	rm -f */*.bak

live:
	latexmk -pvc -pdf -quiet $(TARGET).tex

raw:
	pdflatex $(TARGET)
	bibtex $(TARGET)
	pdflatex $(TARGET)
	pdflatex $(TARGET)


#compiling simulating the time spend using Brians computer.

brian:	$(FIGS_PDF_GEN)
	sleep 30
	latexmk -pdf $(TARGET)

# Konvertering mellem forskellige formater

# fx dia -t eps -e target.eps target.dia
.dia.eps:
	dia -t eps -e $@ $<

# fx jpeg2ps target.jpeg > target.eps
.jpeg.eps:
	jpeg2ps $< > $@

# fx inkscape --export-eps=target.eps --export-text-to-path target.svg
.svg.eps:
	inkscape --export-eps=$@ --export-text-to-path $<

# fx inkscape --export-pdf=target.pdf --export-text-to-path target.svg
.svg.pdf:
#	inkscape -D -z --export-pdf=$@ --export-latex $<
	inkscape -D -z --export-pdf=$@ $<

# fx epstopdf target.eps
#.eps.pdf:
#	epstopdf --outfile=$@ $<

# fx pdftops -eps target.pdf
#.pdf.eps:
#	pdftops -eps $< $@
