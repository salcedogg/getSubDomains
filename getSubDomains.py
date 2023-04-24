import requests
import re
from googlesearch import search
import concurrent.futures
import time

GOOGLE_SEARCH_URL = "https://www.google.com/search?q=site:{domain}&start={start}"

def get_subdomains(domain):
    try:
        subdomains = set()
        # Use multiple search engines to perform the search
        search_engines = ['google', 'bing', 'yahoo']
        for engine in search_engines:
            for i in range(0, 100, 10): # Increase the number of search results
                search_url = GOOGLE_SEARCH_URL.format(domain=domain, start=i)
                search_results = search(search_url, num_results=10, stop=10, pause=2.0, user_agent=f'{engine}bot')
                for url in search_results:
                    # Send an HTTP GET request to the URL and get the response
                    try:
                        response = requests.get(url, timeout=5)
                        # Extract the HTML content of the HTTP response
                        http_content = response.text
                        # Use a regular expression to search for subdomains in the HTML content of the HTTP response
                        # The regular expression matches domain names that follow the standard format of alphanumeric characters separated by dots, allowing for hyphens in the domain name
                        subdomains.update(re.findall(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', http_content))
                    except requests.exceptions.RequestException:
                        pass
        
        # Return a set of unique subdomains found in the HTML content of the HTTP responses
        return subdomains

    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

if __name__ == '__main__':
    # Prompt the user to enter a domain and call the get_subdomains function to enumerate subdomains for the specified domain
    domain = input("Enter the domain to enumerate subdomains for: ")
    
    # Measure the time taken to enumerate subdomains
    start_time = time.time()
    
    # Use multithreading to retrieve the HTTP content of multiple search results simultaneously
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(get_subdomains, domain): domain for domain in [domain]}
        for future in concurrent.futures.as_completed(future_to_url):
            subdomains = future.result()
    
    # Print the resulting set of subdomains and the time taken to enumerate subdomains
    print(f"Subdomains: {subdomains}")
    print(f"Time taken: {time.time() - start_time} seconds")
