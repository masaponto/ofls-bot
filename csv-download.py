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

    def _get_today_info(self):
        today = datetime.datetime.today()
        today_str = today.strftime("%m/%d")
        changed_today_str = today_str if today_str[0] != '0' else today_str[1:]
        return changed_today_str

    # todo 一般化する　上の関数とくっつける
    # todo class にする

    def _get_yesterday_info(self):
        yesterday = datetime.date.today() - datetime.timedelta(0)
        yesterday_str = yesterday.strftime("%m/%d")
        changed_yesterday_str = yesterday_str if yesterday_str[
            0] != '0' else yesterday_str[1:]
        return changed_yesterday_str


    def _get_shift_dict(self, data_dict, date_info):
        shift = data_dict[date_info]
        CELLS = 22
        shift = shift[:CELLS]
        shift_dict = {1: shift[0:1],
                      2: shift[2:3],
                      'lunch': shift[4:6],
                      3: shift[7:9],
                      4: shift[10:12],
                      5: shift[13:15],
                      6: shift[16:22]}

        return shift_dict

#@kame.comment


def main():
    oflsbot = OFLSBot()
    print(oflsbot._get_yesterday_info())


if __name__ == "__main__":
    main()
