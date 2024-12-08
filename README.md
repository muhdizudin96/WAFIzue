# WAFIzue  

WAFIzue is a Web Application Firewall (WAF) testing tool that offers four testing methods:  
1. **Footprinting**  
2. **Fuzzing** (XSS, SQL)  
3. **Payload Execution** (XSS, SQL)  
4. **Bypassing**  

This research would not have been possible without the invaluable inspiration provided by [WAFNinja](https://github.com/khalilbijjou/WAFNinja), which sparked my interest in this project and led to the development of WAFIzue. Additionally, the comprehensive 'all-in-one' functionality of WAFIzue relies heavily on [Wafw00f](https://github.com/EnableSecurity/wafw00f), as it plays a crucial role in the footprinting testing methodology employed within the tool.  

## Installation  

To set up WAFIzue, follow these steps:  

```console  
$ cd WAFIzue  # Navigate to the WAFIzue directory  
$ pip3 install -r requirements.txt  # Install required packages for WAFIzue  
$ cd wafw00f-master  # Navigate to the Wafw00f directory  
$ pip install wafw00f  # Install Wafw00f  
```

## Usage

### Man page
```console
$ python3 WAFIzue.py -h  

    __       __   ______   ________ ______                                    
   /  |  _  /  | /      \ /        /      |                                   
   $$ | / \ $$ |/$$$$$$  |$$$$$$$$/$$$$$$/ ________  __    __   ______        
   $$ |/$  \$$ |$$ |__$$ |$$ |__     $$ | /        |/  |  /  | /      \       
   $$ /$$$  $$ |$$    $$ |$$    |    $$ | $$$$$$$$/ $$ |  $$ |/$$$$$$  |      
   $$ $$/$$ $$ |$$$$$$$$ |$$$$$/     $$ |   /  $$/  $$ |  $$ |$$    $$ |      
   $$$$/  $$$$ |$$ |  $$ |$$ |      _$$ |_ /$$$$/__ $$ \__$$ |$$$$$$$$/       
   $$$/    $$$ |$$ |  $$ |$$ |     / $$   /$$      |$$    $$/ $$       |      
   $$/      $$/ $$/   $$/ $$/      $$$$$$/$$$$$$$$/  $$$$$$/   $$$$$$$/       

Created by: Izzuddin Salim | Codename: IZUEx1  

usage: WAFIzue.py [-h] [-F] [-xss] [-sqli] [-f] -t TARGET [-d DATABASE]  
                   [-o OUTPUT] [-c COOKIES]  

WAFIzue WAF testing tool  

optional arguments:  
  -h, --help            show this help message and exit  
  -F, --fuzz            test WAF using fuzzing  
  -xss, --xss           test WAF by executing XSS payloads  
  -sqli, --sqli         test WAF by executing SQL payloads  
  -f, --footprinting     perform footprinting using WAFWOOF  
  -t TARGET, --target TARGET  
                        target's URL where "WAFIzue" will be replaced with payloads.  
                        For example: -t "http://<YOUR_HOST>/?param=WAFIzue"  
  -d DATABASE, --database DATABASE  
                        Absolute path to a file containing payloads. The tool will  
                        use the default database if -d is not specified.  
  -o OUTPUT, --output OUTPUT  
                        Specify the name of the output file, e.g., -o output.html  
  -c COOKIES, --cookies COOKIES  
                        Session cookies. Use "," (comma) to separate multiple cookies.  
                        For example: -c cookie1="value",cookie2="value"
```

### Footprinting
WAFIzue uses [Wafw00f](https://github.com/EnableSecurity/wafw00f) to perform footprinting, which identifies the type of WAF protecting a target. To run the footprinting test, use the following command:

```console
$ python3 WAFIzue.py -f -t "http://<IP/domain>"
```

### Fuzzing Mode
Fuzzing tests the WAF's response to unexpected inputs by sending a variety of payloads. The default payloads for fuzzing are located in the `db/fuzz` directory. If no specific database is provided, the tool will use the default payloads from this folder. Here are examples of how to run fuzzing tests:

```console
# Run fuzzing with the default payloads
$ python3 WAFIzue.py -F -t "<target IP/domain>/?name=WAFIzue" 

# Run fuzzing and specify an output file
$ python3 WAFIzue.py -F -t "<target IP/domain>/?name=WAFIzue" -o fuzz.html 

# Run fuzzing with a custom payload database and specify an output file
$ python3 WAFIzue.py -F -t "<target IP/domain>/?name=WAFIzue" -d filename -o fuzz.html 

# Run fuzzing with cookies for the session
$ python3 WAFIzue.py -F -t "<target IP/domain>/?q=WAFIzue" -o fuzz.html -c cookie1="value",cookie2="value" 
```

The results will be saved in a structured manner under `results/fuzz/<timestamp>/`. The placeholder ```WAFIzue``` will be replaced with the actual payload in the specified URL.

### XSS Payload Execution Mode
This mode tests the WAF's ability to handle Cross-Site Scripting (XSS) attacks by executing a series of XSS payloads. The default payloads for XSS execution are located in the `db/xss` directory. If no specific database is specified, the tool will use the default payloads. Use the following commands to execute XSS tests:

```console
# Run XSS payload execution with the default payloads
$ python3 WAFIzue.py -xss -t "<target IP/domain>/?name=WAFIzue" 

# Run XSS payload execution and specify an output file
$ python3 WAFIzue.py -xss -t "<target IP/domain>/?name=WAFIzue" -o xss.html 

# Run XSS payload execution with a custom payload database and specify an output file
$ python3 WAFIzue.py -xss -t "<target IP/domain>/?name=WAFIzue" -d filename -o xss.html 

# Run XSS payload execution with cookies for the session
$ python3 WAFIzue.py -xss -t "<target IP/domain>/?name=WAFIzue" -o xss.html -c cookie1="value",cookie2="value" 
```

The results will be saved in a structured manner under `results/xss/<timestamp>/`. The placeholder ```WAFIzue``` will be replaced with the actual payload in the specified URL.

### SQL Payload Execution Mode
This mode tests the WAF's ability to handle SQL injection attacks by executing a series of SQL payloads. The default payloads for SQL execution are located in the `db/sqli` directory. If no specific database is specified, the tool will use the default payloads. Here’s how to run SQL tests:

```console
# Run SQL payload execution with the default payloads
$ python3 WAFIzue.py -sqli -t "<target IP/domain>/?name=WAFIzue" 

# Run SQL payload execution and specify an output file
$ python3 WAFIzue.py -sqli -t "<target IP/domain>/?name=WAFIzue" -o sql.html 

# Run SQL payload execution with a custom payload database and specify an output file
$ python3 WAFIzue.py -sqli -t "<target IP/domain>/?name=WAFIzue" -d filename -o sql.html 

# Run SQL payload execution with cookies for the session
$ python3 WAFIzue.py -sqli -t "<target IP/domain>/?name=WAFIzue" -o sql.html -c cookie1="value",cookie2="value" 
```

The results will be saved in a structured manner under `results/sqli/<timestamp>/`. The placeholder ```WAFIzue``` will be replaced with the actual payload in the specified URL.

## Future Work & Enhancements  

WAFIzue aims to evolve continuously to address the dynamic landscape of web application security. Future enhancements may include:  

1. **Expanded Fuzzing Capabilities**:   
   - Introduce additional fuzzing modes, including support for advanced attack vectors such as XML External Entity (XXE) Injection and Command Injection. This will enable users to test a broader range of vulnerabilities.  

2. **Comprehensive WAF Compatibility Testing**:  
   - Implement a framework for testing against various WAF products and vendors. This will help identify unique behaviors and evasion techniques specific to different WAF implementations.  

3. **Dynamic Payload Database Updates**:  
   - Regularly update and expand the default payload execution and fuzzing databases to include the latest known vulnerabilities and attack patterns. This will ensure that WAFIzue remains effective against emerging threats.  

4. **User Experience Enhancements**:  
   - Improve the user interface and experience by providing more detailed logging, better error handling, and interactive features. This will facilitate easier usage and understanding of the tool's capabilities.  

5. **Integration with Other Security Tools**:  
   - Explore integration possibilities with other security tools and frameworks to create a more comprehensive security testing suite. This could include compatibility with CI/CD pipelines for automated security testing.  

We welcome contributions from the community to help improve and enhance WAFIzue. Whether through code, documentation, or feedback, your input is invaluable in making this tool more effective for everyone involved in web application security.
