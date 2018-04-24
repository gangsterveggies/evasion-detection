all:
	pdflatex project.tex
	bibtex project
	pdflatex project.tex > /dev/null
	pdflatex project.tex > /dev/null
