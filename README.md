# ofls-bot
- Print shift table of OFLS

## Setting
    
```
$ echo 'key: "<ofls-google-spreadsheet-key-goes-here>"' >> ofls.yml
$ echo 'gid: "<ofls-google-spreadsheet-gid-goes-here>"' >> ofls.yml
$ echo 'name: "<your-name-goes-here>"' >> ofls.yml
```

For setting ofls_bot.py  
see [kamebot](https://github.com/masaponto/kamebot)  

## How to use
- ofls_shift.py : Download csv file via google spread sheet, and return awesome string.
- ofls_bot.py : slack bot based on ofls_shift.py using [kamebot](https://github.com/masaponto/kamebot)

## Require
- requests 2.9.1
- pyyaml 3.11
- kamebot 1.0 (option: for ofls_bot.py)

## Options
- \-w , \--week: Please input integer. Defalt is 0 which means this week. 1 means next week. -1 means last week.
- \-d , \--date: Please input integer. Defalt is 0 which means today. 1 means tomorrow. -1 means yesterday.


Examlpe for output next week  
```
$ python ofls_shifet.py -w 1
```

## Todo
- [ ] Do not send to slack if nobody is on shift.

## License
- MIT
