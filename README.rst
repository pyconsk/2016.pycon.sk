PyCon SK and Slovak Python User Group Website
#############################################

PyCon SK website, built with Flask from which static HTML is generated.


Project structure
-----------------

3 folders:

* ``source`` - the Flask app, templates, static files, translations (make your changes here)
* ``staging`` - static HTML, generated from the ``source`` (do NOT edit anything in here)
* ``live`` - static HTML, created by copying the ``staging`` folder (do NOT edit anything in here)


Installation
------------

- clone repository locally::

	git clone git@github.com:pyconsk/pycon.sk.git
	cd pycon.sk/source

- run initialization script (creates a virtual environment and installs all requirements)::

	make init

- activate virtual environments::

	source envs/bin/activate

- start flask server, and you can view it in browser (http://127.0.0.1:5000)::

	python views.py


Translations
------------

- collect messages for translation::

	make messages

- files that need to be translated are generated into directory::

	translations/

- compiling translated messages::

	make compile


Static site
-----------

- generating staging site::

	make staging

- start local webserver, and you can view it in browser (http://127.0.0.1:5000)::

	python -m SimpleHTTPServer 5000

- update live site from code in staging site::

	make live

If you find some bug please do report it, or send us a merge request with a fix, thanks.

Links
-----

- web: https://pycon.sk
- facebook: https://facebook.com/pyconsk
- twitter: https://twitter.com/pyconsk
- slack: https://pyconsk.slack.com

