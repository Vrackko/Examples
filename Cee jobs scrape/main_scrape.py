import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd
import urllib.request

# Specify the path to the file with links
links_file_path = r"C:\Users\HP\Desktop\Instantly laptop\CCjobs\Scraped data\Link Scrapped\links_2023-12-04_15-07-13.txt"

# Specify the directory to save the scraped data and images
scraped_data_directory = r"C:\Users\HP\Desktop\Instantly laptop\CCjobs\Scraped data\Data Scraped"

# Create the directory if it doesn't exist
os.makedirs(scraped_data_directory, exist_ok=True)

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Specify the full path for the Excel file with the scraped data and date and time
excel_file_path = os.path.join(scraped_data_directory, f"scraped_data_{current_datetime}.xlsx")

# Create a directory for images
images_directory = os.path.join(scraped_data_directory, f"Img Scraped_{current_datetime}")
os.makedirs(images_directory, exist_ok=True)

# Read the links from the file
with open(links_file_path, 'r') as file:
    links = [line.strip() for line in file]

# List to store the scraped data
scraped_data = []

# Iterate over all links
for link in links:
    response = requests.get(link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize variables inside the loop
        name = soup.find('h1', class_='page-title').get_text(strip=True)
        job_types = ', '.join([job_type.get_text(strip=True) for job_type in soup.select('ul.job-listing-meta li.job-type')])
        location = soup.find('li', class_='location').get_text(strip=True)
        time_posted = soup.find('li', class_='date-posted').get_text(strip=True)
        company_name = soup.find('li', class_='job-company').get_text(strip=True)
        salary_element = soup.find('li', class_='wpjmef-field-salary')
        salary = salary_element.get_text(strip=True) if salary_element else "/"
        closing_time_element = soup.find('li', class_='application-deadline')
        closing_time = closing_time_element.get_text(strip=True).replace('Closes:', '').strip() if closing_time_element else "Unknown"

        overview_tag = soup.find('h2', class_='widget-title widget-title--job_listing-top job-overview-title', string='Overview')
        desc_1 = '\n'.join([tag.get_text(strip=True) for tag in overview_tag.find_next_siblings() if 'job_application' not in tag.get('class', [])]) if overview_tag else "N/A"

        about_company_tag = soup.find('h2', class_='widget-title widget-title--job_listing-top job-overview-title', string=f'About {company_name}')
        desc_2 = '\n'.join([tag.get_text(strip=True) for tag in about_company_tag.find_next_siblings() if 'job_application' not in tag.get('class', [])]) if about_company_tag else "N/A"

        expired_tag = soup.find('div', class_='job-manager-info', string='This job listing has expired')
        status = 'Expired' if expired_tag else 'Active'

        image_tag = soup.find('img', class_='company_logo')
        image_url = image_tag['src'] if image_tag else None

        application_div = soup.find('div', class_='job_application application')
        application_link = application_div.find('a')['href'] if application_div and application_div.find('a') else 'Expired'

        if status != 'Expired' and image_url:
            image_name = f"{company_name}_logo.jpg"
            image_path = os.path.join(images_directory, image_name)
            urllib.request.urlretrieve(image_url, image_path)
        else:
            image_path = "N/A"

        # Append the scraped data to the list, including the link
        scraped_data.append({
            'Link': link,  # New column for the original link
            'Application Link': application_link,  # New column for the application link
            'Name': name,
            'Job Type': job_types,
            'Posted from': location,
            'Time of posting': time_posted,
            'Company name': company_name,
            'Salary': salary,
            'Closing time': closing_time,
            'Desc_1': desc_1,
            'Desc_2': desc_2,
            'Status': status,
            'Image Path': image_path
        })
        print(f"Scraped data from: {link}")
    else:
        print(f"Failed to scrape data from: {link}")

# Create a DataFrame from the scraped data
df = pd.DataFrame(scraped_data)

# Add columns for the time of scrapping
df['Time of Scrapping'] = current_datetime

# Reorder the columns
df = df[['Link', 'Application Link', 'Name', 'Job Type', 'Posted from', 'Time of posting', 'Company name', 'Salary', 'Closing time', 'Desc_1', 'Desc_2', 'Status', 'Image Path', 'Time of Scrapping']]

# Save the DataFrame to an Excel file
df.to_excel(excel_file_path, index=False)

# Print the DataFrame
print("\nScraped Data:")
print(df)
