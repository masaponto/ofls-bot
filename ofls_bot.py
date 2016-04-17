#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from ofls_shift import OFLS_SHIFT
from kamebot import Kamebot
kame = Kamebot(channel='#ofls')

@kame.comment
def main():
    shift = OFLS_SHIFT()

    date = datetime.date.today().weekday()
    SUNDAY = 6

    if date == SUNDAY:
        print("OFLSBotだよー。\n来週からのシフトをお知らせするよ！")
        print(shift.week_shift())
    else:
        print("OFLSBotだよー。\n今日のシフトをお知らせするよ！")
        print(shift.date_shift())


if __name__ == "__main__":
    main()
