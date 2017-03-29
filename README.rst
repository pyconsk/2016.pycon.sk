PyCon SK 2016 and Slovak Python User Group Website
##################################################

PyCon SK 2016 website, built with Flask from which static HTML is generated.


Contributing
------------

Conference is already over, there is no development in this repo. Its main purpose is archive. If you want to contribute, check out our other repositories.


Project structure
-----------------

**3 branches**:

- ``master`` - the Flask app, templates, static files, translations (make your changes in the ``src`` folder)
- ``staging`` - static HTML, generated from the app in ``master`` branch (do NOT edit anything in here)
- ``live`` - static HTML, created by pushing the ``staging`` branch into ``live`` branch (do NOT edit anything in here)


Installation
------------

- clone repository locally::

    git clone https://github.com/pyconsk/2016.pycon.sk.git
    cd pycon.sk

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

- generating staging site (updates the staging branch)::

    make staging

- update live site by pushing staging branch into the live branch::

    make live


Pull & Push
-----------

- update all branches from remote repository::

    make pull

- push all branches to remote repository::

    make push


If you find some bug please do report it, or send us a merge request with a fix, thanks.


Links
-----

- web: https://2016.pycon.sk
- facebook: https://facebook.com/pyconsk
- twitter: https://twitter.com/pyconsk

