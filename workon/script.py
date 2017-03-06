#!/usr/bin/env python
import os
import sys

import fire
import six

from peewee import IntegrityError

from workon.database import db_path, setup, Project


class WorkOn(object):
    _ERROR_PATH_NOT_ABSOLUTE = 'Project path must be absolute'
    _ERROR_PATH_DOESNT_EXISTS = '{0} doesn\'t exists on this machine'
    _ERROR_PATH_NOT_A_DIR = '{0} is not a dir'
    _ERROR_PROJECT_EXISTS = 'Project already exists :: {0} -> {1}'
    _SUCCESS_PROJECT_ADDED = 'Project {0} added! Now you can go to it with: `work on {0}`'
    _PROJECT_ITEM = '{} >> {}'

    # color format from: http://stackoverflow.com/a/34443116/1676861
    def _print(self, text, color=None, **kwargs):
        """print text with given color to terminal
        """
        COLORS = {
            'red': '\033[91m{}\033[00m',
            'green': '\033[92m{}\033[00m',
            'yellow': '\033[93m{}\033[00m',
            'cyan': '\033[96m{}\033[00m'
        }
        _ = COLORS[color]
        six.print_(_.format(text), **kwargs)

    def _is_unique(self, name, path):
        """verify if there is a project with given name or path
        on the database
        """
        project = None
        try:
            project = Project.select().where(
                (Project.name == name) |
                (Project.path == path)
            )[0]
        except:
            pass

        return project is None

    def _path_is_valid(self, path):
        """validates if a given path is:
        - absolute,
        - exists on current machine
        - is a directory
        """
        VALIDATORS = [
            (os.path.isabs, self._ERROR_PATH_NOT_ABSOLUTE),
            (os.path.exists, self._ERROR_PATH_DOESNT_EXISTS),
            (os.path.isdir, self._ERROR_PATH_NOT_A_DIR),
        ]

        for validator in VALIDATORS:
            func, str_err = validator
            if not func(path):
                self._print(str_err.format(path), 'red')
                return
        return True

    def _get_project_by_name(self, name):
        try:
            return Project.get(Project.name == name)
        except:
            self._print('Project "{0}" doesn\'t exist.'.format(name), 'red')
            self._print('You can add it running: work add {0}'.format(name), 'cyan')
            return None

    def add(self, name, path=None, **kwargs):
        """add new project with given name and path to database
        if the path is not given, current working directory will be taken
        ...as default
        """
        path = path or kwargs.pop('default_path', None)

        if not self._path_is_valid(path):
            return

        if not self._is_unique(name, path):
            p = Project.select().where(
                (Project.name == name) |
                (Project.path == path)
            )[0]
            self._print(self._ERROR_PROJECT_EXISTS.format(name, p.path), 'red')
            return

        Project.create(name=name, path=path)
        self._print(self._SUCCESS_PROJECT_ADDED.format(name), 'green')

    def list(self, **kwargs):
        """displays all projects on database
        """
        projects = Project.select().order_by(Project.name)
        if len(projects) == 0:
            self._print('No projects available', 'yellow')
            return

        for project in projects:
            project_repr = self._PROJECT_ITEM.format(project.name, project.path)
            row = '- {}'.format(self._PROJECT_ITEM.format(project.name, project.path))
            six.print_(row)

    def on(self, name, **kwargs):
        project = self._get_project_by_name(name)
        if not project:
            return
        sys.stdout.write(project.path)

    def rm(self, name, **kwargs):
        project = self._get_project_by_name(name)
        if not project:
            return

        project.delete_instance()
        self._print('Project {} deleted'.format(name), 'green')

    def reset(self, **kwargs):
        Project.delete().execute()
        self._print('All projects have been deleted', 'green')


def main():
    if not os.path.exists(db_path):
        setup()
    fire.Fire(WorkOn)

if __name__ == '__main__':
    main()
