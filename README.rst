Flask-Boost
===========

Flask sample project for boosting your development.

Installation
------------

::

    pip install flask-boost

Development Guide
-----------------

Init project
~~~~~~~~~~~~

::

    boost new your_project_name

Install requirements
~~~~~~~~~~~~~~~~~~~~

``cd`` to project root path, run:
 
::

    virtualenv venv
    . venv/bin/active
    pip install -r requirements.txt
    bower install

Init database
~~~~~~~~~~~~~

Create database via console or other GUI/Web tools.

Update ``config/development.py`` as needed.

Then init tables::

    python manage.py createdb

Livereload support
~~~~~~~~~~~~~~~~~~

Install livereload brower extension from here_.

Run livereload server in another console::

    python manage.py live
    
.. _here: http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-
Run app
~~~~~~~

Run local server::

    python manage.py run

Production Deploy
-----------------

Config server
~~~~~~~~~~~~~

* Ubuntu_
* CentOS_

.. _Ubuntu: http://wiki.hustlzp.com/post/ubuntu-server-config
.. _CentOS: http://wiki.hustlzp.com/post/linux/centos


Install requirements
~~~~~~~~~~~~~~~~~~~~

::

    git clone ***/proj.git
    cd proj
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    bower install

Config app
~~~~~~~~~~

Create database first.

Update ``config/production.py`` as needed.

Then transfer ``config/production.py`` to server.

Init database
~~~~~~~~~~~~~

::

    export MODE=PRODUCTION
    cd proj
    . venv/bin/activate
    python manage.py createdb

Start app
~~~~~~~~~

::

    cp deploy/nginx.conf /etc/nginx/conf.d/proj.conf
    cp deploy/supervisor.conf /etc/supervisord.d/proj.conf
    service nginx restart
    service supervisord restart