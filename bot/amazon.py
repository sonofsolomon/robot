import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *

def slow_type(pageElem, pageInput):
    for letter in pageInput:
        time.sleep(float(random.uniform(.05, .3)))
        pageElem.send_keys(letter)

def amazon_run(driver):
    # Navigate to Amazon's main page
    driver.get("https://www.amazon.com/")

    # Wait for the search box to become clickable
    search = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "twotabsearchtextbox"))
    )

    # Type 'hello' into the search box
    slow_type(search, "hello")

    # Press Enter to submit the search
    search.send_keys(Keys.RETURN)

# Set up the driver (assuming Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    amazon_run(driver)
    time.sleep(10)  # Wait to observe the results
except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()
