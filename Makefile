all: html css
html:
	mkdir -p views
	for p in src/pug/*.pug; do pyjade -c jinja $p -o views/${p%.pug}.html ; done
css:
	mkdir -p static/css
	for s in *.sass;do python -m scss $s -o static/css/${s%.sass}.css; done
