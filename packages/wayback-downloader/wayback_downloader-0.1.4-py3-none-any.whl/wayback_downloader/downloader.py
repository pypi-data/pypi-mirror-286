import wayback
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
import socket
import sys

def check_internet_connection():
    try:
        # Try to resolve the IP address of web.archive.org
        socket.gethostbyname('web.archive.org')
        return True
    except socket.gaierror:
        return False

def create_session_with_retries():
    session = requests.Session()
    retries = Retry(total=10,
                    backoff_factor=0.3,
                    status_forcelist=[429, 500, 502, 503, 504],
                    allowed_methods=["HEAD", "GET", "OPTIONS"])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def download_archive(url, timestamp, max_retries=3):
    formatted_timestamp = timestamp.strftime("%Y%m%d%H%M%S")
    wayback_url = f"http://web.archive.org/web/{formatted_timestamp}/{url}"
    session = create_session_with_retries()
    
    for attempt in range(max_retries):
        try:
            response = session.get(wayback_url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed. Error: {str(e)}")
            if "Connection refused" in str(e):
                print("Connection refused error detected. This might be due to server-side issues or IP blocking.")
                print("Diagnostic information:")
                try:
                    ip = socket.gethostbyname('web.archive.org')
                    print(f"web.archive.org resolves to IP: {ip}")
                except socket.gaierror:
                    print("Failed to resolve web.archive.org to an IP address.")
                
                print("\nTrying to connect to web.archive.org on port 80...")
                try:
                    sock = socket.create_connection(("web.archive.org", 80), timeout=10)
                    print("Successfully connected to web.archive.org on port 80.")
                    sock.close()
                except Exception as sock_e:
                    print(f"Failed to connect to web.archive.org on port 80. Error: {str(sock_e)}")
                
                print("\nPlease check your network connection and try again later.")
                return None
            
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed to download archive for {url} at {formatted_timestamp} after {max_retries} attempts.")
                return None

def save_archive(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)

def extract_links(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        link = urljoin(base_url, a['href'])
        if urlparse(link).netloc == urlparse(base_url).netloc:
            links.add(link)
    return links

def get_content_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def crawl_and_archive(base_url, start_date, end_date, visited=None, content_hashes=None):
    if visited is None:
        visited = set()
    if content_hashes is None:
        content_hashes = set()

    if base_url in visited:
        return

    visited.add(base_url)
    
    client = wayback.WaybackClient()
    
    try:
        snapshots = client.search(base_url, from_date=start_date, to_date=end_date)
        
        for snapshot in snapshots:
            print(f"Downloading archive from {snapshot.timestamp} for {base_url}...")
            content = download_archive(base_url, snapshot.timestamp)
            if content:
                content_hash = get_content_hash(content)
                if content_hash not in content_hashes:
                    content_hashes.add(content_hash)
                    parsed_url = urlparse(base_url)
                    domain = parsed_url.netloc
                    path = parsed_url.path.strip('/').replace('/', '_')
                    if not path:
                        path = 'index'
                    filename = f"{domain}/{path}_{snapshot.timestamp.strftime('%Y%m%d%H%M%S')}.html"
                    save_archive(content, filename)
                    print(f"Saved unique content: {filename}")
                    
                    links = extract_links(content, base_url)
                    for link in links:
                        crawl_and_archive(link, start_date, end_date, visited, content_hashes)
                else:
                    print(f"Skipping duplicate content from {snapshot.timestamp}")
            
            time.sleep(2)  # Delay between requests
    
    except Exception as e:
        print(f"Error processing {base_url}: {str(e)}")

def main():
    if not check_internet_connection():
        print("Error: Unable to connect to web.archive.org. Please check your network connection and try again.")
        sys.exit(1)

    url = input("Enter the URL you want to archive (e.g., http://example.com): ")
    start_date = input("Enter the start date (YYYYMMDD): ")
    end_date = input("Enter the end date (YYYYMMDD): ")
    
    try:
        start_datetime = datetime.strptime(start_date, "%Y%m%d")
        end_datetime = datetime.strptime(end_date, "%Y%m%d")
    except ValueError as e:
        print(f"Error: Invalid date format. {str(e)}")
        return
    
    crawl_and_archive(url, start_datetime, end_datetime)

if __name__ == "__main__":
    main()