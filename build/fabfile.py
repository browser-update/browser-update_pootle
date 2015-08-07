from fabric import api as fab
from functools import wraps
import os, re


#########################################################################################################
# Init / Settings

# Set the working directory to the build/ directory. This is necessary if you
# run "fab ..." in a subdirectory or with "fab ... -f build/fabfile.py"
BUILD_PATH = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
os.chdir(BUILD_PATH)


#########################################################################################################
# Utils

def _env_path():
    return os.path.realpath(os.path.join(BUILD_PATH, '..', 'env'))


def _env_bin(executable):
    return os.path.join(_env_path(), 'bin', executable)


def _env_choose_bin(*executables):
    for executable in executables:
        path = _env_bin(executable)
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    raise ValueError(
        'There is none of the given executables available in the '
        'virtualenv: {0}.'.format(', '.join(executables)))


def _env_python_bin():
    return _env_choose_bin('python2', 'python')


def _env_pip_bin():
    return _env_choose_bin('pip2', 'pip')


#########################################################################################################
# Tasks


# Setup / Install

@fab.task
def env():
    fab.local('virtualenv2 %s' % _env_path())


@fab.task
def install():
    fab.local('%s install -Ur PYTHON_REQUIREMENTS' % _env_pip_bin())


@fab.task
def freeze():
    fab.local('%s freeze -r PYTHON_REQUIREMENTS > PYTHON_REQUIREMENTS.new' % _env_pip_bin())
    fab.local('mv -f PYTHON_REQUIREMENTS.new PYTHON_REQUIREMENTS')


@fab.task
def setup():
    fab.execute(env)
    fab.execute(install)


# Deployment

def _deploy_git_factory():
    import fabdeploit

    class Git(fabdeploit.Git):
        local_repository_path = os.path.dirname(BUILD_PATH)
        # remote_repository_path = None
        release_author = 'Team23 GmbH & Co. KG <info@team23.de>'
        # release_branch = None

    return Git


def _deploy_virtualenv_factory(_git):
    import fabdeploit

    class Virtualenv(fabdeploit.Virtualenv2):
        python_commands = ('python2.7',) + fabdeploit.Virtualenv2.python_commands
        pip_commands = ('pip2.7',) + fabdeploit.Virtualenv2.pip_commands
        virtualenv_commands = ('virtualenv2.7',) + fabdeploit.Virtualenv2.virtualenv_commands

        virtualenv_path = '%s/env' % _git.remote_repository_path
        requirements_file = '%s/build/PYTHON_REQUIREMENTS' % _git.remote_repository_path

    return Virtualenv


def _deploy_pootle_factory(_git):
    from fabdeploit.base import BaseCommandUtil

    class Pootle(BaseCommandUtil):
        settings_path = '%s/web/bu_pootle/settings.py' % _git.remote_repository_path

        def __init__(self, virtualenv, **kwargs):
            self.virtualenv = virtualenv
            super(Pootle, self).__init__(**kwargs)
            if self.settings_path is None:
                raise RuntimeError('No settings_path specified (class or constructor)')

        def run(self, command, *options):
            self._run("%s %s %s %s" % (
                self.virtualenv.select_bin('pootle'),
                '--config="%s"' % self.settings_path,
                command,
                ' '.join([o for o in options if not o is None]),
            ))

        def migrate(self, app=None, migration=None, database=None, fake=False, merge=False):
            self.run(
                'migrate',
                '--noinput',
                '--merge' if merge else None,
                '--database="%s"' % database if database else None,
                '--fake' if fake else None,
                app if app else None,
                migration if migration else None,
            )

        def initdb(self):
            self.run(
                'initdb',
            )

        def createsuperuser(self):
            self.run(
                'createsuperuser',
            )

    return Pootle


def _deploy_base_env():
    fab.require('git')

    fab.env.use_ssh_config = True
    fab.env.hosts = ['wmp.barbel']

    fab.env.virtualenv = _deploy_virtualenv_factory(fab.env.git)()
    fab.env.pootle = _deploy_pootle_factory(fab.env.git)(fab.env.virtualenv)


@fab.task
def barbel():
    fab.env.git = _deploy_git_factory()(
        remote_repository_path='/var/www/localhost/users/wmp/bu_pootle',
        release_branch='master',
    )

    _deploy_base_env()


@fab.task
def deploy_push_files():
    fab.require('git')

    fab.env.git.pull()
    fab.env.git.create_release_commit()
    fab.env.git.push()


@fab.task
def deploy_apply_files():
    fab.require('git')

    fab.env.git.switch_release()


@fab.task
def deploy_virtualenv_files(force=False):
    fab.require('virtualenv')

    fab.env.virtualenv.init(force=force)
    fab.env.virtualenv.update()


@fab.task
def deploy_files():
    fab.execute(deploy_push_files)
    fab.execute(deploy_apply_files)
    fab.execute(deploy_virtualenv_files)


@fab.task
def deploy_migrate():
    fab.require('pootle')

    fab.env.pootle.migrate()


@fab.task
def deploy_stop():
    #fab.run('%s stop' % fab.env.deploy_initscript)
    pass


@fab.task
def deploy_start():
    #fab.run('%s start' % fab.env.deploy_initscript)
    pass


@fab.task
def deploy_restart():
    #fab.run('%s restart' % fab.env.deploy_initscript)
    pass


@fab.task
def deploy(*args):
    fab.require('git')

    # prepare
    fab.execute(deploy_push_files)
    # The 'git status' is done so the virtualenv.create_commit later will not need to
    # scan all files first. Scanning files may be bad for performance and we want to
    # keep the downtime to a minimum.
    if 'virtualenv' in fab.env and fab.env.virtualenv.virtualenv_path:
        with fab.cd(fab.env.virtualenv.virtualenv_path):
            fab.run('git status')
    with fab.cd(fab.env.git.remote_repository_path):
        fab.run('git status')
    fab.execute(deploy_stop)

    # run upgrade
    fab.execute(deploy_apply_files)
    if not 'novirtualenv' in args:
        fab.execute(deploy_virtualenv_files)
    if not 'nomigrate' in args:
        fab.execute(deploy_migrate)

    # start server again
    fab.execute(deploy_start)


@fab.task
def deploy_setup(*args):
    import posixpath

    fab.execute(deploy_push_files)
    fab.execute(deploy_apply_files)
    fab.execute(deploy_virtualenv_files)
    with fab.cd(posixpath.join(fab.env.git.remote_repository_path, 'web', 'bu_pootle')):
        fab.run('cp local_settings.example.py local_settings.py')
        print '*' * 79
        print 'Now edit local_settings.py to fit your needs, press enter when ready!'
        print '*' * 79
        fab.run('read')
    fab.env.pootle.migrate()
    fab.env.pootle.initdb()
    fab.env.pootle.createsuperuser()
