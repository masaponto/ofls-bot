#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import requests
import datetime

from kamebot import Kamebot
kame = Kamebot(channel='#random')

class OFLSBot():

    def __init__(self, KEY='', GID=''):

        if KEY == '':
            if os.environ.get("KEY") == '':
                print('environment vars KEY not found')
                sys.exit()
            else:
                KEY = os.environ.get("KEY")

        if GID == '':
            if os.environ.get("SPGID") == '':
                print('environment vars SPGID not found')
                sys.exit()
            else:
                GID = os.environ.get("SPGID")

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

    def _get_date_info(self, date = 0):
        date = datetime.date.today() + datetime.timedelta(date)
        date_str = date.strftime("%m/%d")
        fixed_date_str = date_str if date_str[
            0] != '0' else date_str[1:]
        return fixed_date_str

    def get_date_shift_dict(self, date=0):
        date_info = self._get_date_info(date)
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

        shift_dict = {k:self._fix_list(v) for k, v in shift_dict.items()}

        return shift_dict

    def _fix_list(self, shift_list):
        return [name for name in shift_list if name != '']

    def date_shift(self, date=0):
        shift = self.get_date_shift_dict(date)

        if date == 0:
            date_str = 'Today'
        elif date > 0:
            date_str = 'after ' + str(date) + ' day'
        elif date < 0:
            date_str = 'before ' + str(abs(date)) + ' day'

        shift_str = '  1st: ' + ','.join(shift[1]) + '\n' + \
                    '  2nd: ' + ','.join(shift[2]) + '\n' + \
                    'lunch: ' + ','.join(shift['lunch']) + '\n' + \
                    '  3rd: ' + ','.join(shift[3]) + '\n' + \
                    '  4th: ' + ','.join(shift[4]) + '\n' + \
                    '  5th: ' + ','.join(shift[5]) + '\n' + \
                    'night: ' + ','.join(shift[6])


        return 'Hello, I am OfLSBot.\n' + date_str + 's shift is \n' + shift_str


#@kame.comment
def main():
    oflsbot = OFLSBot()
    print(oflsbot.date_shift(-1))


if __name__ == "__main__":
    main()
