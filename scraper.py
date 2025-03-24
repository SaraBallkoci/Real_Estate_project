from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile  # Optional
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import json
import time
import pandas as pd

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/119.0",
]

# OPTIONAL: Update with your actual Firefox profile path
# profile_path = "/home/your_name/.mozilla/firefox/abcdefgh.your-profile"

options = Options()
# options.profile = FirefoxProfile(profile_path) # OPTIONAL
options.add_argument("--headless")  # Run in background (no GUI)
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
options.set_preference("general.useragent.override",
                       random.choice(USER_AGENTS))


service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# Base URL (without page number)
base_url = "https://www.century21albania.com/en/properties?keyword=Apartment&business_type=sale&city=Tirana&page="
driver.get(base_url)
wait = WebDriverWait(driver, 5)  # Wait up to 10 seconds

time.sleep(random.uniform(5, 12))  # Random delay
# Scroll down to trigger lazy loading
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# Check if we are being blocked
print(f"Page title: {driver.title}")
if "Access" in driver.title or "blocked" in driver.page_source.lower():
    print("WARNING: Redfin has blocked the request!")
    driver.quit()
    exit()

# print(driver.page_source)

scraped_data = []
# Starting page
page_number = 1

# Scroll down multiple times to load all listings
for _ in range(3):  # Scroll multiple times
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Allow JavaScript to load content


while True:
    print(f"Scraping page {page_number}...")
  
    try:
          # Construct the URL for the current page
        current_url = f"{base_url}{page_number}"
        print(f"Scraping page {page_number}... URL: {current_url}")
        
        # Load the page
        driver.get(current_url)
        time.sleep(random.uniform(5, 12))  # Wait for the page to load
        
        # Wait for the listings to load
        wait = WebDriverWait(driver, 15)
        listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.grid-property_card")))

    except:
        print("❌Failed to locate the property list container. Exiting...")
        break
        # driver.quit()
        # exit()

    print(f"✅Found {len(listings)} listings on page {page_number}")

    for listing in listings:
        # Extract price
        try:
            price = listing.find_element(
                "css selector", "span.heading-5.text-black-custom.font-semibold.font-barlow").text.strip()
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.heading-5.text-black-custom.font-semibold.font-barlow ")))

        except:
            print("Skipping a listing due to missing price")
            price = "N/A"

        # Extract address
        try:
            address = listing.find_element(
                "css selector", "p.text-grey-shade-60.font-normal.paragraph-3.font-oakes.line-clamp-1").text.strip()
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "p.text-grey-shade-60.font-normal.paragraph-3.font-oakes.line-clamp-1")))

        except:
            print("Skipping a listing due to missing address data")
            address = "N/A"
            # Skip listings with missing elements
        try:
        
            
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.paragraph-3.text-black-custom.font-urbanist")))
            sqft = listing.find_element(By.CSS_SELECTOR, "p.paragraph-3.text-black-custom.font-urbanist").text.strip()
          
                      
        except Exception as e:
                    print("Skipping a detail due to missing data:", str(e))

     
        #try:
            

         #   wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.paragraph-3.text-black-custom.font-urbanist")))
          #  beds = listing.find_element(By.CSS_SELECTOR, "p.paragraph-3.text-black-custom.font-urbanist").text.strip()
           # print(beds)
           
                      
        #except Exception as e:
         #           print("Skipping a detail due to missing data:", str(e))


        # Extract listing link
        try:
            link_element = driver.find_element(
                By.CSS_SELECTOR, "a.h-full.c-card.block.bg-white-shade-99-to-gray-08.overflow-hidden.p-4.relative.card-shadow")
            link = link_element.get_attribute("href")
            # link = f"https://www.century21albania.com/{link}" if link.startswith("/") else link
        except:
            print("Skipping a listing due to missing link data")
            link = "N/A"
  # Skip listings with missing elements

        # Extract image URL
        try:
            image_element = listing.find_element(
                By.CSS_SELECTOR, "img.w-full.h-full.object-cover.grid-property_nested-image")
            image_url = image_element.get_attribute("src")
        except:
            print("Skipping a listing due to missing image data")
            image_url = "N/A"

    

        #for listing in listings:
         #   print(listing.get_attribute("outerHTML"))  # See raw HTML
        # Store the data
        scraped_data.append({
            "Price": price,
            "Address": address,
            # "Baths": baths,
            "SqFt": sqft,
            #"Beds": beds,
            "Link": link,
            "ImageURL": image_url,
           
        })

   
    if len(listings) > 0:
            page_number += 1
    else:
            print("🚫 No listings found. Exiting scraping process.")
            break
    
    
df = pd.DataFrame(scraped_data)
df.to_csv(r"C:\Users\User\Desktop\datapipeline\tirana_forsale.csv", index=False)
print(f"✅{len(df)} listings saved!")

driver.quit()
