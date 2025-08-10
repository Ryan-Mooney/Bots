from helpers.logger_functions import info_log, debug_log
import time, re, json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#TODO: Variables that should be secured in some way
username_input = 'mooneyryanj@gmail.com'
password_input = '422moondawgx'
search_criteria = {'search_text': 'software developer near pittsburgh, pa', 'easy_apply': True, 'date_posted': '24 Hours'}

def wait_for_element_by_xpath(driver, xpath, expected=None):
   try:
      if expected:
        info_log(f'Expected is {expected}')
        WebDriverWait(driver, timeout=5, poll_frequency=0.25).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        actual = driver.find_element(By.XPATH, xpath).text
        while expected not in actual:
           WebDriverWait(driver, timeout=5, poll_frequency=0.25).until(EC.element_to_be_clickable((By.XPATH, xpath)))
           actual = driver.find_element(By.XPATH, xpath).text
      else:
         WebDriverWait(driver, timeout=5, poll_frequency=0.25).until(EC.element_to_be_clickable((By.XPATH, xpath)))
      return driver.find_element(By.XPATH, xpath)
   except Exception as message:
      debug_log(message)

def wait_for_element_by_id(driver, id, expected=None):
   try:
      if expected:
        WebDriverWait(driver, timeout=5, poll_frequency=0.25).until(EC.element_to_be_clickable((By.ID, id)))
        actual = driver.find_element(By.ID, id).text
        while expected not in actual:
           WebDriverWait(driver, timeout=5, poll_frequency=0.25).until(EC.element_to_be_clickable((By.ID, id)))
           actual = driver.find_element(By.ID, id).text
      else:
         WebDriverWait(driver, timeout=5, poll_frequency=0.25).until(EC.element_to_be_clickable((By.ID, id)))
      return driver.find_element(By.ID, id)
   except Exception as message:
      debug_log(message)

def click_element_by_id(driver, id, expected=None):
   try:
      if expected:
        wait_for_element_by_id(driver, id, expected)
      else:
        WebDriverWait(driver, timeout=5, poll_frequency=0.25).until(EC.element_to_be_clickable((By.ID, id)))
      elem = driver.find_element(By.XPATH, id)
      elem.click()
      return elem
   except Exception as message:
      debug_log(message)

def click_element_by_xpath(driver, xpath, expected=None):
   try:
      if expected:
        wait_for_element_by_xpath(driver, xpath, expected)
      else:
        WebDriverWait(driver, timeout=5, poll_frequency=1).until(EC.element_to_be_clickable((By.XPATH, xpath)))
      elem = driver.find_element(By.XPATH, xpath)
      elem.click()
      return elem
   except Exception as message:
      debug_log(message)

def click_element_by_class(driver, class_name, expected=None):
   try:
      if expected:
        WebDriverWait(driver, timeout=5, poll_frequency=1).until(EC.element_to_be_clickable((By.XPATH, class_name)))
        actual = driver.find_element(By.XPATH, class_name).text
        while expected not in actual:
           WebDriverWait(driver, timeout=5, poll_frequency=1).until(EC.element_to_be_clickable((By.XPATH, class_name)))
           actual = driver.find_element(By.XPATH, class_name).text
      else:
        WebDriverWait(driver, timeout=5, poll_frequency=1).until(EC.element_to_be_clickable((By.XPATH, class_name)))
      elem = driver.find_element(By.CLASS_NAME, class_name)
      elem.click()
      return elem
   except Exception as message:
      debug_log(message)

def sign_in_to_linkedin(driver):
    wait_for_element_by_xpath(driver, '/html/body/div/main/div[2]/div[1]/form/div[1]/input')
    try:
      elem = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[1]/input')
      elem.click()
      elem.send_keys(username_input)   
      elem = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[2]/input')
      elem.click()
      elem.send_keys(password_input) 
      elem.send_keys(Keys.RETURN)
    except Exception as message:
      debug_log(message)

def extract_text_via_xpath(driver, xpath):
    try:
      WebDriverWait(driver, timeout=5, poll_frequency=1).until(EC.presence_of_element_located((By.XPATH, xpath)))
      return driver.find_element(By.XPATH, xpath).text
    except Exception as message:
      debug_log(message)

def clean_and_parse_json(gpt_response: str):
    # Remove ```json or ``` at start/end (Markdown code block markers)
    cleaned = re.sub(r"^```json\s*", "", gpt_response.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    
    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        print("Cleaned text was:", cleaned)
        return None