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
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
chrome_options.add_argument("--ignore-certificate-errors-spki-list")
chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

status = "Out of Stock"

counter = 0
while status == "Out of Stock":
  driver.get("https://www.evga.com/products/product.aspx?pn=08G-P5-3665-KR")
  try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "LFrame_tblMainA")))
    try:
      driver.find_element_by_id("LFrame_pnlOutOfStock")
      status = "Out of Stock"
    except:
      status = "In Stock"
    print("EVGA Status: " + status)
  except:
    pass
  counter = counter + 1
  if counter % 10 == 0:
    print(".................")
  driver.delete_all_cookies()
  time.sleep(3)

winsound.Beep(frequency, duration)
winsound.Beep(frequency, duration)
winsound.Beep(frequency, duration)

print("BACK IN STOCK. BUY NOOOOOOOOOWWWWWWWWWWWWWW")

msgRoot = MIMEMultipart("related")
msgRoot["From"] = "moondawg422@gmail.com"
msgRoot["To"]= "mooneyryanj@gmail.com"
msgRoot["Subject"] = "EVGA GPU Status Report"
message = "The RTX 3060 Ti is in stock. Click here: https://www.evga.com/products/product.aspx?pn=08G-P5-3665-KR"
msgText = MIMEText(message, "html")
msgRoot.attach(msgText)

smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login("moondawg422@gmail.com", "Moondawg422#@$")
smtp.sendmail("moondawg422@gmail.com", "mooneyryanj@gmail.com", msgRoot.as_string())
smtp.quit()

driver.quit()