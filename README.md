# WAFIzue
WAF testing tool offer 4 testing methods:
1. Footprinting
2. Fuzzing (XSS, SQL)
3. Payload execution (XSS, SQL)
4. Bypassing


Special thank to all contributors [Awesome-WAF](https://github.com/0xInfection/Awesome-WAF/graphs/contributors) repo. Moreover, this research could not be done without [WAFNinja](https://github.com/khalilbijjou/WAFNinja), since it was the tool that inspired me to work on this project and give me the idea of creating WAFIzue. Lastly, WAFIzue would not be able to offer "all-in-one" feature without [Wafw00f](https://github.com/EnableSecurity/wafw00f), since it is used in WAFIzue when performing footprinting testing methods.

# Installation
```console
$ pip3 install -r requirements.txt # setup WAFIzue
$ cd wafw00f-master # Go to wafw00f directory
$ pip install wafw00f # setup Wafw00f
```

# Usage

## Man page
```console
$ python3 WAFIzue.py -h

    __       __   ______   ________ ______                                    
#  /  |  _  /  | /      \ /        /      |                                   
#  $$ | / \ $$ |/$$$$$$  |$$$$$$$$/$$$$$$/ ________  __    __   ______        
#  $$ |/$  \$$ |$$ |__$$ |$$ |__     $$ | /        |/  |  /  | /      \       
#  $$ /$$$  $$ |$$    $$ |$$    |    $$ | $$$$$$$$/ $$ |  $$ |/$$$$$$  |      
#  $$ $$/$$ $$ |$$$$$$$$ |$$$$$/     $$ |   /  $$/  $$ |  $$ |$$    $$ |      
#  $$$$/  $$$$ |$$ |  $$ |$$ |      _$$ |_ /$$$$/__ $$ \__$$ |$$$$$$$$/       
#  $$$/    $$$ |$$ |  $$ |$$ |     / $$   /$$      |$$    $$/ $$       |      
#  $$/      $$/ $$/   $$/ $$/      $$$$$$/$$$$$$$$/  $$$$$$/   $$$$$$$/       
                                                                        
Develop by Muhammad Izzuddin Bin Salim | Student ID:B22020039

usage: WAFIzue.py [-h] [-F] [-xss] [-sqli] [-f] -t TARGET [-d DATABASE]
                   [-o OUTPUT] [-c COOKIES]

WAFIzue WAF testing tool

optional arguments:
  -h, --help            show this help message and exit
  -F, --fuzz            testing WAF using fuzzing
  -xss, --xss           testing WAF by executing XSS payloads
  -sqli, --sqli         testing WAF by executing SQL payloads
  -f, --footprinting    footprinting WAF using WAFWOOF
  -t TARGET, --target TARGET
                        target's url and "WAFIzue" where the payloads will be
                        replace. For instance: -t
                        "http://<YOUR_HOST>/?param=WAFIzue"
  -d DATABASE, --database DATABASE
                        Absolute path to file contain payloads. the tool will
                        use the default database if -d is not given
  -o OUTPUT, --output OUTPUT
                        Name of the output file ex -o output.html
  -c COOKIES, --cookies COOKIES
                        cookies for the session. Use "," (comma) to separeate
                        cookies For instance: -c
                        cookie1="something",cookie2="something"
```
## Fuzzing mode
```console
$ python3 WAFIzue.py -F -t "<target IP>/?q=WAFIzue" -o fuzz.html -c cookie="something"
```
the payloads will be replace with ```WAFIzue``` in ``-t`` so dont for get to include it
## XSS Payload execution mode
```console
$ python3 WAFIzue.py -xss -t "<target IP>/?name=WAFIzue" -o xss.html -c cookie1="something",cookie2="something"
```
the payloads will be replace with ```WAFIzue``` in ``-t`` so dont for get to include it

## SQL Payload execution mode
```console
$ python3 WAFIzue.py -sqli -t "<target IP>/?name=WAFIzue" -o sql.html -c cookie1="something",cookie2="something"
```
the payloads will be replace with ```WAFIzue``` in ``-t`` so dont for get to include it

## Footprinting
WAFIzue is using [Wafw00f](https://github.com/EnableSecurity/wafw00f) to perform footprinting
```console
$ python3 WAFIzue.py -f -t "<target IP>"
```

# Future Work and Enhancements

As a future work continuation on improving the tools would be interesting.  The code injection has been the most common vulnerability in the past ten years based on the OWASP top ten list. It would be interesting to add more fuzzing mode and payload execution to WAFIzue. For instance, XML External Entity (XXE) Injection and Command Injection. When WAFIzue is performing fuzzing mode, it fuzzes both XSS and SQL at the same time. Another thing that would be interesting is to split fuzzing mode so the tester specifically fuzzes what they want, not both XSS and SQLI at the same time. Furthermore, testing the tool on different WAF products/vendors could also be possible and beneficial. Lastly, both default payload executions and fuzzing databases should be updated to make to WAFIzue more powerful
