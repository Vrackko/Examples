import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Sitemap URL
sitemap_url = "https://euremotejobs.com/sitemap-1.xml"

# Specify the directory to save the file
save_directory = r"C:\Users\HP\Desktop\Instantly laptop\CCjobs\Scraped data\Link Scrapped"

# Create the directory if it doesn't exist
os.makedirs(save_directory, exist_ok=True)

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Specify the full path for the file with the date and time
file_path = os.path.join(save_directory, f"links_{current_datetime}.txt")

# Send a GET request to the sitemap URL
response = requests.get(sitemap_url)

# List to store the downloaded links
downloaded_links = []

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the XML content of the sitemap using BeautifulSoup
    soup = BeautifulSoup(response.text, "xml")

    # Extract all URLs from the sitemap that match the specified pattern
    job_links = [loc.text for loc in soup.find_all("loc") if "/job/" in loc.text]

    # Print the count of links in the sitemap
    print(f"Number of links in the sitemap: {len(job_links)}")

    # Save the links to a text file in the specified directory with the date and time
    with open(file_path, 'w') as file:
        for link in job_links:
            file.write(link + '\n')

    # Extract up to 10 URLs from the sitemap for downloading
    job_links_to_download = job_links

    # Download the content of each job link
    for link in job_links_to_download:
        job_response = requests.get(link)
        if job_response.status_code == 200:
            # Append the link to the list
            downloaded_links.append(link)
            print(link)
        else:
            print(f"Failed to download content from: {link}")

else:
    print("Failed to retrieve sitemap. Status code:", response.status_code)

# Print the list of downloaded links
print("\nList of Downloaded Links:")
print(downloaded_links)
