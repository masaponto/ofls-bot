#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import requests
import datetime


class OFLS_SHIFT():
    """Downlooad the ofls shift which is splead sheet, and return good string.
    """

    def __init__(self, KEY='', GID=''):
        """
        Args:
        KEY (stirng) key of google spreadsheets, you can check it from the url.
        GID (string) gid of google spreadsheets, you can check it from the url.
        """

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
        """Downlooad csv from google spreadsheets and return list of string

        Args:
        url (string)

        Returns:
        2d-list [[string]]
        """
        r = requests.get(url)
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
        list of shift(dictionary)  [{int or string: string}]
        """
        weekday = datetime.date.today().weekday()
        week_start = - weekday + week * 7
        week_end = 6 - weekday + week * 7
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
        for i in range(6):
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
        week_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
        shift_list = self._get_week_shift_list(week)
        week_shift_str_list = [
            week_str[i] + '\n' + self._format_table(shift) for i, shift in enumerate(shift_list)]

        return '\n\n'.join(week_shift_str_list)

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

        return date_str + '\n' + shift_str

    def get_your_week_shift(self, name, week=0):
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
        week_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

        shift_list = self._get_week_shift_list(week)
        your_shift = [[period_str[period - 1] for period,
                       lst in shift.items() if name in lst] for shift in (shift_list)]

        shift_str = ''
        for i, shift in enumerate(your_shift):
            shift_str += week_str[i] + ': ' + \
                ','.join(shift) + '\n' if shift != [] else ""

        return shift_str.rstrip('\n')


def main():
    shift = OFLS_SHIFT()
    NAME = ""
    # print(shift.date_shift(-2))
    print(shift.week_shift(1))
    #print(shift.get_your_week_shift(NAME, week=1))


if __name__ == "__main__":
    main()
