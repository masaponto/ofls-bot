# ofls-shift
- Print shift table of OFLS

## Install and Setting

```
$ pip install git+https://github.com/masaponto/ofls-shift  --upgrade
$ mkdir $HOME/.config/ofls_shift/
$ echo 'key: "<ofls-google-spreadsheet-key-goes-here>"' >> $HOME/.config/ofls_shift/ofls.yml
$ echo 'gid: "<ofls-google-spreadsheet-gid-goes-here>"' >> $HOME/.config/ofls_shift/ofls.yml
$ echo 'name: "<your-name-goes-here>"' >> $HOME/.config/ofls_shift/ofls.yml
```


## Require
- requests 2.9.1
- pyyaml 3.11

## Options
- \-w , \--week: Please input integer. Defalt is 0 which means this week. 1 means next week. -1 means last week.
- \-d , \--date: Please input integer. Defalt is 0 which means today. 1 means tomorrow. -1 means yesterday.


Examlpe for output next week  
```
$ ofls -w 1
```

## Todo
- [ ] Do not send to slack if nobody is on shift.

## License
- MIT
