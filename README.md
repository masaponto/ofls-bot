# ofls-shift
- Print shift table of OFLS
- Python 3.x

## Install and Setting

```
$ pip3 install git+https://github.com/masaponto/ofls-shift  --upgrade
$ mkdir $HOME/.config/ofls-shift/
$ echo 'key: "<ofls-google-spreadsheet-key-goes-here>"' >> $HOME/.config/ofls_shift/ofls.yml
$ echo 'gid: "<ofls-google-spreadsheet-gid-goes-here>"' >> $HOME/.config/ofls_shift/ofls.yml
$ echo 'name: "<your-name-goes-here>"' >> $HOME/.config/ofls_shift/ofls.yml
```

## Require
- requests 2.9.1
- pyyaml 3.11

## How to use
Print today's shift  
```
$ ofls
```  

Print tomorrow's shift  
```
$ ofls -d 1
```  

print next week  
```
$ ofls -w 1
```

if you want to see the shift table for a week  
```
$ ofls -t
```


- \-w , \--week: Please input integer. Defalt is 0 which means this week. 1 means next week. -1 means last week.
- \-d , \--date: Please input integer. Defalt is 0 which means today. 1 means tomorrow. -1 means yesterday.
- \-t , \--table: You can see the time table for a week

## And more ...
If you want use ofls-shift as slack bot. You can use [kame_bot](https://github.com/masaponto/kamebot)  
The sample is as follows  
[ofls_bot](https://gist.github.com/masaponto/63c76fb3514412f2239b42f7770c32e3)  

## License
- MIT

## THANKS
This software uses python-tabulate.py
https://github.com/gregbanks/python-tabulate/blob/master/tabulate.py
