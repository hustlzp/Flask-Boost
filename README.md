Flask-Boost
===============

Flask sample project for boosting your development.

###Development

####Clean up project files

Delete `docs/`, update `README.md` and `LICENSE` as needed.

Rename folder `Flask-Bootstrap/` and `proj/` to your real project name.

Rename all the `proj` in codes to your real project name.

####Install requirements

`cd` to project root path, run:
 
```py
virtualenv venv
. venv/bin/active
pip install -r requirements.txt
```

####Init database

Create database and then init tables:

```py
python manage.py createdb
```

Create database migration files:

```py
python manage.py db init
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

####Install requirements

```
pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

####Copy config files

```
cp deploy/nginx.conf /etc/nginx/conf.d/proj.conf
cp deploy/supervisor.conf /etc/supervisor.d/proj.conf
```

####Start app

```
supervisorctl reread
supervisorctl update
supervisorctl start proj
```
