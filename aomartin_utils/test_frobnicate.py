import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import unittest
import aomartin_utils.frobnicate as frobnicate

log = logging.getLogger(__name__)
log.silent = functools.partial(log.log, 0)

rng = random.Random()


class TestAOMartinUtils(unittest.TestCase):
    def setUp(self):

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        )

    def test_frobnicate(self):

        paths = [
            pathlib.Path(p)
            for p in [
                # "/home/amartin/downloads/davids-bridal-2/Coupon redemptions all Accounts 1208_0506.xlsx",
                # "/home/amartin/downloads/davids-bridal-2/Loyalty Accounts by purch behavior 05052021.xlsx",
                "/home/amartin/downloads/davids-bridal-2/Loyalty_byorder.csv",
            ]
        ]

        for path in paths:

            log.info(path)

            info = frobnicate.frobnicate_spreadsheet(path)

            print(info)

            # for col_name, col_info in info.items():

            #    sample = col_info.pop('sample')

            #    log.info("%s: %s\n%s", col_name, col_info, sample)
