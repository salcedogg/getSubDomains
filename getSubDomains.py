import requests
import re
from googlesearch import search

GOOGLE_SEARCH_URL = "https://www.google.com/search?q=site:{domain}&start=0"

def get_subdomains(domain):
    try:
        # Use the googlesearch library to perform the Google search
        search_query = f"site:{domain}"
        search_results = search(search_query, num_results=10)

        subdomains = set()
        for url in search_results:
            # Send an HTTP GET request to the URL and get the response
            response = requests.get(url, timeout=5)
            # Extract the HTML content of the HTTP response
            http_content = response.text
            # Use a regular expression to search for subdomains in the HTML content of the HTTP response
            # The regular expression matches domain names that follow the standard format of alphanumeric characters separated by dots, allowing for hyphens in the domain name
            subdomains.update(re.findall(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', http_content))

        # Return a set of unique subdomains found in the HTML content of the HTTP responses
        return subdomains

    except Exception as e:
        print(f"An error occurred: {e}")
        return set()


# Prompt the user to enter a domain and call the get_subdomains function to enumerate subdomains for the specified domain
domain = input("Enter the domain to enumerate subdomains for: ")
subdomains = get_subdomains(domain)
# Print the resulting set of subdomains
print(subdomains)
