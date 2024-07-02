import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_browser():
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed
    driver.maximize_window()  # Maximize the browser window
    driver.get("https://www.google.com")
    return driver

def search_topic(driver, topic):
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(topic)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for search results to load

def select_search_result(driver, index):
    try:
        # Wait until the search results are present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3")))
        search_results = driver.find_elements(By.CSS_SELECTOR, "h3")
        print(f"Found {len(search_results)} search results.")
        if index < len(search_results):
            result = search_results[index]
            location = result.location
            size = result.size
            x = location['x'] + size['width'] // 2
            y = location['y'] + size['height'] // 2

            # Adjust for browser window position
            window_position = driver.get_window_position()
            x += window_position['x']
            y += window_position['y'] + driver.execute_script("return window.outerHeight - window.innerHeight;")

            # Click on the search result using pyautogui
            print(f"Clicking on search result {index} at position ({x}, {y}).")
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(2)  # Wait for the page to load
        else:
            print(f"Search result index {index} is out of range.")
    except Exception as e:
        print(f"An error occurred while selecting the search result: {e}")

def scroll_through_page(driver):
    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.innerHeight;")
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    for i in range(0, scroll_height, screen_height):
        pyautogui.scroll(-screen_height)
        time.sleep(scroll_pause_time)

def main():
    # List of topics to search
    topics = ["Python programming", "Selenium automation"]

    # Open the browser
    driver = open_browser()

    for topic in topics:
        search_topic(driver, topic)
        for i in range(5):  # Click on the top 5 search results
            select_search_result(driver, i)
            scroll_through_page(driver)
            driver.back()
            time.sleep(2)  # Wait for the page to load

    driver.quit()

if __name__ == "__main__":
    main()