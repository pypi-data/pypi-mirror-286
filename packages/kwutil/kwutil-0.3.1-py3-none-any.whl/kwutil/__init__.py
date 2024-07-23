"""
The kwutil Module
=================

+------------------+------------------------------------------------------+
| Read the docs    | https://kwutil.readthedocs.io                        |
+------------------+------------------------------------------------------+
| Gitlab (main)    | https://gitlab.kitware.com/computer-vision/kwutil    |
+------------------+------------------------------------------------------+
| Github (mirror)  | https://github.com/Kitware/kwutil                    |
+------------------+------------------------------------------------------+
| Pypi             | https://pypi.org/project/kwutil                      |
+------------------+------------------------------------------------------+

The Kitware utility module.

This module is for small, pure-python utility functions. Dependencies are
allowed, but they must be small and highly standard packages (e.g. rich,
psutil, ruamel.yaml).

"""
__version__ = '0.3.1'

__autogen__ = """
mkinit ~/code/kwutil/kwutil/__init__.py --lazy_loader
mkinit ~/code/kwutil/kwutil/__init__.py
"""


__submodules__ = {
    'copy_manager': ['CopyManager'],
    'partial_format': [],
    'slugify_ext': [],
    'util_environ': ['envflag'],
    'util_eval': [],
    'util_exception': [],
    'util_json': [],
    'util_locks': [],
    'util_parallel': ['coerce_num_workers'],
    'util_path': [],
    'util_pattern': [],
    'util_progress': ['ProgressManager'],
    'util_resources': [],
    'util_time': ['datetime', 'timedelta'],
    'util_windows': [],
    'util_random': [],
    'util_yaml': ['Yaml'],
}

import lazy_loader


__getattr__, __dir__, __all__ = lazy_loader.attach(
    __name__,
    submodules={
        'copy_manager',
        'partial_format',
        'slugify_ext',
        'util_environ',
        'util_eval',
        'util_exception',
        'util_json',
        'util_locks',
        'util_parallel',
        'util_path',
        'util_pattern',
        'util_progress',
        'util_random',
        'util_resources',
        'util_time',
        'util_windows',
        'util_yaml',
    },
    submod_attrs={
        'copy_manager': [
            'CopyManager',
        ],
        'util_environ': [
            'envflag',
        ],
        'util_parallel': [
            'coerce_num_workers',
        ],
        'util_progress': [
            'ProgressManager',
        ],
        'util_time': [
            'datetime',
            'timedelta',
        ],
        'util_yaml': [
            'Yaml',
        ],
    },
)

__all__ = ['CopyManager', 'ProgressManager', 'Yaml', 'coerce_num_workers',
           'copy_manager', 'datetime', 'envflag', 'partial_format',
           'slugify_ext', 'timedelta', 'util_environ', 'util_eval',
           'util_exception', 'util_json', 'util_locks', 'util_parallel',
           'util_path', 'util_pattern', 'util_progress', 'util_random',
           'util_resources', 'util_time', 'util_windows', 'util_yaml']
