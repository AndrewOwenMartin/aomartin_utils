import argparse
import pathlib
import subprocess
import logging
import os
import re
import json

def split_on_empty_lines(s):

    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"

    return re.split(blank_line_regex, s.strip())

log = logging.getLogger(__name__)

def existant_file(s):

    path = pathlib.Path(s)

    if not path.exists():
    
        raise argparse.ArgumentTypeError(f"path {path} does not exist")
        
    if not path.is_file():

        raise argparse.ArgumentTypeError(f"path {path} is not a file")

    return path

def non_existant_path(s):

    path = pathlib.Path(s)

    if path.exists():
    
        raise argparse.ArgumentTypeError(f"Can't create a project in an existing directory: {path}")
        
    return path

def my_latexmk(path, gobble=True):

    cmd = ["latexmk", "-pdf", "-halt-on-error", str(path)]

    #log.info("Running command: %s", " ".join(cmd))

    env = os.environ.copy()

    env['max_print_line'] = "1000"

    if gobble:

        completed_process = subprocess.run(cmd, capture_output=True, encoding="ISO-8859-1", env=env)

        #log.info("output:\nstdout=%s\nstderr=%s", x.stdout, x.stderr)
        #log.info("output:\nstdout=%s\nstderr=%s", x.stdout.decode("ISO-8859-1"), x.stderr.decode('utf-8'))

        stdout = completed_process.stdout
        stderr = completed_process.stderr

        stdout = split_on_empty_lines(stdout)

        for line in stdout:

            if "warning" in line.casefold():

                print(line)

    else:

        completed_process = subprocess.run(cmd, env=env)

    #with open("/tmp/stdout.txt", 'w') as f:

    #    #f.write(json.dumps(stdout, indent=4))
    #    json.dump(stdout, f, indent=4)

    #with open("/tmp/stderr.txt", 'w') as f:

    #    f.write(stderr)

    #log.info("Refreshing mupdf")

    subprocess.run(["pkill", "-hup", "mupdf"])

def my_latexmk_main():

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()

    parser.add_argument('source', type=existant_file)

    parser.add_argument('--no-gobble', action='store_const', const=False, default=True, dest='gobble', help="disable gobbling of logs")

    args = parser.parse_args()

    my_latexmk(path=args.source, gobble=args.gobble)
