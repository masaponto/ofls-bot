# ofls-shift
- 弊学の某室のシフト表をいい感じに表示します with Python3

## Install and Setting
```
$ pip3 install git+https://github.com/masaponto/ofls-shift  --upgrade  
$ echo 'export OFLS_KEY=<your-key-for-spread-sheet-goes-here>' >> ~/.bash_profile  
$ echo 'export OFLS_GID=<your-gid-for-spread-sheet-goes-here>' >> ~/.bash_profile  
```

## Require
- requests 2.9.1
- PTable 0.9.2

## How to use
Print today's shift. see ```$ ofls -h``` for detail.
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

## License
This software is released under the MIT License  
Copyright (c) 2017 masaponto
http://opensource.org/licenses/mit-license.php
