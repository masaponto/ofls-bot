#!/usr/bin/env python

import sys
import os
import csv
import datetime
import re
import requests
from prettytable import PrettyTable


class Shift():

    def __init__(self, key, gid):
        table_list = self.__get_shift_table(key, gid)
        key_pattern = re.compile('\d*\/\d*')

        self.shift_table = {key_pattern.match(row[0]).group(): DayShift(
            row[0], self.__get_oneday_shift_list(row)) for row in table_list[3:]}

    def __get_shift_table(self, key, gid):
        url = 'https://docs.google.com/spreadsheets/d/%s/export?format=csv&gid=%s' \
            % (key, gid)

        try:
            response = requests.get(url)
        except Exception as e:
            print('key or gid is invalid')
            print(e)
            sys.exit(1)

        decoded_table = response.content.decode('utf-8')
        reader = csv.reader(decoded_table.splitlines(), delimiter=',')
        table = list(reader)

        return table

    def __get_oneday_shift_list(self, row):
        shift_list = [row[1:3], row[3:5], row[5:8], row[8:11],
                      row[11:14], row[14:17], row[17:23]]
        fix_pattern = re.compile(',*$')
        shift_list = [fix_pattern.sub('', ','.join(text))
                      for text in shift_list] + [row[23], row[24], row[25]]

        return shift_list

    def date_shift(self, date_str):
        if re.match('\d+\/\d+', date_str):
            return self.shift_table[date_str]
        elif re.match('-?\d+', date_str):
            fdate = datetime.date.today() + datetime.timedelta(int(date_str))
            date_str = fdate.strftime("%-m/%-d")
            return self.shift_table[date_str]
        else:
            return 'Ooops :('

    def week_shift(self, date_str):
        start, end = self.__get_show_range(date_str)
        weekshift = [self.date_shift(str(i)) for i in range(start, end)]

        return '\n\n'.join([shift.date + '\n' + shift.get_string() for shift in weekshift])

    def week_table(self, date_str):
        start, end = self.__get_show_range(date_str)
        weekshift = [self.date_shift(str(i)) for i in range(start, end)]
        ptable = PrettyTable()
        ptable.add_column('Period', ('1st', '2nd', 'lun', '3rd',
                                     '4th', '5th', 'nig', 'mur', 'hig', 'etc'), align='l')
        [ptable.add_column(shift.date, shift.table, align='l')
         for shift in weekshift]

        return ptable.get_string()

    def __get_show_range(self, date_str):
        today = datetime.datetime.today()

        if re.match('\d+\/\d+', date_str):
            d = datetime.datetime.strptime(date_str, "%m/%d")
            d = d.replace(year=today.year)
            diff = int((d - today).total_seconds() / (3600 * 24))
            start = diff - d.weekday()
            end = start + 5
        elif re.match('-?\d+', date_str):
            weekday = today.weekday()
            start = int(date_str) * 7 - weekday
            end = start + 5
        else:
            start, end = 0, 0

        return start, end


class DayShift():

    def __init__(self, date, table):
        self.date = date
        self.table = table

    def __str__(self):
        return self.get_string()

    def get_string(self):
        indices = ('1st', '2nd', 'lun', '3rd', '4th',
                   '5th', 'nig', '------\nmur', 'hig', 'etc')
        formatted_str_list = [self.date] + ['%s : %s' % (i, name)
                                            for i, name in zip(indices, self.table)]

        return '\n'.join(formatted_str_list)


def print_shift():
    import argparse

    try:
        key = os.environ['OFLS_KEY']
        gid = os.environ['OFLS_GID']
    except Exception as e:
        print('key or gid is invalid')
        print(e)
        sys.exit(1)

    shift = Shift(key, gid)

    p = argparse.ArgumentParser(
        description='This script is to print shift table of OFLS')

    p.add_argument('-w', '--week', type=str,
                   help='week', nargs='?', const='0')
    p.add_argument('-t', '--table', type=str,
                   help='table', nargs='?', const='0')
    p.add_argument('-d', '--date', type=str,
                   help='date', nargs='?', default='0', const='0')

    option_args, other = p.parse_known_args()

    if option_args.table is not None:
        print(shift.week_table(option_args.table))

    elif option_args.week is not None:
        print(shift.week_shift(option_args.week))

    else:
        print(shift.date_shift(option_args.date))


def main():
    print_shift()


if __name__ == "__main__":
    main()
