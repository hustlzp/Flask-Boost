Flask-Bootstrap
===============

Flask sample project for bootstrap.

`cd` to the project path, run:
 
```py
virtualenv venv
. venv/bin/active
pip install -r requirements.txt
```

Delete `docs/`, update `README.md` and `LICENSE` as needed.

Rename folder `Flask-Bootstrap/` and `proj/` to your real project name.

Rename all the `proj` in codes to your real project name.

Create database and then init tables:

```py
python manage.py createdb
```

Create database migration files:

```py
python manage.py db init
```

###Deploy

```
pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt

cp deploy/nginx.conf /etc/nginx/conf.d/proj.conf
cp deploy/supervisor.conf /etc/supervisor.d/proj.conf
```
