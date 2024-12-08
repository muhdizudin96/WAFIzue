import argparse  
import urllib.parse  
import subprocess  
import requests  
import pandas as pd  
import webbrowser  
from itertools import cycle  
import os  
from progress.bar import Bar  
from parse import parse, validate_database  
from datetime import datetime  
import matplotlib.pyplot as plt  # For plotting  
from colorama import Fore, Style, init  # For colored output  
import pyfiglet  # For ASCII art  

# Initialize colorama  
init(autoreset=True)  

def show_disclaimer():  
    """Display a disclaimer to the user."""  
    disclaimer = f"""{Fore.YELLOW}WARNING: This tool is intended for educational purposes only.   
    Unauthorized use of this tool may violate laws and regulations.   
    The developer is not liable for any misuse or unauthorized actions taken with this tool.{Style.RESET_ALL}  
    
    Do you agree to proceed? (yes/no)  
    """  
    print(disclaimer)  
    user_input = input(f"{Fore.CYAN}Your response: {Style.RESET_ALL}").strip().lower()  
    if user_input != 'yes':  
        print(f"{Fore.RED}Thanks for using WAFIzue! Have a great day!{Style.RESET_ALL}")  
        exit(0)  

def print_success(message):  
    print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")  

def print_error(message):  
    print(f"{Fore.RED}[!] {message}{Style.RESET_ALL}")  

def print_warning(message):  
    print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")  

def write_results(mode, results, target, output_filename=None):  
    """Writing result as an HTML file in a mode-specific folder"""  
    base_output_dir = 'results'  
    if not os.path.exists(base_output_dir):  
        os.makedirs(base_output_dir)  

    # Create a timestamped directory for the results  
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  
    mode_output_dir = os.path.join(base_output_dir, mode, timestamp)  
    if not os.path.exists(mode_output_dir):  
        os.makedirs(mode_output_dir)  

    if output_filename:  
        output_path = os.path.join(mode_output_dir, output_filename)  
    else:  
        output_filename = f'results_{timestamp}.html'  
        output_path = os.path.join(mode_output_dir, output_filename)  

    pass_count = sum(1 for result in results if result[1] == 'pass')  
    fail_count = sum(1 for result in results if result[1] == 'fail')  
    total_count = len(results)  

    pass_percentage = (pass_count / total_count * 100) if total_count > 0 else 0  
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

    # Create charts  
    labels = ['Passed', 'Failed']  
    sizes = [pass_count, fail_count]  
    colors = ['#4CAF50', '#F44336']  

    # Generate Pie Chart  
    plt.figure(figsize=(6, 6))  
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)  
    plt.axis('equal')  
    pie_chart_path = os.path.join(mode_output_dir, 'payload_results_pie_chart.png')  
    plt.savefig(pie_chart_path)  
    plt.close()  

    # Generate Bar Chart  
    plt.figure(figsize=(6, 4))  
    plt.bar(labels, sizes, color=colors)  
    plt.ylabel('Count')  
    plt.title('Payload Results')  
    bar_chart_path = os.path.join(mode_output_dir, 'payload_results_bar_chart.png')  
    plt.savefig(bar_chart_path)  
    plt.close()  

    if pass_count == total_count:  
        conclusion = "All payloads passed. The target appears to be secure against the tested vulnerabilities."  
    elif fail_count == total_count:  
        conclusion = "All payloads failed. The target may be highly vulnerable or unresponsive to the tests."  
    else:  
        effectiveness = (pass_count / total_count) * 100  
        conclusion = f"Some payloads passed ({pass_count}), while others failed ({fail_count}). This indicates a pass rate of {effectiveness:.2f}%."  

    try:  
        with open(output_path, 'w') as f:  
            f.write(f'''<html>  
<head>  
    <title>WAFIzue Results</title>  
    <style>  
        body {{  
            font-family: Arial, sans-serif;  
            background-color: #f4f4f4;  
            color: #333;  
            margin: 0;  
            padding: 20px;  
        }}  
        h1 {{  
            color: #007BFF;  
        }}  
        h2 {{  
            border-bottom: 2px solid #007BFF;  
            padding-bottom: 10px;  
        }}  
        table {{  
            width: 100%;  
            border-collapse: collapse;  
            margin: 20px 0;  
            background-color: #fff;  
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  
        }}  
        th, td {{  
            padding: 12px;  
            text-align: left;  
            border-bottom: 1px solid #ddd;  
        }}  
        th {{  
            background-color: #007BFF;  
            color: #fff;  
        }}  
        tr:hover {{  
            background-color: #f1f1f1;  
        }}  
        img {{  
            max-width: 100%;  
            height: auto;  
        }}  
        .conclusion {{  
            font-weight: bold;  
            margin-top: 20px;  
        }}  
    </style>  
</head>  
<body>  
    <h1>WAFIzue Results Summary</h1>  
    <p>Date and Time of Test: {current_time}</p>  
    <p>Target URL: {target}</p>  
    <p>Total Payloads Sent: {total_count}</p>  
    <p>Passed: {pass_count}</p>  
    <p>Failed: {fail_count}</p>  
    <p>Pass Percentage: {pass_percentage:.2f}%</p>  
    <p class="conclusion"><strong>Conclusion: {conclusion}</strong></p>  
    <hr>  
    <h2>Charts</h2>  
    <h3>Pie Chart of Results</h3>  
    <img src="payload_results_pie_chart.png" alt="Pie Chart">  
    <h3>Bar Chart of Results</h3>  
    <img src="payload_results_bar_chart.png" alt="Bar Chart">  
    <hr>  
    <h2>Detailed Results</h2>  
    <h3>Passed Payloads</h3>  
    <table>  
        <tr><th>Payload</th><th>Status</th><th>HTTP Method</th></tr>''')  
            
            # Separate results into passed and failed  
            passed_results = [result for result in results if result[1] == 'pass']  
            failed_results = [result for result in results if result[1] == 'fail']  

            # Write passed results first  
            for result in passed_results:  
                name = result[0].replace('>', '&gt;').replace('<', '&lt;')  
                http_method = result[2]  
                f.write(f'<tr style="background-color: #dff0d8;">')  
                f.write(f'<td>{name}</td><td>pass</td><td>{http_method}</td></tr>')  

            f.write('''</table>  
    <h3>Failed Payloads</h3>  
    <table>  
        <tr><th>Payload</th><th>Status</th><th>HTTP Method</th></tr>''')  

            # Write failed results  
            for result in failed_results:  
                name = result[0].replace('>', '&gt;').replace('<', '&lt;')  
                http_method = result[2]  
                f.write(f'<tr style="background-color: #f2dede;">')  
                f.write(f'<td>{name}</td><td>fail</td><td>{http_method}</td></tr>')  

            f.write('''</table>  
    </body>  
</html>''')  

    except Exception as e:  
        print_error(f"Error writing results to file: {e}")  
        return None  

    return output_path, pie_chart_path, bar_chart_path  

def get_proxies():  
    """Fetching proxy"""  
    proxies = []  
    r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=https")  
    print_success("[+] Getting proxy list, this will take a few seconds")  

    for line in r.text.splitlines():  
        if len(proxies) == 10:  
            break  
        ip = line.strip()  
        try:  
            response = requests.get('https://httpbin.org/ip', proxies={"http": ip, "https": ip})  
            proxies.append(ip)  
            print_success(f"[+] Got {len(proxies)} proxies")  
        except:  
            print_warning("[!] BAD proxy. Skipping to next one")  

    print_success('[+] Got ALL 10 proxies')  
    return proxies  

def fire(mode, target, payload, header, count, proxy, user_agent=None, http_methods=['GET']):  
    """Firing payload to target website"""  
    payload = urllib.parse.quote(payload.replace('\n', ''))  

    # Set the User-Agent in the header if provided  
    if user_agent:  
        header['User-Agent'] = user_agent  

    url = target.replace('WAFIzue', payload)  

    results = []  
    for http_method in http_methods:  
        if proxy is None:  
            if http_method == 'POST':  
                r = requests.post(url, headers=header)  
            else:  
                r = requests.get(url, headers=header)  
        else:  
            if http_method == 'POST':  
                r = requests.post(url, headers=header, proxies={"http": proxy, "https": proxy})  
            else:  
                r = requests.get(url, headers=header, proxies={"http": proxy, "https": proxy})  

        if r.status_code == 200:  
            status = 'pass'  
        elif r.status_code in [403, 404]:  
            status = 'fail'  
        else:  
            status = 'fail'  

        # Append the HTTP method to the results  
        results.append((urllib.parse.unquote(payload), status, http_method))  
    return results  

def create_header(cookies):  
    """Create HTML header"""  
    usr_input = input(f"{Fore.CYAN}[?] Do you want to add an extension header? (y/n): {Style.RESET_ALL}")  

    if usr_input.lower() == 'y':  
        header = {'content-type': 'application/json',  
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0',  
                  'Accept-Encoding': 'gzip, deflate, sdch',  
                  'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp,*/*;q=0.8',  
                  'Connection': 'keep-alive',  
                  'X-Originating-IP': '127.0.0.1',  
                  'X-Forwarded-For': '127.0.0.1',  
                  'X-Remote-IP': '127.0.0.1',  
                  'X-Remote-Addr': '127.0.0.1',  
                  'Cookie': cookies}  
    else:  
        header = {'content-type': 'application/json',  
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0',  
                  'Accept-Encoding': 'gzip, deflate, sdch',  
                  'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp,*/*;q=0.8',  
                  'Connection': 'keep-alive',  
                  'Cookie': cookies}  
    return header  

def read_payload(mode, target, dbPath, header, user_agent, http_methods):  
    """Read payloads from the database and fire them to the target website"""  
    print_success(f'[DEBUG] Using database path: {dbPath}')  
    count = 0  
    usr_input = input(f'{Fore.CYAN}[?] Do you want to use a web proxy to avoid IP ban? (y/n): {Style.RESET_ALL}')  

    proxy = None  
    proxy_pool = None  # Ensure proxy_pool is initialized  

    if usr_input.lower() == 'y':  
        proxy_choice = input(f'{Fore.CYAN}[?] Do you want to use the default proxy list (d) or provide a custom proxy IP (c)? (d/c): {Style.RESET_ALL}')  
        if proxy_choice.lower() == 'd':  
            proxy_pool = cycle(get_proxies())  # Use default proxies  
        elif proxy_choice.lower() == 'c':  
            custom_proxy = input(f'{Fore.CYAN}[?] Please enter your custom proxy IP (format: ip:port): {Style.RESET_ALL}')  
            proxy = custom_proxy  # Use the provided custom proxy  
            print_success(f"[+] Using custom proxy: {proxy}")  
        else:  
            print_warning("Invalid choice. Proceeding without a proxy.")  
    # No need for an else clause; proxy_pool is already None by default  

    with open(dbPath, 'r') as payloads:  
        payloads = payloads.readlines()  
        bar = Bar('Processing', max=len(payloads))  
        results = []  # Initialize results list  
        for payload in payloads:  
            count += 1  
            if proxy_pool is None:  
                result = fire(mode, target, payload, header, count, proxy, user_agent, http_methods)  
            else:  
                proxy = next(proxy_pool)  
                result = fire(mode, target, payload, header, count, proxy, user_agent, http_methods)  
            results.extend(result)  
            bar.next()  
        bar.finish()  
    return results  

def select_user_agent():  
    """Prompt the user to select a User-Agent from a list or enter a custom one."""  
    user_agents = [  
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",  
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",  
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",  
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"  
    ]  

    print("Select a User-Agent from the list below or enter your own:")  
    for i, agent in enumerate(user_agents, start=1):  
        print(f"{i}. {agent}")  
    print(f"{len(user_agents) + 1}. Enter a custom User-Agent")  

    choice = int(input("Your choice (number): "))  

    if 1 <= choice <= len(user_agents):  
        return user_agents[choice - 1]  
    elif choice == len(user_agents) + 1:  
        return input("Enter your custom User-Agent: ")  
    else:  
        print_warning("Invalid choice. Default User-Agent will be used.")  
        return None  

def select_http_method():  
    """Prompt the user to select the HTTP method for the requests."""  
    print("Select the HTTP method for the requests:")  
    print("1. GET")  
    print("2. POST")  
    print("3. GET & POST (both)")  
    choice = input("Your choice (1/2/3): ")  

    if choice == '1':  
        return ['GET']  
    elif choice == '2':  
        return ['POST']  
    elif choice == '3':  
        return ['GET', 'POST']  
    else:  
        print_warning("Invalid choice. Defaulting to GET method.")  
        return ['GET']  

# Display logo using pyfiglet  
logo = pyfiglet.figlet_format("WAFIzue")  
print(Fore.CYAN + logo + Style.RESET_ALL)  

# Display creator information  
print(Fore.MAGENTA + "Created by: Izzuddin Salim | Codename: IZUEx1" + Style.RESET_ALL)  

# Show disclaimer before proceeding  
show_disclaimer()  

args = parse()  

if args.footprinting:  
    target = args.target  
    print_success(f'[+] The target website is {target}')  
    print_success('[+] Executing wafw00f')  
    output = subprocess.getoutput('python3 wafw00f-master/wafw00f/main.py {}'.format(target))  
    print(output)  
else:  
    # Select User-Agent  
    user_agent = select_user_agent()  

    # Select HTTP Method  
    http_methods = select_http_method()  

    mode, target, cookies = args.fuzz, args.target, args.cookies  
    header = create_header(cookies)  

    # Determine the database path  
    if args.database:  
        dbPath = args.database  
    else:  
        dbPath = validate_database(args)  

    # Execute the appropriate logic based on the mode  
    if args.fuzz:  
        dbPath = 'db/fuzz'  
        payload_files = [os.path.join(dbPath, f) for f in os.listdir(dbPath) if f.endswith('.txt')]  
        results = []  
        for payload_file in payload_files:  
            results.extend(read_payload('fuzz', target, payload_file, header, user_agent, http_methods))  

    elif args.xss:  
        results = read_payload('xss', target, dbPath, header, user_agent, http_methods)  

    elif args.sqli:  
        results = read_payload('sqli', target, dbPath, header, user_agent, http_methods)  

    # Call write_results and print the output path  
    output_path, pie_chart_path, bar_chart_path = write_results('fuzz' if args.fuzz else 'xss' if args.xss else 'sqli', results, target, args.output)  
    if output_path:  # Check if output_path is valid  
        print_success(f'[+] The results are saved in {output_path}')  
        print_success(f'[+] Pie chart saved at: {pie_chart_path}')  
        print_success(f'[+] Bar chart saved at: {bar_chart_path}')  

        # Automatically open the output HTML file in the default web browser  
        webbrowser.open('file://' + os.path.realpath(output_path))  
    else:  
        print_error("Failed to save results.")
