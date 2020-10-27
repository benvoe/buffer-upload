import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_infinite(driver):
    return False

def buffer_login(driver, buffer_mail, buffer_pass):
    driver.get("https://login.buffer.com/")
    username = driver.find_element_by_id('email')
    username.send_keys(buffer_mail)
    password = driver.find_element_by_id('password')
    password.send_keys(buffer_pass + Keys.RETURN)

def buffer_select_profile(driver, select_profile):
    wait = WebDriverWait(driver, 30)
    profiles = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ProfileSidebar")]'))) # ProfileSidebar
    profile_tab = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ProfileListItem")]//label[@title="{}"]'.format(select_profile)))) # ProfileListItem
    profile_tab.click()

def buffer_open_composer(driver):
    driver.find_element_by_xpath('//button[@data-cy="open-composer-button"]').click()

def buffer_fill_composer(driver, text_path, image_path, location):
    wait = WebDriverWait(driver, 30)
    txt_field = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "public-DraftEditor-content")]'))) # public-DraftEditor-content

    text_str = open(text_path, 'r').read()
    txt_field.send_keys(text_str)
    
    img_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))) # Imagefield
    img_field.send_keys(str(image_path.absolute()))
    if location is not '':
        loc_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@class, "LocationComposerBar")]'))) # LocationComposerBar
        loc_field.send_keys(location)
        loc_item = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "LocationComposerBar__optionRowHighlighted")]')))
        loc_field.send_keys(Keys.RETURN)

def buffer_add_to_queue(driver):
    wait = WebDriverWait(driver, 30)
    print("Waiting for upload ...")

    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "UpdateSaver__button__")]')))

    submit_btn.click()

def submit_to_buffer(profile, text_path, image_path, location, email, password, driver='geckodriver'):
    driver_path = Path(__file__).parent / 'selenium' / driver

    with webdriver.Firefox(executable_path=driver_path) as driver:
        driver.implicitly_wait(10)

        # Login to Buffer
        buffer_login(driver, email, password)

        # Select profile
        buffer_select_profile(driver, profile)
        
        # Open Composer
        buffer_open_composer(driver)
        
        # Fill Composer
        buffer_fill_composer(driver, text_path, image_path, location)

        # Submit when ready
        buffer_add_to_queue(driver)
  