PyCon SK 2016 and Slovak Python User Group Website
##################################################

PyCon SK 2016 website, built with Flask from which static HTML is generated.

At the end of 2019 site generation was migrated to use Python3 by default. Other  major change was to update generation scripts no longer use 3 branches. Instead we generate to `/docs` folder to support GitHub pages.

Contributing
------------

Conference is already over, there is no development in this repo. Its main purpose is archive. If you want to contribute, check out our other repositories.


Project structure
-----------------

**3 branches**:

- ``master`` - the Flask app, templates, static files, translations (make your changes in the ``src`` folder)
- ``staging`` - static HTML, generated from the app in ``master`` branch (do NOT edit anything in here - NO LONGER USED!)
- ``live`` - static HTML, created by pushing the ``staging`` branch into ``live`` branch (do NOT edit anything in here - NO LONGER USED!)


Installation
------------

- clone repository locally::

    git clone https://github.com/pyconsk/2016.pycon.sk.git
    cd pycon.sk

- run initialization script (creates a virtual environment and installs all requirements)::

    make init

- activate virtual environments::

    source envs3/bin/activate

- start flask server, and you can view it in browser (http://127.0.0.1:5000)::

    python src/views.py


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

- generate into `/docs` folder static site::

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
- SPy o.z.: https://spyoz.eu/

License
-------

MIT license for code (GitHub repo), CC-BY for content, except sponsors logo's (consult with particular comapny if you would like to use their logo). For more detail read the LICENSE file
