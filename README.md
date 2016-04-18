# ofls-bot
- oflsのシフト表を持ってくる
- Python 3

## Setting
```
$ echo 'export OFLSKEY=<your-spreadsheet-key-goes-here>' >> ~/.zshenv
$ echo 'export OFLSGID=<your-spreadsheet-gid-goes-here>' >> ~/.zshenv
$ echo 'export OFLSNAME=<your-name-goes-here>' >> ~/.zshenv
```
for setting ofls_bot.py  
see [kamebot](https://github.com/masaponto/kamebot)  

## How to use
- ofls_shift.py : Downlooad the ofls shift which is google spread sheet, and return good string.
- ofls_bot.py : slack bot based on ofls_shift.py using [kamebot](https://github.com/masaponto/kamebot)

## Require
- requests 2.9.1
- kamebot 1.0 (option: for ofls_bot.py)

## Options
- \-w , \--week: Please input integer. Defalt is 0 which means this week. 1 means next week. -1 means last week.
- \-d , \--date: Please input integer. Defalt is 0 which means today. 1 means tomorrow. -1 means yesterday.

examlpe for output next week  
```
$ python ofls_shifet.py -w 1
```


## License
- MIT
