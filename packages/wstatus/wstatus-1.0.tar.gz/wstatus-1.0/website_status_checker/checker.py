import requests
import sys
import argparse
from urllib.parse import urlparse

def check_website(url, method='GET'):
    try:
        # Basic URL validation
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return f"Invalid URL format: {url}"

        if method.upper() == 'POST':
            response = requests.post(url, timeout=5)
        else:
            response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return f"{url} is up!"
        else:
            return f"{url} is down! Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"{url} is down! Error: {e}"

def check_websites(urls, method='GET'):
    results = []
    for url in urls:
        result = check_website(url, method)
        results.append(result)
    return results

def check_websites_cli():
    parser = argparse.ArgumentParser(description="Check the status of websites.")
    parser.add_argument('urls', metavar='URL', type=str, nargs='+', help='URLs to check')
    parser.add_argument('-g', '--get', action='store_const', const='GET', default='GET', help='Use GET request (default)')
    parser.add_argument('-p', '--post', action='store_const', const='POST', help='Use POST request')
    parser.add_argument('-o', '--output', type=str, help='Output file to save the results')

    args = parser.parse_args()
    method = args.get if args.get else args.post

    results = check_websites(args.urls, method)
    
    if args.output:
        with open(args.output, 'w') as f:
            for result in results:
                f.write(result + '\n')
    else:
        for result in results:
            print(result)