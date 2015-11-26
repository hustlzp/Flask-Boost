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

Installation
------------

::

    pip install flask-boost

or install the latest version from GitHub::

    pip install git+https://github.com/hustlzp/Flask-Boost.git#egg=flask_boost

**ATTENTION**: Breaking changes have been made in 0.6.x, use the command below if you want to install the 0.5.x version::

    pip install flask-boost==0.5.6

Development Guide
-----------------

Init project
~~~~~~~~~~~~

::

    boost new <your_project_name>

Setup backend requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

``cd`` to project root path, run:
 
::

    virtualenv venv
    . venv/bin/activate (venv\Scripts\activate in Windows)
    pip install -r requirements.txt

**Note**: if you failed in ``pip install -r requirements.txt`` in Windows, try to install package binaries directly.
**Note**: if you meet error installing pycrpyto in windows,try follow this article compiling-pycrypto-on-win7-64_ ,
or get the complied pycrypyto library directly: archive_pycrpyto_library_

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
    npm install gulp

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

In ``Preferences -> Project -> Project Interpreter``, set ``venv`` as project interpreter.

In ``Preferences -> Project -> Project Structure``, set ``application/pages`` and ``application/macros`` as template folders,
set ``application`` and ``application/static/css`` as resource folders.

In ``Language & Frameworks -> JavaScript -> Bower``, set ``bower.json`` as bower.json.

Recommended plugins:

* .ignore
* Markdown
* Bootstrap3

.. _PyCharm: https://www.jetbrains.com/pycharm/

First Production Deploy
-----------------------

Config server
~~~~~~~~~~~~~

Install virtualenv, git, supervisor, nginx and g++ on your server.

**Note**: Flask-Boost uses Pillow to process images, so you may install some external libraries needed by `Pillow`. Please follow the Pillow official doc_.

.. _doc: http://pillow.readthedocs.org/en/latest/installation.html

Install requirements
~~~~~~~~~~~~~~~~~~~~

::

    git clone **.git
    cd proj
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

Config app
~~~~~~~~~~

Update configs in ``config/production.py`` as needed and transfer it to server.

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

for CentOS 7:

::

    systemctl start nginx.service
    systemctl start supervisord.service


Daily Production Deploy
-----------------------

Update ``HOST_STRING`` in config with the format ``user@ip``.

Commit your codes and run::

    git push && fab deploy

License
-------

The MIT License (MIT)

Copyright (c) 2015 hustlzp

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
