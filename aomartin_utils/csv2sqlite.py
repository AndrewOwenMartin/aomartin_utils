import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import argparse
import subprocess
import sqlite3, csv
from aomartin_utils.utils import existant_file, non_existant_path

log = logging.getLogger(__name__)
log.silent = functools.partial(log.log, 0)


def csv2sqlite(csv_path, sqlite_path):

    con = sqlite3.connect(str(sqlite_path))

    cur = con.cursor()

    with csv_path.open() as f:

        reader = csv.reader(f)

        headers = next(reader)

        column_defs = ",\n".join([f"{header.casefold()} TEXT" for header in headers])

        create_sql = f"CREATE TABLE data ({column_defs});"

        log.info("creating table:\n%s", create_sql)

        cur.execute(create_sql)

        question_marks = ", ".join(["?" for header in headers])

        insert_sql = f"INSERT INTO data VALUES ({question_marks})"

        log.info("Inserting rows:\n%s", insert_sql)

        cur.executemany(insert_sql, reader)

        log.info("Inserted rows: %s", cur.rowcount)

        con.commit()


def csv2sqlite_main():

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )

    parser = argparse.ArgumentParser(description="Turn a CSV file into a sqlite table")

    parser.add_argument("csv_file", type=existant_file)

    parser.add_argument("sqlite_path", type=non_existant_path)

    args = parser.parse_args()

    csv2sqlite(csv_path=args.csv_file, sqlite_path=args.sqlite_path)
