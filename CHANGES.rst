Flask Boost Changelog
=====================

Version 0.7.5
-------------

* Fix a bug in cli.

Version 0.7.4
-------------

* Upgrade FontAwesome to 4.5.0.
* Update doc.

Version 0.7.3
-------------

* Fix encoding bug in cli.

Version 0.7.2
-------------

* Compile macro files via FIS.
* Run gulp in build command.

Version 0.7.1
-------------

* Fix a bug in action template.
* Upgrade coverage to 4.0.2.
* Update doc.

Version 0.7.0
-------------

* Fix livereload.
* Set SQLALCHEMY_TRACK_MODIFICATIONS to False.
* Update doc.

Version 0.6.4
-------------

* Fix bugs when generating project in Windows.
* Exclude useless files from package.

Version 0.6.3
-------------

* Upgrade ``Flask-SQLAlchemy`` to 2.1.
* Upgrade ``PyMySQL`` to 0.6.7.
* Upgrade ``Pillow`` to 3.0.0.
* Upgrade ``six`` to 1.10.0.
* Upgrade ``raven`` to 5.8.1.
* Upgrade ``coverage`` to 4.0.1.

Version 0.6.2
-------------

* Remove ``Flask-Uploads`` to support Python 3.x.

Version 0.6.1
-------------

* Replace ``shutil.move`` with ``shutil.copy`` to avoid crash in Windows.
* Update doc.

Version 0.6.0
-------------

* Move page stuff to ``application/pages`` dir.
* Move macro stuff to ``application/macros`` dir.
* Use Gulp_ to build macro assets in development.
* Use FIS_ to build assets in production.
* Lock package version in ``requirements.txt``.

.. _Gulp: http://gulpjs.com
.. _FIS: http://fex-team.github.io/fis-site/

Version 0.5.6
-------------

* Freeze version of packages.
* Upgrade fontaswsome to 4.4.0.
* Add jsonify decorator.

Version 0.5.5
-------------

* Update form templates.
* Update doc & clean codes & fix typos.

Version 0.5.4
-------------

* Init sentry in production.
* Update doc.
* Clean codes.

Version 0.5.3
-------------

* Add action less template file.
* Upgrade Bootstrap to 0.5.3.


Version 0.5.2
-------------

* Fix a bug when compile app.js & app.css.
* Add some actions' js & less files.
* Clean codes.
* Update doc.

Version 0.5.1
-------------

* Log errors to stderr in production mode.
* Enable Sentry only when in production and SENTRY_DSN config is not empty.
* Set db password to empty in dev config.
* Set db host to localhost in production config.
* Update doc.

Version 0.5.0
-------------

* Split ``app.css`` to ``libs.css`` and ``app.css``.
* Rename ``build/page.js`` to ``build/app.js``.
* Do not rewrite inner url starts with ``data:``.
* Upgrade jQuery to 1.11.3.
* Clean codes.

Version 0.4.18
--------------

* Create js & less file when create action with template.
* Do not create action when create controller.
* Refactor codes.

Version 0.4.17
--------------

* Quit if controller file does't exist when new action.
* Mkdir if controller template dir not exist when new action.
* Fix typo.

Version 0.4.16
--------------

* Add generate action command.
* Change command ``generate`` to ``new``
* Add generate action command.
* Add clearfix style to form-group.
* Indent html files with 4 spaces.
* Update doc.

Version 0.4.15
--------------

* Fix a bug when generate template file.

Version 0.4.14
--------------

* Generate template file when generate controller.
* Fix a route bug in controller template.
* Clean codes.

Version 0.4.13
--------------

* Use ``UglifyJS`` to compile js codes.

Version 0.4.12
--------------

* Include templates files in dist.

Version 0.4.11
--------------

* Add ``boost generate model`` command.
* Generate import statement when generating form.

Version 0.4.10
--------------

* Generate test file when generating controller.

Version 0.4.9
-------------

* Dynamic load controllers.
* Add ``boost generate controller`` command.
* Add ``boost generate form`` command.
* Update doc.

Version 0.4.8
-------------

* Update doc.
* Use glob2 instead of formic in livereload support.
* Clean requirements.txt.
* Update some codes to support Python3. (However the package ``Flask-Upload`` does't support Python3)

Version 0.4.7
-------------

* Fix a bug in requirements.txt.

Version 0.4.6
-------------

* Fix project generation logic to support Python3.
* Use PyMySQL instead of MySQL-python to support Python3.

Version 0.4.5
-------------

* Translate Chinese to English.
* Add ``g.signin`` js variable.
* Add screen sizes from Bootstrap.
* Update doc.

Version 0.4.4
-------------

* Update url rewrite logic when build assets.
* Do not rewrite url in js codes.
* Fix a bug when process absolute path in YAML file.
* Add ``g.method`` js variable.
* Fix a bug in ``timesince``.
* Add form helper ``check_url``.
* Remove useless codes and files.

Version 0.4.3
-------------

* Refactor macro's structure.
* Split component.less into macros/*.less.

Version 0.4.2
-------------

* Use jsmin instead of uglipyjs to compile js codes because of bugs from latter.

Version 0.4.1
-------------

* Exclude libs with full url.
* Add global js function ``registerContext`` to register context into global variable g.
* Extract _rewrite_relative_url function
* Rewrite relative path in js lib files.
* Use uglipyjs instead of jsmin to compile js codes.

Version 0.4.0
-------------

* Use js.yml & css.yml to declare assets.
* Now can build assets via console command ``python manage.py build_assets``.
* Fix bugs & add external paramter & better warning info for urlFor js function.
* Upgrade permission to 0.3.0.
* Upgrade bootstrap to 3.3.4.
* Rm url_prefix when register blueprints.
* Add viewport meta tag to head.
* Add absolute_url_for helper, and inject as jinja2 global.
* Add mkdir_p to helpers.
* Refactor utils.uploadsets.
* Track avatars default image.
* Update color vars in ``utils.less``.


Version 0.3.4
-------------

* Add g as global JavaScript variable.
* Add urlFor as global JavaScript function.
* Add page_vars block to inject JavaScript variables to a page.
* Move rules & permissions to jinja2 globals instead of global context.

Version 0.3.3
-------------

* Add csrf token header for Ajax request.
* Add avatar_url property to User model.
* Update filters.timesince.
* Upgrade bootstrap to 3.3.2.
* Clean codes and comments.

Version 0.3.2
-------------

* Remove Flask-Mail support.
* Upgrade font-awesome to 4.3.0.
* Remove useless configs.
* Add app.production attr.
* Remove no-margin-top css style.
* Enable Sentry only in production mode.
* Add highlight to account.signup & account.signin page.
* Fix typo.

Version 0.3.1
-------------

* Remove fab pull
* Clean codes.

Version 0.3.0
-------------

* Remove Flask-Admin support.
* Add hash to assets url.
* Log render time into HTTP header when the user is admin.

Version 0.2.0
-------------

* Add account system.

Version 0.1.7
-------------

* Now can title the project name by #{project|title}.
* Track bower components.
* Bump bootstrap version to 3.3.1, and fix jquery version to 1.11.1.
* Add a migration file for initialization.

Version 0.1.6
-------------

* Add default favicon.
* Clean requirements.txt.
* Update code example for nav highlight.
* Add page class to body tag.

Version 0.1.5
-------------

* Add ``fab pull`` command to update codes on server.
* Add ``flask_env.sh`` to set environment variables when shell runs.
* Fix some HTML bugs.
* Fix Supervisor config file bug.

Version 0.1.4
-------------

* Include ``versions`` in ``migrations`` directory.

Version 0.1.3
-------------

* Add README file.
* Bump bootstrap to 3.3.0 and font-awesome to 4.2.0.

Version 0.1.2
-------------

* Fix the page script bug.

Version 0.1.1
-------------

* Add help messages.

Version 0.1.0
-------------

* First public preview release.
