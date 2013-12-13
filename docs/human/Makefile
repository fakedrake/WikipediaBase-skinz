.PHONY: force all
GRAPH=wikipediabase.ps wikipediabase.png

all: $(GRAPH)

%.ps: %.dot
	dot $^ -Tps2 -o $@

%.png: wikipediabase.dot
	dot $^ -Tpng -o $@

# diagram.pdf: diagram.ps
# 	ps2pdf  wikipediabase.ps wikipediabase.pdf

clean:
	rm -rf $(GRAPH)
