from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException

from helpers.logger_functions import *
from helpers.helper_functions import *
from chatgpt_bot import get_chatgpt_response

# Steps to take:

# Navigate to site
# Sign in
# Set up Search
# Open Job
# Extract job description
# Open another window to chatgpt
# Input prompt, resume, and description
# Rewrite and copy new resume
# Open job
# Input info
# log success/fail

#TODO: Variables that should be secured in some way 
username_input = ''
password_input = ''
search_criteria = {'search_text': 'software developer near pittsburgh, pa', 'easy_apply': True, 'date_posted': '24 Hours'}
OPENAI_API_KEY = ''

# Initialize driver options
chrome_options=Options()
chrome_options.add_argument("--ignore-certificate-errors-spki-list")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
chrome_options.add_experimental_option("useAutomationExtension", False) 
# chrome_options.add_argument("--headless")

def runBot():
    
    with open('resume.txt', 'r') as f:
       resume_text = f.read()

    # Open driver
    info_log("Opening linked in window...")
    linkedin_driver = webdriver.Chrome(options=chrome_options)
    linkedin_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    linkedin_driver.get("https://www.linkedin.com/jobs/collections/recommended?discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII")

    #Sign In
    sign_in_to_linkedin(linkedin_driver)
    
    try:
      # Enters search text
      if search_criteria['search_text']:
        info_log("Entering search query...")
        # WebDriverWait(linkedin_driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[3]/section/div/div/div[1]/div/ul/li[5]/div/button')))
        # elem = linkedin_driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[3]/section/div/div/div[1]/div/ul/li[5]/div/button')
        query = search_criteria['search_text']
        # Adds date criteria
        if search_criteria['date_posted']:
            query = query + f' in the past {search_criteria['date_posted']}'
        if search_criteria['easy_apply']:
            query = query + ' Easy Apply'
        info_log(f'Sending search query [{query}]...')

        wait_for_element_by_xpath(linkedin_driver, '/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/label')
        search_box = click_element_by_xpath(linkedin_driver, '/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]')
        search_box.click()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        results_text = wait_for_element_by_xpath(linkedin_driver, '/html/body/div[5]/div[3]/div[3]/div/div[1]/div/div/div[1]', 'results').text
        results = int(re.sub('\ results$', '', results_text))
        info_log('Search returned successfully.')

    except Exception as message:
      debug_log(message)
    
    list_item = 1
    while list_item <= int(results):
        # Open job
        job_title = ''
        job_company = ''
        job_description = ''
        try:
            # Click job list item
            info_log("Selecting job item...")
            wait_for_element_by_xpath(linkedin_driver, f'/html/body/div[5]/div[3]/div[3]/div/div[2]/main/div/div[2]/div[1]/ul/li[{list_item}]')
            click_element_by_xpath(linkedin_driver, f'/html/body/div[5]/div[3]/div[3]/div/div[2]/main/div/div[2]/div[1]/ul/li[{list_item}]')

            # Find job description
            info_log('Selecting job...')
            job_title = wait_for_element_by_xpath(linkedin_driver, f'/html/body/div[5]/div[3]/div[3]/div/div[2]/main/div/div[2]/div[1]/ul/li[{list_item}]/div/a/div/div/div[2]/div[1]/div[1]/span[1]/strong').text
            wait_for_element_by_xpath(linkedin_driver, '/html/body/div[6]/div[3]/div[3]/div/div[2]/main/div/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/h1', job_title)
            info_log(f'Confirming selection for {job_title}.')

            # Check if already applied
            applied_elements = linkedin_driver.find_elements(By.XPATH, '/html/body/div[6]/div[3]/div[3]/div/div[2]/main/div/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div/div[1]/div[1]/div[6]')
            if applied_elements and 'Applied' in applied_elements[0].text:
                raise Exception(f"Job already applied for {job_title}")
        
            # Extract job info
            info_log("Extracting job info...")
            job_company = wait_for_element_by_xpath(linkedin_driver, '/html/body/div[5]/div[3]/div[3]/div/div[2]/main/div/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div/div[1]/div/div[1]/div[1]/div/a').text
            job_description = wait_for_element_by_xpath(linkedin_driver, '/html/body/div[5]/div[3]/div[3]/div/div[2]/main/div/div[2]/div[2]/div/div[3]/div[1]/div/div[5]/article/div/div[1]').text

            # import os
            # doc_name = f'Ryan Mooney Resume - {job_title} at {job_company}.docx'
            # current_dir = os.getcwd()
            # filepath = os.path.join(current_dir, 'resumes', doc_name)
            doc_name = get_chatgpt_response(resume_text, job_description, job_title, job_company) #filepath

            apply_with_resume(linkedin_driver, doc_name)

        except Exception as message:
            debug_log(message)

        if 25 % list_item:
            click_element_by_xpath(linkedin_driver, '/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/div[3]/div/button')
            time.sleep(1)

        list_item = list_item + 1

    linkedin_driver.quit()

def fill_in_empty_fields(driver):
    wait_for_element_by_xpath(driver, '/div/div/div[1]/div/input')
    input_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    for field in input_fields:
        try:
            if field.is_displayed() and field.is_enabled():
                value = field.get_attribute("value")
                if value == "":
                    field.clear()
                    field.send_keys("1")
        except ElementNotInteractableException:
            print("Element not interactable, skipping")
   
def apply_with_resume(linkedin_driver, doc_name):

    wait_for_element_by_xpath(linkedin_driver, '/html/body/div[5]/div[3]/div[3]/div/div[1]/div/div/div[1]', 'results')

    click_element_by_xpath(linkedin_driver, "//*[@id='jobs-apply-button-id']")
    click_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/form/footer/div[2]/button')
    wait_for_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/form/div/div/h3', 'Resume')

    import os
    current_dir = os.getcwd()
    filepath = os.path.join(current_dir, 'resumes', doc_name)
    time.sleep(1)
    file_input = linkedin_driver.find_element(By.NAME, "file")
    print(filepath)
    file_input.send_keys(filepath)
    click_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]')
    wait_for_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/form/div/div/div/h4', 'Mark this job as a top choice')
    fill_in_empty_fields(linkedin_driver)
    click_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]')
    wait_for_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/form/div/div/h3', 'Additional Questions')
    fill_in_empty_fields(linkedin_driver)
    click_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]')
    wait_for_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/div/div/h3', 'Review your application')
    click_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/div/footer/div[3]/button[2]')

    wait_for_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[1]/h2', 'Application Sent')
    click_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[3]/button')

    # file_input = wait_for_element_by_xpath(linkedin_driver, '/html/body/div[4]/div/div/div[2]/div/div[2]/form/div/div/div/div[2]/div[1]/input')
    # file_input.send_keys(r'C:\Users\moone\OneDrive\Documents\Bots\resume-applier\resumes\Ryan Mooney Resume - example title at example company.docx')


    while True:
       pass

runBot()
