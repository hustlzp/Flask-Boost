from fabric.api import run, env, cd, prefix
from config import load_config

config = load_config()
host_string = config.HOST_STRING


def deploy():
    env.host_string = config.HOST_STRING
    with cd('/var/www/proj'):
        run('git reset --hard HEAD')
        run('git pull')
        run('bower install')
        with prefix('source venv/bin/activate'):
            run('pip install -r requirements.txt')
            run('python manage.py db upgrade')
        run('sudo supervisorctl restart proj')


def restart():
    env.host_string = config.HOST_STRING
    run('sudo supervisorctl restart proj')