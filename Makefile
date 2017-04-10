SHELL := /bin/bash
all: html css
html:
	mkdir -p views
	for p in src/pug/*.pug; do base=$$(basename $$p); pyjade -c jinja $$p -o views/$${base%.pug}.html; done

css:
	mkdir -p static/css
	for s in src/sass/*.sass; do base=$$(basename $$s); sassc $$s static/css/$${base%.sass}.css; done
