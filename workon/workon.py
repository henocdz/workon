#!/usr/bin/env python
import os

import fire

from peewee import IntegrityError

from database import setup, Project


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
        print(_.format(text), **kwargs)

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

    def add(self, name, path=None):
        """add new project with given name and path to database
        if the path is not given, current working directory will be taken
        ...as default
        """
        path = path or os.getcwd()

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
        self._print_success(self._SUCCESS_PROJECT_ADDED.format(name))

    def list(self):
        """displays all projects on database
        """
        projects = Project.select().order_by(Project.name)
        for project in projects:
            print('- ', self._PROJECT_ITEM.format(project.name, project.path))

    def mv(self, name):
        pass

    def on(self, name):
        pass

    def rm(self, name):
        pass

    def reset(self, name):
        pass


def main():
    fire.Fire(WorkOn)

if __name__ == '__main__':
    if not os.path.exists('./workon.db'):
        setup()
    main()
