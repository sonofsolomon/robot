import numpy
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import *
import time
import random
import datetime
# Import your module functions here
from amazon import amazon_run
# from foxnews import fox_news_run
# ... other imports ...

# Assuming these functions are defined in your imported modules
functionList = [ebay_run]#, etsy_run, fox_news_run, game_run, cookie_run, ebay_run]
# loginList = [gearbest_run, ali_express_run, wish_run, shein_run]

def setDriver():
    options = webdriver.ChromeOptions()  # Initializing Chrome Options from the Webdriver
    prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
    options.add_argument("start-fullscreen")
    options.add_argument("disable-popup-blocking")
    options.add_argument("disable-notifications")
    options.add_argument("disable-gpu")  # Renderer timeout

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(10)
    return driver

def main():
    start = datetime.datetime.now()
    random.shuffle(functionList)  # Shuffles list of functions
    driver = setDriver()
    driver.set_page_load_timeout(30)  # Set timeout to 30 seconds

    driver.get("https://www.google.com")

    # for func in loginList:  # Go through login functions
    #     func(driver)
    #     time.sleep(2)

    for func in functionList:  # Go through functions in shuffled order
        func(driver)
        time.sleep(2)

    end = datetime.datetime.now()
    executionTime = end - start

    print("Start time - " + str(start))
    print("End time - " + str(end))
    print("Execution Time - " + str(executionTime))

    driver.quit()

if __name__ == "__main__":
    main()
