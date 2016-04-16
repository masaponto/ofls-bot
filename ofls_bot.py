#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import requests
import datetime

from kamebot import Kamebot
kame = Kamebot(channel='#ofls')

class OFLSBot():

    def __init__(self, KEY='', GID=''):

        if KEY == '':
            if os.environ.get("OFLSKEY") == '':
                print('environment vars KEY not found')
                sys.exit()
            else:
                KEY = os.environ.get("OFLSKEY")

        if GID == '':
            if os.environ.get("OFLSGID") == '':
                print('environment vars OFLSGID not found')
                sys.exit()
            else:
                GID = os.environ.get("OFLSGID")

        self.URL = 'https://docs.google.com/spreadsheets/d/' + \
            KEY + '/export?format=csv&gid=' + GID

        self.get_data_dict()

    def _get_csv_list(self, url):
        r = requests.get(url)
        decoded_content = r.content.decode('utf-8')
        reader = csv.reader(decoded_content.splitlines(), delimiter=',')
        return list(reader)

    def get_data_dict(self):
        datalist = self._get_csv_list(self.URL)
        self.data_dict = {data[0][:-3]: data[1:] for data in datalist}

    def _get_date_info(self, date=0):
        date = datetime.date.today() + datetime.timedelta(date)
        date_str = date.strftime("%m/%d")
        fixed_date_str = date_str if date_str[0] != '0' else date_str[1:]
        return fixed_date_str

    def get_date_shift_dict(self, date=0):
        date_info = self._get_date_info(date)

        if not date_info in self.data_dict:
            print('data not found orz')
            sys.exit()
        #assert(date_info in self.data_dict)

        shift = self.data_dict[date_info]
        CELLS = 22
        shift = shift[:CELLS]
        shift_dict = {1: shift[0:1],
                      2: shift[2:3],
                      'lunch': shift[4:6],
                      3: shift[7:9],
                      4: shift[10:12],
                      5: shift[13:15],
                      6: shift[16:22]}

        shift_dict = {k: self._fix_list(v) for k, v in shift_dict.items()}

        return shift_dict

    def _fix_list(self, shift_list):
        return [name for name in shift_list if name != '']

    def _get_week_shift_list(self, week=0):
        weekday = datetime.date.today().weekday()
        week_start = - weekday + week * 7
        week_end = 6 - weekday + week * 7
        return [self.get_date_shift_dict(date) for date in range(week_start, week_end + 1)]

    def _format_table(self, shift):
        shift_str = '  1st: ' + ','.join(shift[1]) + '\n' + \
                    '  2nd: ' + ','.join(shift[2]) + '\n' + \
                    'lunch: ' + ','.join(shift['lunch']) + '\n' + \
                    '  3rd: ' + ','.join(shift[3]) + '\n' + \
                    '  4th: ' + ','.join(shift[4]) + '\n' + \
                    '  5th: ' + ','.join(shift[5]) + '\n' + \
                    'night: ' + ','.join(shift[6])
        return shift_str

    def week_shift(self, week=0):
        week_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
        shift_list = self._get_week_shift_list(week)
        week_shift_str_list = [
            week_str[i] + '\n' + self._format_table(shift) for i, shift in enumerate(shift_list)]

        return 'Hello, I am OFLSBot.\nThe shifts of this week are \n' + '\n\n'.join(week_shift_str_list)

    def date_shift(self, date=0):
        shift = self.get_date_shift_dict(date)
        shift_str = self._format_table(shift)
        date_str = self._get_date_info(date)
        date_str = 'Today ' + date_str if date == 0 else date_str

        return 'Hello, I am OFLSBot.\n' + date_str + '\'s shift is \n' + shift_str


@kame.comment
def main():
    oflsbot = OFLSBot()
    print(oflsbot.date_shift(0))
    #print(oflsbot.week_shift(1))


if __name__ == "__main__":
    main()
