import random, time, re, xlwt, datetime, os, smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders
import winsound

# Initialize
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
chrome_options=Options()
chrome_options.add_argument("--ignore-certificate-errors-spki-list")
chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.bestbuy.com/")

# Enter search criteria
element = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "c-close-icon")))
elem = driver.find_element_by_xpath('//*[@class="c-close-icon c-modal-close-icon"]').click()
try:
  element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "survey-invite-no")))
  elem = driver.find_element_by_xpath('//*[@id="survey-invite-no"]').click()
except:
  pass
element = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.ID, "gh-search-input")))
elem = driver.find_element_by_id("gh-search-input")
elem.click()
elem.send_keys("rtx 3060 ti")
elem.send_keys(Keys.RETURN)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main-results")))
status = driver.find_element_by_class_name("add-to-cart-button").text

counter = 0
while status == "Sold Out":
  try:
    time.sleep(3)
    driver.refresh()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main-results")))
    status = driver.find_element_by_class_name("add-to-cart-button").text
    print("Best Buy Status: " + status)
  except:
    pass
  counter = counter + 1
  if counter % 10 == 0:
    print(".................")

winsound.Beep(frequency, duration)
winsound.Beep(frequency, duration)
winsound.Beep(frequency, duration)

print("BACK IN STOCK. BUY NOOOOOOOOOWWWWWWWWWWWWWW")

msgRoot = MIMEMultipart("related")
msgRoot["From"] = "moondawg422@gmail.com"
msgRoot["To"]= "mooneyryanj@gmail.com"
msgRoot["Subject"] = "Best Buy GPU Status Report"
message = "The RTX 3060 Ti is in stock. Click here: https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402"
msgText = MIMEText(message, "html")
msgRoot.attach(msgText)

smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login("moondawg422@gmail.com", "Moondawg422#@$")
smtp.sendmail("moondawg422@gmail.com", "mooneyryanj@gmail.com", msgRoot.as_string())
smtp.quit()

driver.quit()