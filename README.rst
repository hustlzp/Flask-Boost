Flask-Boost
===========

.. image:: http://img.shields.io/pypi/v/flask-boost.svg
   :target: https://pypi.python.org/pypi/flask-boost
   :alt: Latest Version
.. image:: http://img.shields.io/pypi/dm/flask-boost.svg
   :target: https://pypi.python.org/pypi/flask-boost
   :alt: Downloads Per Month
.. image:: http://img.shields.io/pypi/pyversions/flask-boost.svg
   :target: https://pypi.python.org/pypi/flask-boost
   :alt: Python Versions
.. image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/hustlzp/Flask-Boost/blob/master/LICENSE
   :alt: The MIT License

Flask application generator for boosting your development.

Features
--------

* **Well Defined Project Structure**

  * Use factory pattern to generate Flask app.
  * Use Blueprints to organize controllers.
  * Split controllers, models, forms, utilities, assets, Jinja2 pages, Jinja2 macros into different directories.
  * Organize Jinja2 page assets (HTML, JavaScript, CSS) to the same directory.
  * Organize Jinja2 macro assets (HTML, JavaScript, CSS) to the same directory.

* **Batteries Included**

  * Use Flask-SQLAlchemy and Flask-Migrate as database tools.
  * Use Flask-WTF to validate forms.
  * Use Flask-Script to help writing scripts.
  * Use permission_ to define permissions.
  * Use Bootstrap as frontend framework.
  * Use Bower to manage frontend packages.
  * Use Gulp and FIS_ to compile static assets.
  * Use Gunicorn to run Flask app and Supervisor to manage Gunicorn processes.
  * Use Fabric as deployment tool.
  * Use Sentry to log exceptions.
  * Use Nginx to serve static files.

* **Scaffold Commands**

  * Generate project files: ``boost new <project>``
  * Generate controller files: ``boost new controller <controller>``
  * Generate action files: ``boost new action <controller> <action> [-t]``
  * Generate form files: ``boost new form <form>``
  * Generate model files: ``boost new model <model>``
  * Generate macro files: ``boost new macro <category> <macro>`` or ``boost new macro <macro>``

.. _permission: https://github.com/hustlzp/permission

Installation
------------

::

    pip install flask-boost

Development Guide
-----------------

Init project
~~~~~~~~~~~~

::

    boost new <your_project_name>

Setup backend requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~
 
::

    cd <your_project_dir>
    virtualenv venv
    . venv/bin/activate (venv\Scripts\activate in Windows)
    pip install -r requirements.txt

**Note**: if you failed in ``pip install -r requirements.txt`` in Windows, try to install package binaries directly:

* pycrpyto: try to follow this article compiling-pycrypto-on-win7-64_, or get the complied pycrypyto library directly: archive_pycrpyto_library_.

.. _compiling-pycrypto-on-win7-64: https://yorickdowne.wordpress.com/2010/12/22/compiling-pycrypto-on-win7-64/
.. _archive_pycrpyto_library: http://archive.warshaft.com/pycrypto-2.3.1.win7x64-py2.7x64.7z

Init database
~~~~~~~~~~~~~

Create database with name ``your_project_name`` and encoding ``utf8``.

Update ``SQLALCHEMY_DATABASE_URI`` in ``config/development.py`` as needed.

Then init tables::

    python manage.py db upgrade

Run app
~~~~~~~

Run local server::

    python manage.py run

Setup frontend requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install Node.js first and then install Bower_, FIS_ and Gulp_ globally::

    npm install -g bower
    npm install -g fis
    npm install -g fis-postpackager-simple
    npm install -g gulp

Install local packages::

    npm install
    bower install

Run Gulp watch task
~~~~~~~~~~~~~~~~~~~

::

    gulp watch

LiveReload support
~~~~~~~~~~~~~~~~~~

Install LiveReload browser extension from here_.

And use ``python manage.py live`` instead of ``python manage.py run`` to start app.

.. _here: http://livereload.com/extensions/

Scaffold commands
~~~~~~~~~~~~~~~~~

::

    boost new <project>
    boost new controller <controller>
    boost new action <controller> <action> [-t]
    boost new form <form>
    boost new model <model>
    boost new macro <category> <macro>
    boost new macro <macro>
    boost -v
    boost -h

Recommended IDE
~~~~~~~~~~~~~~~

PyCharm_ is the recommended IDE for Flask-Boost.

Recommended preferences:

* In ``Preferences -> Project -> Project Interpreter``, set ``venv`` as project interpreter.
* In ``Preferences -> Project -> Project Structure``, set ``application/pages`` and ``application/macros`` as template folders, set ``application`` and ``application/static/css`` as resource folders.
* In ``Language & Frameworks -> JavaScript -> Bower``, set ``bower.json`` as bower.json.

Recommended PyCharm plugins:

* .ignore
* Markdown
* Bootstrap3

.. _PyCharm: https://www.jetbrains.com/pycharm/

First Production Deploy
-----------------------

Config server
~~~~~~~~~~~~~

Install mysql-server, python-virtualenv, git, supervisor, nginx, g++, python-dev, libmysqlclient-dev, libxml2-dev, libxslt-dev on your server.

Install requirements
~~~~~~~~~~~~~~~~~~~~

::

    git clone **.git
    cd <your_project_dir>
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

Config app
~~~~~~~~~~

Save ``config/production_sample.py`` as ``config/production.py``, update configs in ``config/production.py`` as needed and transfer it to server.

**Note**: remember to update ``SECRET_KEY`` in ``config/production.py``! You can generate random secret key as follows::

>>> import os
>>> os.urandom(24)

Init database
~~~~~~~~~~~~~

Create database with name ``your_project_name`` and encoding ``utf8``.

And run::

    export MODE=PRODUCTION
    python manage.py db upgrade

Copy config files
~~~~~~~~~~~~~~~~~

Update project root path as needed in ``deploy/nginx.conf`` and ``deploy/supervisor.conf``.

::

    cp deploy/flask_env.sh /etc/profile.d/
    cp deploy/nginx.conf /etc/nginx/conf.d/<your_project_name>.conf
    cp deploy/supervisor.conf /etc/supervisor/conf.d/<your_project_name>.conf

Build assets
~~~~~~~~~~~~

Install Node.js first and then install Bower_, FIS_ and Gulp_ globally::

    npm install -g bower
    npm install -g fis
    npm install -g fis-postpackager-simple
    npm install -g gulp

Install local packages::

    npm install
    bower install

Then::

    gulp
    python manage.py build

.. _Bower: http://bower.io
.. _FIS: http://fex-team.github.io/fis-site/
.. _Gulp: http://gulpjs.com

Start app
~~~~~~~~~

::

    service nginx restart
    service supervisor restart

Daily Production Deploy
-----------------------

Update ``HOST_STRING`` in config with the format ``user@ip``.

Commit your codes and run::

    git push && fab deploy

P.S. If you wanna to deploy flask with Apache2, see this_ post.

.. _this: https://www.digitalocean.com/community/tutorials/how-to-use-apache-http-server-as-reverse-proxy-using-mod_proxy-extension

License
-------

MIT
