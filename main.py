import requests
import re

def extract_emails(url):
    response = session.get(url)
    if response.status_code == 200:
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', response.text, re.IGNORECASE)
        return emails
    else:
        return []

def crawl_subdomains(base_url, file_name):
    with open(file_name, 'w') as file:
        visited = set()
        queue = [base_url]

        while queue:
            current_url = queue.pop(0)
            if current_url in visited:
                continue

            visited.add(current_url)

            emails = extract_emails(current_url)
            for email in emails:
                file.write(email + '\n')

            response = session.get(current_url)
            if response.status_code == 200:
                links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', response.text)
                for link in links:
                    if link.startswith('http') and base_url in link and link not in visited:
                        queue.append(link)

# Main program
url = input("Enter the base URL: ")
file_name = input("Enter the file name to save emails: ")

session = requests.Session()
crawl_subdomains(url, file_name)

print("Emails extracted and saved successfully.")
