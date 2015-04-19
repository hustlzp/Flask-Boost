Flask-Boost
===========

.. image:: http://img.shields.io/pypi/v/flask-boost.svg
   :target: https://pypi.python.org/pypi/flask-boost
   :alt: Latest Version
.. image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/hustlzp/Flask-Boost/blob/master/LICENSE
   :alt: The MIT License

Flask application generator for boosting your development.

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

Init database
~~~~~~~~~~~~~

Create database with name ``your_project_name``.

Update ``SQLALCHEMY_DATABASE_URI`` in ``config/development.py`` as needed.

Then init tables::

    python manage.py db upgrade

Run app
~~~~~~~

Run local server::

    python manage.py run

LiveReload support
~~~~~~~~~~~~~~~~~~

Install livereload brower extension from here_.

Run livereload server in another console::

    python manage.py live

.. _here: http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-

First Production Deploy
-----------------------

Config server
~~~~~~~~~~~~~

Install virtualenv, git, supervisor and g++ on your server.

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

Update configs ``config/production.py`` as needed and transfer it to server.

Init database
~~~~~~~~~~~~~

Create database with name ``your_project_name``.

And run::

    export MODE=PRODUCTION
    python manage.py db upgrade

Build assets
~~~~~~~~~~~~

::

    python manage.py build_assets

Copy config files
~~~~~~~~~~~~~~~~~

::

    cp deploy/flask_env.sh /etc/profile.d/
    cp deploy/nginx.conf /etc/nginx/conf.d/{your_project_name}.conf
    cp deploy/supervisor.conf /etc/supervisord.d/{your_project_name}.conf

Start app
~~~~~~~~~

::

    service nginx restart
    service supervisord restart

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
