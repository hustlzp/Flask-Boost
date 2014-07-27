from fabric.api import run, env, cd, prefix
from proj import config


def deploy():
    env.host_string = config.HOST_STRING
    with cd('/var/www/proj'):
        run('git pull')
        run('bower install')
        with prefix('source venv/bin/activate'):
            run('pip install -r requirements.txt')
        run('sudo supervisorctl restart proj')


def restart():
    env.host_string = config.HOST_STRING
    run('sudo supervisorctl restart proj')