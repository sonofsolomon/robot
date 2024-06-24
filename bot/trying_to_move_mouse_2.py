from pynput.mouse import Controller, Button
# import keyboard from pynput.keyboard with the following code:
from pynput.keyboard import Controller as KeyboardController, Key

from selenium import webdriver
from selenium.webdriver.common.by import By
from scipy.special import comb
import numpy as np
import random
import time

# Initialize the mouse controller
mouse = Controller()
# defined keyboard controller
keyboard = KeyboardController()
def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://127.0.0.1:5000")
    return driver

def human_like_mouse_move(to_x, to_y):
    from_x, from_y = mouse.position
    from_x, from_y, to_x, to_y = map(int, [from_x, from_y, to_x, to_y])

    # Overshoot logic
    overshoot_chance = random.random()
    overshoot_x, overshoot_y = (to_x, to_y) if overshoot_chance >= 0.3 else calculate_overshoot_point(to_x, to_y)

    # Slowing down logic
    slow_down_chance = random.random()

    control_points = np.array([
        [from_x, from_y],
        [random.randint(min(from_x, to_x), max(from_x, to_x)), random.randint(min(from_y, to_y), max(from_y, to_y))],
        [overshoot_x, overshoot_y],
        [to_x, to_y]
    ])
    
    curve_points = calculate_bezier_curve(control_points, num_points=200)
    
    for i, point in enumerate(curve_points):
        # Adjust speed only towards the end, and only sometimes
        if slow_down_chance < 0.5 and i > len(curve_points) * 0.8:  # Slow down in the last 20%, 50% chance
            speed = 0.01  # Slower speed
        else:
            speed = 0.001  # Normal speed
        
        mouse.position = (int(point[0]), int(point[1]))
        time.sleep(speed)

def calculate_bezier_curve(points, num_points=100):
    n = len(points) - 1
    return np.array([np.sum([bernstein_poly(i, n, t) * points[i] for i in range(n + 1)], axis=0)
                     for t in np.linspace(0, 1, num_points)])

def bernstein_poly(i, n, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def calculate_overshoot_point(to_x, to_y):
    overshoot_distance = random.randint(10, 50)
    direction_x = random.choice([-1, 1])
    direction_y = random.choice([-1, 1])
    return to_x + direction_x * overshoot_distance, to_y + direction_y * overshoot_distance

def move_to_element_and_click(driver, element):
    location = element.location_once_scrolled_into_view
    size = element.size
    screen_x = driver.execute_script("return window.screenX + window.outerWidth - window.innerWidth;")
    screen_y = driver.execute_script("return window.screenY + window.outerHeight - window.innerHeight;")
    absolute_x = screen_x + location['x'] + size['width'] / 2
    absolute_y = screen_y + location['y'] + size['height'] / 2
    human_like_mouse_move(absolute_x, absolute_y)
    mouse.click(Button.left, 1)  # Perform a click

def type_human_like(text):
    for char in text:
        # Use the keyboard controller to press and release keys
        keyboard.press(char)
        time.sleep(random.uniform(0.01, 0.15))  # Adjust these values as needed
        keyboard.release(char)
        # Random delay to mimic human typing
        time.sleep(random.uniform(0.0002, 0.0007))


def fill_field(driver, element_id, text):
    element = driver.find_element(By.ID, element_id)
    move_to_element_and_click(driver, element)  # Ensure the element is focused by clicking on it
    element.clear()  # Ensure the field is empty
    type_human_like(text)  # Type the provided text

def login_process(driver, username, password):
    fill_field(driver, "loginEmail", username)
    fill_field(driver, "loginPassword", password)
    fill_field(driver, "robotCheck", "I am not a robot")
    robot_checkbox = driver.find_element(By.ID, "testing")
    move_to_element_and_click(driver, robot_checkbox)
    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    move_to_element_and_click(driver, submit_button)
    time.sleep(0.5)  # Adjust based on your application's response time

    driver.refresh()  # Reset the form for the next attempt

driver = setup_driver()
try:
    while True:
        login_process(driver, "admin", "password123")
        time.sleep(0.5)  # Wait time between attempts, adjust as necessary
finally:
    driver.quit()
