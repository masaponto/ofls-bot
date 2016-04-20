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

- \-w , \--week: Please input integer. Defalt is 0 which means this week. 1 means next week. -1 means last week.
- \-d , \--date: Please input integer. Defalt is 0 which means today. 1 means tomorrow. -1 means yesterday.


## And more ...
If you want use ofls-shift as slack bot.   
I recomend you to use [kame_bot](https://github.com/masaponto/kamebot)  
The sample is as follows  
[ofls_bot](https://gist.github.com/masaponto/7057bd59d07a236b463299c08fd616c5)  

## Todo
- [ ] Do not send to slack if nobody is on shift.

## License
- MIT
