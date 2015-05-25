Flask Boost Changelog
=====================

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