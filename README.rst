PyCon SK and Slovak Python User Group Website
#############################################

PyCon SK website, build in Flask from which static HTML is generated.


Installation
------------

- clone repository locally::

	git clone git@github.com:pyconsk/pycon.sk.git
	cd pycon.sk/source

- run initialization script (creates virtualenvs and install requirements)::

	make init

- activate virtual environments::

	source envs/bin/activate

- start flask server, and you can view it in browser (http://127.0.0.1:5000)::

	python views.py


Translations
------------

- collect messages for translation::

	make messages

- files that needs to be translated are generated into directory::

	translations/

- compiling translated messages::

	make compile


Static site generation
----------------------

- generating staging site::

	make staging

- start local webserver, and you can view it in browser (http://127.0.0.1:5000)::

	python -m SimpleHTTPServer 5000

- update live site from code in staging site:

	make live

If you find some bug please do report it, or send us merge request with fix, thanks.

Links
-----

- web: https://pycon.sk
- facebook: https://facebook.com/pyconsk
- twitter: https://twitter.com/pyconsk
- slack: https://pyconsk.slack.com

