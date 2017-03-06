import os
import sys

def get_project_path():
    return os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        'workon'
    )
