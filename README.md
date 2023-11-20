# Description
### ⚠️This script is currently available on Linux⚠️
Pmap is a port scanner written in Python. It has several options, from choosing the ports to scan to only showing open ports.
## 🗳️ Installation
You don't have to install any dependencies, this script uses local Python 3 libraries to work.
<br>
Download the script and start using it!
```
curl -O https://raw.githubusercontent.com/rxfatalslash/pmap/main/pmap.py
chmod +x pmap.py
```
## 🖱️ Use
This script works by passing it certain parameters and options.
```
pmap.py [-h] -t TARGET [-p PORTS] [-v] [--open] [-Pn]

Port scanner, free of external dependencies

options:
  -h, --help                    show this help message and exit

  -t TARGET, --target TARGET    IP address to scan (required)

  -p PORTS, --ports PORTS       Port/s to scan, you are able to use multiple ports (,) and ranges (-)

  -v, --verbose                 Activate verbosity

  --open                        Show only open ports

  -Pn, --noping                 Skip the ping comprobation
```
## 📋 License
<a href="http://www.wtfpl.net">
  <img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png" width="80" height="15" />
</a>

```
        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.
```