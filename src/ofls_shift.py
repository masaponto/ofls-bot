#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import datetime
import argparse
import requests
import yaml


class OFLS_SHIFT():
    """Downlooad the ofls shift which is splead sheet, and return good string.
    """

    def __init__(self):

        try:
            with open(os.environ['HOME'] + '/.config/ofls-shift/ofls.yml', 'r') as f:
                data = yaml.load(f)
        except Exception as e:
            print(e)
            print('Please create config flie at $HOME/.config/ofls_shift/ofls.yml.')
            sys.exit(1)

        self.NAME = data['name']
        self.URL = 'https://docs.google.com/spreadsheets/d/' + \
          data['key'] + '/export?format=csv&gid=' + data['gid']

        self.get_data_dict()

    def _get_csv_list(self, url):
        """Downlooad csv from google spreadsheets and return list of string

        Args:
        url (string)

        Returns:
        2d-list [[string]]
        """
        try:
            r = requests.get(url)
        except Exception as e:
            print(e)
            print('key or gid are not correct.')
            sys.exit(1)

        decoded_content = r.content.decode('utf-8')
        reader = csv.reader(decoded_content.splitlines(), delimiter=',')
        return list(reader)

    def get_data_dict(self):
        """get new shift file, and set it as dictionary
        """
        datalist = self._get_csv_list(self.URL)
        self.data_dict = {data[0][:-3]: data[1:] for data in datalist}

    def _get_date_info(self, date=0):
        """get date information
        date = 0 means today. date = 1 means tommorow.
        And date = -1 means yesterday.

        Args:
        date (int)

        Returns:
        fixed_date_str (string)
        """
        date = datetime.date.today() + datetime.timedelta(date)
        date_str = date.strftime("%m/%d")
        fixed_date_str = date_str if date_str[0] != '0' else date_str[1:]
        return fixed_date_str

    def get_date_shift_dict(self, date=0):
        """get shift (dictionary) baesd on the date (argument)

        Args:
        date (int)

        Returns
        dictionary {int: [string]}
        """
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
                      3: shift[4:6],
                      4: shift[7:9],
                      5: shift[10:12],
                      6: shift[13:15],
                      7: shift[16:22]}

        shift_dict = {k: self._fix_list(v) for k, v in shift_dict.items()}

        return shift_dict

    def _fix_list(self, shift_list):
        """remove empty string from shift_list

        Args:
        shift_list ([string])

        Returns:
        fixed_shift_list ([string])
        """
        return [name for name in shift_list if name != '']

    def _get_week_shift_list(self, week=0):
        """get one week shift
        week = 0 means this week. week = 1 means next week.
        And week = -1 means last week.

        Args:
        week (int)

        Returns:
        list of shift (dictionary)  [{int: string}]
        """
        weekday = datetime.date.today().weekday()
        week_start = - weekday + week * 7
        week_end = 5 - weekday + week * 7
        return [self.get_date_shift_dict(date) for date in range(week_start, week_end + 1)]

    def _format_table(self, shift):
        """format shift good view (string).

        Args:
        shift {int: string}

        returns:
        string
        """

        periods = ('  1st: ', '  2nd: ', 'lunch: ',
                   '  3rd: ', '  4th: ', '  5th: ', 'night: ')
        shift_str = ''
        for i in range(6 + 1):
            shift_str += periods[i] + ','.join(shift[i + 1]) + '\n'

        return shift_str

    def week_shift(self, week=0):
        """ get one week shift and return good stirng
        week = 0 means this week. week = 1 means next week.
        And week = -1 means last week.

        Args:
        week (int)

        Returns:
        stirng
        """
        week_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
        shift_list = self._get_week_shift_list(week)
        week_shift_str_list = [
            week_str[i] + '\n' + self._format_table(shift) for i, shift in enumerate(shift_list)]

        return '\n'.join(week_shift_str_list)

    def date_shift(self, date=0):
        """ get one day shift and return good stirng
        date = 0 means today. date = 1 means tommorow.
        And date = -1 means yesterday.

        Args:
        date (int)

        Returns:
        stirng
        """
        shift = self.get_date_shift_dict(date)
        shift_str = self._format_table(shift)
        date_str = self._get_date_info(date)
        date_str = 'Today ' + date_str if date == 0 else date_str

        return date_str + '\n' + shift_str.rstrip('\n')

    def get_your_week_shift(self, week=0):
        """ get week shift for you and return good stirng
        week = 0 means this week. week = 1 means next week.
        And week = -1 means last week.

        Args:
        name string
        week (int)

        Returns:
        stirng
        """
        period_str = ('1st', '2nd', 'lunch', '3rd', '4th', '5th', 'night')
        week_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')

        shift_list = self._get_week_shift_list(week)
        your_shift = [[period_str[period - 1] for period,
                       lst in shift.items() if self.NAME in lst] for shift in (shift_list)]

        shift_str = ''
        for i, shift in enumerate(your_shift):
            shift_str += week_str[i] + ': ' + \
                ','.join(shift) + '\n' if shift != [] else ""

        return shift_str.rstrip('\n')


def print_shift():
    p = argparse.ArgumentParser(description='This script is for get shift of ofls.')
    p.add_argument('-w', '--week', type=int, help='week', nargs='?')
    p.add_argument('-d', '--date', type=int, help='date', default=0, nargs='?')
    option_args = p.parse_known_args()[0]

    shift = OFLS_SHIFT()
    if option_args.week != None:
        print('Your shift')
        print(shift.get_your_week_shift(option_args.week))
        print()
        print(shift.week_shift(option_args.week))
    else:
        print(shift.date_shift(option_args.date))

def main():
    print_shift()

if __name__ == "__main__":
    main()
