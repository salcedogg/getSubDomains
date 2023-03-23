import requests
import re

def get_subdomains(domain):

    # Construct the Google search query for the site operator with the specified domain
    url = f"https://www.google.com/search?q=site:{domain}&start=0"
    # Set the User-Agent header to a web browser user agent string to avoid being blocked by Google
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    # Send an HTTP GET request to the specified URL with the specified headers and get the response
    response = requests.get(url, headers=headers)
    # Extract the HTML content of the HTTP response
    html = response.text
    # Use a regular expression to search for subdomains in the HTML content of the HTTP response
    # The regular expression matches domain names that follow the standard format of alphanumeric characters separated by dots, allowing for hyphens in the domain name
    subdomains = re.findall(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', html)
    # Return a set of unique subdomains found in the HTML content of the HTTP response
    return set(subdomains)


# Prompt the user to enter a domain and call the get_subdomains function to enumerate subdomains for the specified domain
domain = input("Enter the domain to enumerate subdomains for: ")
subdomains = get_subdomains(domain)
# Print the resulting set of subdomains
print(subdomains)

 #S4









