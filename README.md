Flask-Boost
===============

Flask sample project for boosting your development.

###Development Guide

####Init project files

Click `Download ZIP` on GitHub and copy all files to your project path.

Delete `docs/`, update `README.md`, `.gitignore` and `LICENSE` as needed.

Rename folder `Flask-Bootstrap/` and `proj/` to your real project name.

Rename all the `proj` in codes to your real project name.

Copy `config/development_sample.py` to `config/development.py` and update config as needed.

####Install requirements

`cd` to project root path, run:
 
```py
virtualenv venv
. venv/bin/active
pip install -r requirements.txt
bower install
```

####Init database

Create database via console or other GUI/Web tools.

Then init tables and migration files:

```py
python manage.py createdb
python manage.py db init
```

Edit `migrations/alembic.ini` as follows:

```
[alembic]
# template used to generate migration files
file_template = %%(year)d%%(month).2d%%(day).2d%%(hour).2d%%(minute).2d%%(second).2d_%%(rev)s_%%(slug)s
```

####Livereload support

Install livereload brower extension from [here](http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-).

Run livereload server in another console:

```py
python manage.py live
```

####Run app

Run local server:

```py
python manage.py run
```

###Production Deploy

####Config server

* [Ubuntu](http://wiki.hustlzp.com/post/ubuntu-server-config)
* [CentOS 6.5](http://wiki.hustlzp.com/post/linux/centos)

####Install requirements

```
git clone ***/proj.git
cd proj
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

####Config app

Create database first.

Copy `config/production_sample.py` to `config/production.py` and update config as needed.

Then transfer `config/production.py` to server.

####Init database

Create tables:

```py
export MODE=PRODUCTION
cd proj
. venv/bin/activate
python manage.py db upgrade
```

####Start app

```
cp deploy/nginx.conf /etc/nginx/conf.d/proj.conf
cp deploy/supervisor.conf /etc/supervisord.d/proj.conf
service nginx restart
supervisorctl reread
supervisorctl update
supervisorctl start proj
```
