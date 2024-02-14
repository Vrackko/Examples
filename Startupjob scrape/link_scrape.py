from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# Set up the browser with headers
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Launch the browser
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Go to the link
    driver.get("https://startup.jobs")
    
    # Wait for 5 seconds
    time.sleep(5)
    
    # Step 2: Find the search input div
    search_div = driver.find_element(By.CLASS_NAME, "searchForm__section__input")
    
    # Step 3: Type "Customer Support" in the search input
    search_input = search_div.find_element(By.ID, "query")
    search_input.send_keys("Customer Support")
    
    # Step 4: Click on the remote checkbox
    remote_checkbox = driver.find_element(By.ID, "remote")
    remote_checkbox.click()
    
    # Step 5: Uncheck the Internship checkbox
    internship_checkbox = driver.find_element(By.ID, "commitments_internship")
    ActionChains(driver).move_to_element(internship_checkbox).click().perform()
    
    # Wait for the dynamically loaded content
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "flex.flex-col.items-start")))
    time.sleep(5)
    # Get the page source after the changes
    page_source = driver.page_source
    
    # Use BeautifulSoup to parse the modified page source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find the body with class "antialiased posts"
    body = soup.find('body', class_='antialiased posts')
    
    # Find all divs with class "flex flex-col items-start" within the specified body
    divs = body.find_all('div', class_='flex flex-col items-start')
    
    # Get all links in each div
    links = [div.a['href'] for div in divs if div.a]
    
    # Remove the first 35 links
    links = links[35:]
    
    # Exclude links equal to {{{path}}}
    links = [link for link in links if link != "{{{path}}}"]
    
    # Prepend "https://startup.jobs" to each link
    links = ["https://startup.jobs" + link for link in links]
    
    # Save the links to a text file
    with open(r'C:\Users\HP\Desktop\Instantly laptop\CCjobs\Scraped data\startupjobs\links.txt', 'w') as file:
        for link in links:
            file.write(link + '\n')
    
    # Print success message
    print("Scraping and link saving completed successfully")

except Exception as e:
    # Print error message
    print("Error: ", str(e))

finally:
    # Close the browser window
    driver.quit()
