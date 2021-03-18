import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import argparse
import subprocess
from aomartin_utils.utils import non_existant_path

log = logging.getLogger(__name__)
log.silent = functools.partial(log.log, 0)

rng = random.Random()

setup_py_template = """\
from setuptools import setup

setup(
    name="{project_name}",
    version="0.1",
    packages=[
        "{project_name}",
    ],
    description="",
    keywords=[],
    entry_points={{
        "console_scripts": [],
    }},
    install_requires=[],
    classifiers=[],
    author="Andrew Owen Martin",
    author_email="andrew@aomartin.co.uk",
)
"""

config_file_template = """\
[DEFAULT]

[paths]
gen_dir=./gen/
res_dir=./res/
"""

config_py_template = """\
import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import configparser
import functools
import pathlib
import pkg_resources

log = logging.getLogger(__name__)
log.silent = functools.partial(log.log, 0)

rng = random.Random()

config_file_paths = (
    pkg_resources.resource_filename(__name__, "{project_name}.conf"),
    pathlib.Path("~").expanduser() / "config" / "{project_name}.conf",
)


def load():

    config_parser = configparser.ConfigParser()

    for config_file_path in config_file_paths:

        config_file_path = pathlib.Path(config_file_path)

        if config_file_path.exists():

            log.info("loading config from %s", config_file_path)

            config_parser.read(config_file_path)

    return config_parser
"""

repl_py_template = """\
import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
from importlib import reload
import {project_name}.config
#import pandas as pd
#import numpy as np
#import plotnine as p9

log = logging.getLogger(__name__)
log.silent = functools.partial(log.log, 0)

config = {project_name}.config.load()

rng = random.Random()

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )
"""

def create_py_app(directory, project_name=None):

    if project_name is None:

        project_name = directory.name.casefold().replace("-","_")

    project_dir = directory / project_name

    log.info("making directory %s.", directory)

    directory.mkdir()

    log.info("making python module directory %s.", project_dir)

    project_dir.mkdir()

    venv_dir_path = directory / 'venv'

    log.info("making venv at %s.", venv_dir_path)

    subprocess.run(['python3', '-m', 'venv', '--prompt', directory.name, venv_dir_path])

    log.info("setting up pip a bit")

    pip_path = venv_dir_path / 'bin' / 'pip'

    subprocess.run([pip_path, 'install', 'pip', 'wheel', 'ptpython', '--upgrade'])

    activate_file_path = (directory / 'activate')

    with activate_file_path.open('w') as f:

        f.write("""\
#! /bin/echo Run like this ". activate" Error message from:
source venv/bin/activate
"""
        )

    for dir_name in ['gen','res','doc']:

        gen_dir = directory / dir_name

        log.info("making dir %s", gen_dir)

        gen_dir.mkdir()

        with (gen_dir / '.gitignore').open('w') as f:

            f.write("#*\n!gitignore\n")

    log.info("initialising git")

    subprocess.run(["git","init"], cwd=directory)

    gitignore_path = directory / '.gitignore'

    log.info("writing .gitignore to %s", gitignore_path)

    with gitignore_path.open('w') as f:

        f.write("venv\n")

    manifest_path = directory / 'MANIFEST.in'

    log.info("writing manifest to %s", manifest_path)

    with manifest_path.open('w') as f:

        f.write(f"include {project_name}/{directory.name}.conf\n")

    readme_path = directory / "README.md"

    log.info("writing root README to %s", readme_path)

    with readme_path.open('w') as f:

        f.write(f"# {directory.name} project\n\n- [doc](./doc/)\n- [res](./res/)")

    repl_exec_path = directory / 'repl'

    log.info("writing repl executable to %s", repl_exec_path)

    with repl_exec_path.open('w') as f:

        f.write("#!/bin/sh\n./venv/bin/ptpython -i repl.py\n")

    repl_exec_path.chmod(0o755)

    repl_py_path = directory / 'repl.py'

    log.info("writing repl.py to %s", repl_py_path)

    with repl_py_path.open('w') as f:

        f.write(repl_py_template.format(project_name=project_name))

    config_py_path = project_dir / 'config.py'

    log.info("writing config.py to %s", config_py_path)

    with config_py_path.open('w') as f:

        f.write(config_py_template.format(project_name=project_name))

    config_file_path = directory / project_name / f'{directory.name}.conf'

    log.info("writing config file to %s", config_file_path)

    with config_file_path.open('w') as f:

        f.write(config_file_template)

    log.info("Adding everything to initial git")

    setup_py_path = directory / 'setup.py'

    with setup_py_path.open('w') as f:

        f.write(setup_py_template.format(project_name=project_name))

    subprocess.run(["git","add", "--verbose", "."], cwd=directory)

    subprocess.run(["git","commit", "--message", "initialised with create-python-app"], cwd=directory)


def create_py_app_main():

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )

    parser = argparse.ArgumentParser()

    parser.add_argument('dir', type=non_existant_path)

    parser.add_argument('project_name', nargs='?', default=None, type=str)

    args = parser.parse_args()

    directory = args.dir

    create_py_app(directory, args.project_name)
