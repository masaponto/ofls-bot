#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ofls_shift import OFLS_SHIFT
from kamebot import Kamebot
kame = Kamebot(channel='#ofls')

#@kame.comment
def main():
    shift = OFLS_SHIFT()
    print("OFLSBotだよー。シフトを知らせるよ！")
    print(shift.date_shift(0))
    #print(oflsbot.week_shift(1))

if __name__ == "__main__":
    main()
