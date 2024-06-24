import pyautogui
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
# Required for Bernstein polynomial calculation
from scipy.special import comb

import pyautogui
import time
import random

def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://127.0.0.1:5000")
    return driver

import numpy as np

def human_like_mouse_move(to_x, to_y):
    from_x, from_y = pyautogui.position()
    
    # Ensure coordinates are integers
    from_x, from_y, to_x, to_y = map(int, [from_x, from_y, to_x, to_y])
    
    # Chance for overshoot
    overshoot_chance = random.random()
    overshoot_x, overshoot_y = (to_x, to_y)
    if overshoot_chance < 1:  # Adjusted for clarity, represents a 30% chance
        overshoot_x, overshoot_y = calculate_overshoot_point(to_x, to_y)
    
    # Generate Bezier Curve points, including the potential overshoot as part of the curve
    control_points = np.array([
        [from_x, from_y],
        [random.randint(min(from_x, to_x), max(from_x, to_x)), random.randint(min(from_y, to_y), max(from_y, to_y))],
        [overshoot_x, overshoot_y],  # Potential overshoot point
        [to_x, to_y]  # Final destination
    ])
    
    # Calculate Bezier Curve points
    curve_points = calculate_bezier_curve(control_points, num_points=6)
    
    # Randomly decide if this movement will include slowing down
    include_slowdown = random.random() < 1  # 50% chance to include slowdown
    
    # Randomly determine the magnitude of the slowdown
    slowdown_factor = random.uniform(0.1, 0.2)  # Adjust these values based on desired variability
    
    # Move through the curve points with optional varying speed
    num_points = len(curve_points)
    for i, point in enumerate(curve_points):
        if include_slowdown:
            # Apply a slowdown curve if slowing down is included
            progress = i / num_points  # Progress ratio of the path covered
            speed = slowdown_factor * progress + 0.000001  # Adjust the speed based on progress and random factor
        else:
            # Keep a consistent speed if no slowdown is applied
            speed = 0.0001
        
        pyautogui.moveTo(int(point[0]), int(point[1]), duration=speed)




def calculate_bezier_curve(points, num_points=20):
    """Calculate points of a Bezier curve given control points."""
    n = len(points) - 1
    return np.array([np.sum([bernstein_poly(i, n, t) * points[i] for i in range(n + 1)], axis=0) 
                     for t in np.linspace(0, 1, num_points)])

def bernstein_poly(i, n, t):
    """Calculate the Bernstein polynomial of n, i as a function of t."""
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def calculate_overshoot_point(to_x, to_y):
    """Adjust the overshoot distance and make it relative to the target for a smoother transition."""
    #overshoot_distance = random.randint(10, 50)  # You might adjust this based on screen resolution
    overshoot_distance = random.randint(100, 200)  # You might adjust this based on screen resolution
    direction_x = random.choice([-1, 1])
    direction_y = random.choice([-1, 1])
    # Calculate overshoot point with a smoother, smaller deviation
    return to_x + direction_x * overshoot_distance, to_y + direction_y * overshoot_distance

def move_to_element_and_click(driver, element):
    location = element.location_once_scrolled_into_view
    size = element.size
    screen_x = driver.execute_script("return window.screenX + window.outerWidth - window.innerWidth;")
    screen_y = driver.execute_script("return window.screenY + window.outerHeight - window.innerHeight;")
    absolute_x = screen_x + location['x'] + size['width'] / 2
    absolute_y = screen_y + location['y'] + size['height'] / 2
    
    # Move the mouse cursor to the element
    human_like_mouse_move(absolute_x, absolute_y)
    
    # Simulate mouse down event
    pyautogui.mouseDown()
    
    # Introduce a human-like delay between mouse down and mouse up
    time.sleep(random.uniform(0.05, 0.25))  # Adjust these values as needed to simulate human speed variability
    
    # Simulate mouse up event
    pyautogui.mouseUp()

def type_human_like(text):
    for char in text:
        pyautogui.press(char)
        time.sleep(random.uniform(0.0002,0.0007)) # Adjust these values as needed
        pyautogui.keyUp(char)
        # Reduce the minimum and maximum values to speed up typing
        time.sleep(random.uniform(0.0002,0.0007))  # Adjust these values as needed


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
