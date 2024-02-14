from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import time


chrome_driver_path = r'C:\Users\HP\Desktop\chromedriver-win64\chromedriver.exe'


with open('C:\\Users\\HP\\Desktop\\Personal laptop\\Web Scraping\\Company wall\\links.txt', 'r') as file:
    source_links = file.read().splitlines()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')


service = ChromeService(chrome_driver_path)


driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    
    all_company_links = []

    # Iterate through the source links
    for source_link in source_links:
        
        driver.get(source_link)

        
        time.sleep(5)

        
        page_source = driver.page_source

        
        soup = BeautifulSoup(page_source, 'html.parser')

        
        loc_elements = soup.find_all('loc')
        company_links = [loc.text for loc in loc_elements]

       
        all_company_links.extend(company_links)

    
    if len(all_company_links) > 0:
        
        with open('C:\\Users\\HP\\Desktop\\Personal laptop\\Web Scraping\\Company wall\\Companylinks.txt', 'w') as file:
            for company_link in all_company_links:
                file.write(company_link + '\n')

        print("Company links have been saved to 'C:\\Users\\HP\\Desktop\\Personal laptop\\Web Scraping\\Company wall\\Companylinks.txt'")
    else:
        print("No company links found in the provided source links. Exiting.")

finally:
    
    driver.quit()
