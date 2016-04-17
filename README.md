# ofls-bot
oflsのシフト表を持ってくる

## Setting
```
$ echo 'export OFLSKEY=<your-spreadsheet-key-goes-here>' >> ~/.zshenv
$ echo 'export OFLSGID=<your-spreadsheet-gid-goes-here>' >> ~/.zshenv
```

## How to use
- ofls_shift.py : Downlooad the ofls shift which is splead sheet, and return good string.
- ofls_bot.py : slack bot based on ofls_shift.py using [kamebot](https://github.com/masaponto/kamebot)

## Require
- requests 2.9.1
- kamebot 1.0 (option: for ofls_bot.py)

## License
- MIT
