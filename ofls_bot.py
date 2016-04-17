#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys
from ofls_shift import OFLS_SHIFT
from kamebot import Kamebot
kame = Kamebot(channel='#ofls')

@kame.comment
def main():
    shift = OFLS_SHIFT()

    date = datetime.date.today().weekday()
    SUNDAY = 6

    if os.environ.get("OFLSNAME") == '' or os.environ.get("OFLSNAME") == None:
        print('environment vars OFLSNAME not found')
        print('please run follow')
        print('$echo \'export OFLSKEY=<your-name-goes-here>\' >> ~/.zshenv')
        sys.exit()
    else:
        NAME = os.environ.get("OFLSNAME")

    if date == SUNDAY:
        print("OFLSBotだよー。\n来週の" + NAME + "君のシフトをお知らせするよ！")
        print(shift.get_your_week_shift(NAME, week=1))
        print("\n全体のシフトはこれ！")
        print(shift.week_shift(1))
    else:
        print("OFLSBotだよー。\n今日のシフトをお知らせするよ！")
        print(shift.date_shift())


if __name__ == "__main__":
    main()
