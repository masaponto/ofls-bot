#!/usr/bin/env python

import sys
import os
from ofls import Shift


def main():
    try:
        key = os.environ['OFLS_KEY']
        gid = os.environ['OFLS_GID']
    except Exception as e:
        print('key or gid is invalid')
        print(e)
        sys.exit(1)

    shift = Shift(key, gid)

    print(shift.week_table("0"))
    print(shift.date_shift("5/29"))


if __name__ == "__main__":
    main()
