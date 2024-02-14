import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import re
from PIL import Image
from io import BytesIO

# Function to scrape text and image from the specified HTML elements
def scrape_job_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find job title
    job_title_element = soup.find('h1', class_='visualHeader__title')
    job_title = job_title_element.text.strip() if job_title_element else None
    
    # Find employer
    employer_element = soup.find('h2', class_='visualHeader__subtitle')
    employer = employer_element.text.strip() if employer_element else None

    # Find image URL
    image_element = soup.find('a', class_='block object-contain h-20 w-20 overflow-hidden bg-white rounded')
    image_url = image_element.find('img')['src'] if image_element and image_element.find('img') else None

    # Find application link
    application_link_element = soup.find('a', class_='flex justify-center items-center gap-2 w-full text-center text-lg px-6 py-3 border border-transparent text-base font-bold rounded-md drop-shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 group')
    application_link = application_link_element['href'] if application_link_element else None

    return job_title, employer, image_url, application_link

# Function to download and save an image with sanitized file name
def download_image(image_url, folder_path, file_name_prefix):
    # Replace invalid characters with underscores in the file name
    sanitized_file_name = re.sub(r'[^a-zA-Z0-9_]', '_', file_name_prefix)

    # Replace the placeholder with the actual base URL
    full_image_url = f'https://startup.jobs{image_url}'

    # Request the image data
    response = requests.get(full_image_url)
    image_data = response.content

    # Open the image using Pillow to determine the file type
    try:
        img = Image.open(BytesIO(image_data))
        # Save the image with the correct file extension
        img.save(os.path.join(folder_path, f'{sanitized_file_name}.{img.format.lower()}'))
    except Exception as e:
        print(f"Error saving image: {e}")

# Function to read links from the text file, scrape data, and save to Excel with images in the specified folder
def scrape_and_save_to_excel(file_path, image_folder):
    # Read links from the text file
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file]

    # Initialize a list to store scraped data
    data = []

    # Create a folder for images
    os.makedirs(image_folder, exist_ok=True)

    # Iterate through each link and scrape job information
    for link in links:
        job_title, employer, image_url, application_link = scrape_job_info(link)
        if job_title and employer and image_url and application_link:
            data.append({'Link': link, 'Job Title': job_title, 'Employer': employer, 'Image URL': image_url, 'Application Link': f'https://startup.jobs{application_link}'})

            # Extract the file name from the image URL
            file_name_prefix = f'Job_{len(data)}'
            
            # Download and save the image in the specified image folder
            download_image(image_url, image_folder, file_name_prefix)

    # Print the scraped data for debugging
    print("Scraped Data:")
    print(data)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Specify the desired path for saving the Excel file
    excel_file_path = r'C:\Users\HP\Desktop\Instantly laptop\CCjobs\Scraped data\startupjobs\CustomerSupport.xlsx'

    # Print the Excel file path for debugging
    print("Excel File Path:", excel_file_path)

    df.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    # Specify the path to the text file containing links
    text_file_path = r'C:\Users\HP\Desktop\Instantly laptop\CCjobs\Scraped data\startupjobs\links.txt'

    # Specify the folder where images will be saved
    image_folder_path = r'C:\Users\HP\Desktop\Instantly laptop\CCjobs\Scraped data\startupjobs\JobImages'

    # Call the function to scrape data, save to Excel, and download images
    scrape_and_save_to_excel(text_file_path, image_folder_path)
