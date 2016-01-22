#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import argparse

from rpi_reporter.config import ReporterConfig
from rpi_reporter.reporter import Reporter


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('config_file', help='Config file')
    parser.add_argument('--single-run', action='store_true',
                        help='Run report loop just once')

    args = parser.parse_args()

    c = ReporterConfig()
    c.load(args.config_file)

    c.update_config()
    print("DBG: {!r}".format(c.config))

    r = Reporter(c)
    r.report_loop(single_run=args.single_run)


if __name__ == "__main__":
    main()
