import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Your TMDB credentials ---
TMDB_USERNAME = os.environ.get("TMDB_USERNAME")
TMDB_PASSWORD = os.environ.get("TMDB_PASSWORD") 

# --- Setup and teardown browser ---
@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# --- Test 1: Login to TMDB ---
def test_login(browser):
    browser.get("https://www.themoviedb.org/login")
    time.sleep(2)
    browser.find_element(By.ID, "username").send_keys(TMDB_USERNAME)
    browser.find_element(By.ID, "password").send_keys(TMDB_PASSWORD)
    browser.find_element(By.ID, "login_button").click()
    time.sleep(3)
    assert "login" not in browser.current_url, "Login failed — still on login page"

# --- Test 2: Click search icon and type KGF Chapter 2 ---
def test_search_kgf_chapter_2(browser):
    browser.get("https://www.themoviedb.org/")
    time.sleep(2)

    # Click the search icon
    browser.find_element(By.CSS_SELECTOR, "a.search").click()
    time.sleep(2)

    # Type and press Enter
    wait = WebDriverWait(browser, 10)
    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
    search_input.clear()
    search_input.send_keys("KGF Chapter 2")
    search_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # Verify search results page loaded with KGF results
    assert "search" in browser.current_url, "Not on search results page"
    assert "K.G.F" in browser.find_element(By.TAG_NAME, "body").text, \
        "KGF Chapter 2 not found in search results"