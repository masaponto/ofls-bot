#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import datetime
import argparse
import requests
import yaml
# from tabulate import tabulate
import tabulate


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

    def _fix_date_str(self, date_str):
        """delete 0 from date_str

        >>> shift._fix_date_str('05/08')
        '5/8'

        >>> shift._fix_date_str('09/02')
        '9/2'

        >>> shift._fix_date_str('10/12')
        '10/12'

        Args:
        string

        Returns:
        string
        """
        fixed_date_str = date_str if date_str[
            -2] != '0' else date_str[0:-2] + date_str[-1]
        fixed_date_str = date_str if fixed_date_str[
            0] != '0' else fixed_date_str[1:]
        return fixed_date_str

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
        fixed_date_str = self._fix_date_str(date_str)

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

        shift = self.data_dict[date_info]
        CELLS = 25
        shift = shift[:CELLS]

        shift_dict = {1: shift[0:1],
                      2: shift[2:3],
                      3: shift[4:6],
                      4: shift[7:9],
                      5: shift[10:12],
                      6: shift[13:15],
                      7: shift[16:21],
                      8: [shift[22]],
                      9: [shift[23]]}

        shift_dict = {k: self._fix_list(v) for k, v in shift_dict.items()}
        return shift_dict

    def _fix_list(self, shift_list):
        """remove empty string from shift_list

        >>> lst = ['', '', 'sushi', 'is', '', 'good']
        >>> shift._fix_list(lst)
        ['sushi', 'is', 'good']


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
        return [self.get_date_shift_dict(date) for date in range(week_start, week_end)]

    def _format_table(self, shift):
        """format shift good view (string).
        Args:
        shift {int: string}

        returns:
        [stirng]
        """

        periods = ('  1st: ', '  2nd: ', 'lunch: ',
                   '  3rd: ', '  4th: ', '  5th: ', 'night: ', '------\n' + 'mura: ', 'higu: ')

        shift_str_lst = [periods[i] +
                         ','.join(shift[i + 1]) for i in range(6 + 3)]
            
        return shift_str_lst

    def week_shift_table(self, week=0):
        week_str = ('月', '火', '水', '木', '金')
        periods = ('１', '２', '昼', '３', '４', '５', '夜')

        shift_list = self._get_week_shift_list(week)

        week_shift_str_list = [
            ['・'.join(shift[i + 1]) for i in range(7)] for shift in shift_list]

        week_shift_str_list.insert(0, periods)

        table = [list(x) for x in zip(*week_shift_str_list)]

        return tabulate.tabulate(table, week_str, tablefmt="pipe")

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
        week_shift_str_lst = [
            week_str[i] + '\n' + '\n'.join(self._format_table(shift)) for i, shift in enumerate(shift_list)]

        return '\n\n'.join(week_shift_str_lst)

    def _is_noshift(self, shift):
        """
        >>> shift_dic = {1: [], 2: [], 3:['ccc'], 4:['ddd'], 5:['eee'], 6:['fff'], 7:[]}
        >>> shift._is_noshift(shift_dic)
        False
        >>> empty_shift_dic = {1: [], 2: [], 3:[], 4:[], 5:[], 6:[], 7:[]}
        >>> shift._is_noshift(empty_shift_dic)
        True

        Args
        shift (dictionary){int: [string]}

        Returns:
        boolean
        """

        return bool(all([v == [] for k, v in shift.items()]))

    def date_shift(self, date=0):
        """ get one day shift and return good stirng
        date = 0 means today. date = 1 means tommorow.
        And date = -1 means yesterday.
        if nobody is on shift the day, return noshift

        Args:
        date (int)

        Returns:
        stirng
        """

        date_str = self._get_date_info(date)
        date_str = 'Today ' + date_str if date == 0 else date_str

        shift = self.get_date_shift_dict(date)
        if self._is_noshift(shift):
            return date_str + ' is no shift.'

        shift_str = '\n'.join(self._format_table(shift))

        return date_str + '\n' + shift_str

    def get_your_week_shift(self, week=0):
        """ get week shift for you and return good stirng
        week = 0 means this week. week = 1 means next week.
        And week = -1 means last week.

        Args:
        name string
        week (int)

        Returns:
        string
        """
        period_str = ('1st', '2nd', 'lunch', '3rd', '4th', '5th', 'night')
        week_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')

        shift_list = self._get_week_shift_list(week)
        your_shift = [[period_str[period - 1] for period,
                       lst in shift.items() if self.NAME in lst] for shift in (shift_list)]

        shift_str_lst = [week_str[i] + ': ' + ','.join(shift)
                         for i, shift in enumerate(your_shift) if shift != []]

        return '\n'.join(shift_str_lst)



    def _get_month_shift_list(self):
        """get shift list from this month first to today.

        Returns:
        list of shift (dictionary)  [{int: string}]
        """
        
        today = datetime.date.today()
        start_day = - int(today.strftime("%d")) + 1        
        return [self.get_date_shift_dict(date) for date in range(start_day, 0)]
    

    def get_your_month_salary(self):
        """
        get your salary (yen) of this month
        Returns:
        salary of this month (int)
        """
        return sum([self._get_your_date_salary(shift) for shift in self._get_month_shift_list()])
        
    
    def _get_your_date_salary(self, shift):
        """
        get your salary (yen) of that day

        Args:
        shift {int: string}
        
        Returns:
        salary of this month (int)       
        """
        to_time = lambda p: 1 if p == 3 or p == 7 else 1.5
        work_time = [to_time(k) for k, v in shift.items() if self.NAME in v]
        return int(sum(work_time) * 1000)
                             

def print_shift():
    p = argparse.ArgumentParser(
        description='This script is for get shift of ofls.')
    p.add_argument('-w', '--week', type=int, help='week',  nargs='?')
    p.add_argument('-t', '--table', help='is_table',
                   action='store_true')
    p.add_argument('-d', '--date', type=int, help='date', default=0, nargs='?')
    p.add_argument('-s', '--salary', help='How much salary did you earn',
                   action='store_true')
    option_args = p.parse_known_args()[0]

    shift = OFLS_SHIFT()

    if option_args.table:
        if option_args.week == None:
            print(shift.week_shift_table(0))
        else:
            print(shift.week_shift_table(option_args.week))
    elif option_args.salary:
        print(shift.get_your_month_salary(),'yen')
        
    elif option_args.week != None:
        print('Your shift')
        print(shift.get_your_week_shift(option_args.week))
        print()
        print(shift.week_shift(option_args.week))
    else:
        option_args.date = 0 if option_args.date == None else option_args.date
        print(shift.date_shift(option_args.date))


def main():
    print_shift()
    #shift = OFLS_SHIFT()
    #print(shift.get_your_month_salary())

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'shift': OFLS_SHIFT()})
    main()
