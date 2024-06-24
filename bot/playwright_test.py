import threading
from playwright.sync_api import sync_playwright
import numpy as np
import random
import time
from pynput import keyboard
import pyautogui

synchronize_mouse = False

def keyboard_listener():
    def on_press(key):
        global synchronize_mouse
        if key == keyboard.Key.cmd:  # Adjust for macOS Command key
            synchronize_mouse = True

    def on_release(key):
        global synchronize_mouse
        if key == keyboard.Key.cmd:
            synchronize_mouse = False

    # Listener setup inside the function to ensure proper thread handling
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

def setup_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://127.0.0.1:5000")
    return page, playwright

def human_like_mouse_move(page, to_x, to_y, last_position):
    from_x, from_y = last_position
    # Define control points for the Bezier curve
    control_points = np.array([
        [from_x, from_y],
        [random.randint(min(from_x, to_x), max(from_x, to_x)), random.randint(min(from_y, to_y), max(from_y, to_y))],
        [to_x, to_y]
    ])
    curve_points = calculate_bezier_curve(control_points, num_points=50)
    for point in curve_points:
        page.mouse.move(int(point[0]), int(point[1]))
        if synchronize_mouse:
            pyautogui.moveTo(point[0], point[1])
        time.sleep(0.01)
    return (to_x, to_y)

def calculate_bezier_curve(points, num_points=100):
    n = len(points) - 1
    return np.array([np.sum([bernstein_poly(i, n, t) * points[i] for i in range(n + 1)], axis=0) for t in np.linspace(0, 1, num_points)])

def bernstein_poly(i, n, t):
    from scipy.special import comb
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def type_human_like(page, text):
    for char in text:
        page.keyboard.press(char)
        time.sleep(random.uniform(0.01, 0.55))

def move_and_click(page, selector, last_position):
    element = page.query_selector(selector)
    box = element.bounding_box()
    center_x = box['x'] + box['width'] / 2
    center_y = box['y'] + box['height'] / 2
    new_position = human_like_mouse_move(page, center_x, center_y, last_position)
    page.mouse.click(center_x, center_y)
    return new_position

def login_process(page):
    last_position = (0, 0)
    last_position = move_and_click(page, "#loginEmail", last_position)
    type_human_like(page, "admin")
    last_position = move_and_click(page, "#loginPassword", last_position)
    type_human_like(page, "password123")
    last_position = move_and_click(page, "#robotCheck", last_position)
    type_human_like(page, "I am not a robot")
    last_position = move_and_click(page, "#testing", last_position)
    last_position = move_and_click(page, "input[type='submit']", last_position)
    page.reload()

if __name__ == "__main__":
    thread = threading.Thread(target=keyboard_listener)
    thread.start()

    page, playwright = setup_browser()
    try:
        while True:
            login_process(page)
            time.sleep(0.5)
    finally:
        playwright.stop()
        thread.join()  # Ensure the keyboard listener thread is cleanly stopped
