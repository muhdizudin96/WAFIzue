import argparse  
from pathlib import Path  
import os  

def parse():  
    """Parse user given arguments  

    Returns:  
        parsed args (Namespace): Namespace object of parsed arguments  
    """  
    parser = argparse.ArgumentParser(  
        description="ProjectX WAF testing tool")  
    parser.add_argument('-F', '--fuzz', action="store_true",  
                        help="testing WAF using fuzzing")  
    parser.add_argument('-xss', '--xss', action="store_true",  
                        help="testing WAF by executing XSS payloads")  
    parser.add_argument('-sqli', '--sqli', action="store_true",  
                        help="testing WAF by executing SQL payloads")  
    parser.add_argument('-f', '--footprinting', action="store_true",  
                        help="footprinting WAF using WAFW00F")  
    parser.add_argument('-t', '--target', type=str, required=True,  
                        help='target\'s url and "WAFIzue" where the payloads will be replaced.\nFor instance: -t "http://<YOUR_HOST>/?param=WAFIzue"')  
    parser.add_argument('-o', '--output', type=str,  
                        help="Name of the output file ex -o output.html")  
    parser.add_argument('-c', '--cookies', type=str,  
                        help='Cookies for the session. Use "," (comma) to separate cookies\nFor instance: -c cookie1="something",cookie2="something"')  
    parser.add_argument('-d', '--database', type=str,  
                        help='Path to custom payload file')  # Added custom payload file argument  
    parser.add_argument('-u', '--user-agent', type=str,  
                        help='Custom User-Agent string. If not provided, a default will be used.')  
    parser.add_argument('--user-agent-options', action='store_true',  
                        help='Show predefined User-Agent options to choose from.')  

    args = parser.parse_args()  

    if args.user_agent_options:  
        print("Predefined User-Agent options:")  
        print("1. Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  
        print("2. Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15")  
        print("3. Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36")  
        exit(0)  

    return args  

def validate_database(args):  
    """Validating given database  
    
    Check if the given database exists; if not, the default database will be used.  
    If the given path to the database exists, the given path will be used.  

    Args:  
        args (Namespace): Arguments given by user  

    Returns:  
        database path (str): Path to payload database  
    """  
    if args.database:  # Check if a custom database file is provided  
        if os.path.isfile(args.database):  
            return args.database  # Use the custom database file  
        else:  
            print(f"[!!] Custom database file {args.database} does not exist. Falling back to default.")  
    
    # Default paths for payloads  
    if args.xss:  
        return 'db/xss.txt'  # Default XSS payload file  
    elif args.sqli:  
        return 'db/sqli.txt'  # Default SQL injection payload file  
    elif args.fuzz:  
        return 'db/fuzz'  # Return the directory for fuzzing payloads  
    
    return None  # No specific database for fuzzing  

def validate_output(output):  
    """Validate the output file path.  

    Ensure the output directory exists or create it.  

    Args:  
        output (str): Output file path.  

    Returns:  
        str: Validated output file path.  
    """  
    output_path = Path(output)  
    if not output_path.parent.exists():  
        print(f"[!!] Output directory {output_path.parent} does not exist. Creating it.")  
        output_path.parent.mkdir(parents=True, exist_ok=True)  
    return str(output_path)  

def removeWhiteSpace(f):  
    """ Removes whitespace from filename and appends .html  

    Args:  
        f (str): Input filename string  

    Returns:  
        str: Filename with spaces removed and .html appended  
    """  
    fName = str(f).replace(" ", "") + '.html'  
    return fName  

# Example usage  
if __name__ == "__main__":  
    args = parse()  
    if args.output:  # Validate output if provided  
        args.output = validate_output(args.output)  
    print(args)
