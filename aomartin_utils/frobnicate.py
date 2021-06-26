import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import aomartin_utils
import argparse
import csv
import pandas as pd

log = logging.getLogger(__name__)
log.silent = functools.partial(log.log, 0)

rng = random.Random()


def main():

    log.info("__name__: %s.", __name__)


def load_csv(path):

    with path.open() as csvfile:

        reader = csv.reader(csvfile)

        headers = next(reader)

        rows = [tuple(row) for row in reader]

        df = pd.DataFrame(rows, columns=headers)

        return df


def load_excel(path):

    df = pd.read_excel(path, header=0, dtype="object")

    return df


def is_float(x):

    try:

        float(x)

    except ValueError:

        return False

    else:

        return True


def is_int(x):

    try:

        int(x)

    except ValueError:

        return False

    else:

        return True


def is_date(x):

    x = str(x)

    return bool(re.search(r"[0-9]{1,2}[^0-9][0-9]{1,2}[^0-9][0-9]{2,4}", x)) or bool(
        re.search(r"[0-9]{2,4}[^0-9][0-9]{1,2}[^0-9][0-9]{1,2}", x)
    )


def count_type(column, checker, truthy_count):

    count = sum(checker(x) for x in column)

    proportion = (count / truthy_count) if truthy_count else None

    return dict(count=count, proportion=proportion)


def get_sample(column, max_len):

    longest_sample = ""

    column = tuple(set(x for x in column if x))

    for num in itertools.count(start=1):

        try:

            sample = [str(x) for x in rng.sample(column, num)]

        except ValueError:

            sample = None

        else:

            sample = ", ".join(sample)

        if sample is None or len(sample) > max_len:

            return longest_sample

        else:

            longest_sample = sample


def frobnicate_df(df):

    info = {}

    for col_num, column_name in enumerate(df.columns):

        column = df[column_name]

        value_count = len(column.unique())

        falsy_count = sum(1 for x in column if not x)

        truthy_count = sum(1 for x in column if x)

        none_count = sum(1 for x in column if x is None)

        col_sample = get_sample(column, max_len=230)

        col_info = {
            "unique_values": value_count,
            "falsy": falsy_count,
            "truthy": truthy_count,
            "sample": col_sample,
            "none": none_count,
        }

        col_info["float"] = count_type(
            column, checker=is_float, truthy_count=truthy_count
        )
        col_info["int"] = count_type(column, checker=is_int, truthy_count=truthy_count)
        col_info["date"] = count_type(
            column, checker=is_date, truthy_count=truthy_count
        )

        log.info(
            "column: %s. %s",
            column_name,
            {k: v for k, v in col_info.items() if k != "sample"},
        )

        info[column_name] = col_info

    return info


def frobnicate_spreadsheet(path):

    info = {}

    info["path"] = str(path)

    if ".csv" in path.suffixes:

        loader = load_csv

        file_format = "CSV"

    elif set([".xls", ".xlsx"]).intersection(path.suffixes):

        loader = load_excel

        file_format = "Excel"

    info["file_format"] = file_format

    df = loader(path)

    df_info = frobnicate_df(df)

    df_meta = {
        "row_count": len(df.columns),
        "column_count": len(df),
    }

    return info_to_markdown(df_info, path, df_meta)


def info_to_markdown(info, path, df_meta):

    lines = [f"## {path.name}"]

    lines.append(f"Rows: {df_meta['row_count']}  ")
    lines.append(f"Columns: {df_meta['column_count']}  ")

    for column_name, col_info in info.items():

        lines.append(f"- **{column_name}**:")

        for k, v in col_info.items():

            if isinstance(v, dict):

                dict_str = ", ".join(f"{a}: {b}" for a, b in v.items())

                lines.append(f"  - `{k}`: {dict_str}")

            else:

                lines.append(f"  - `{k}`: {v}")

    return "\n".join(lines)


def frobnicate_main():

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )

    parser = argparse.ArgumentParser(
        description="get some markdown detailing facts about the spreadsheet and its columns."
    )

    parser.add_argument("source", type=aomartin_utils.utils.existant_file)

    args = parser.parse_args()

    info = frobnicate_spreadsheet(path=args.source)

    print(info)
