from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class AutoApply:
    def __init__(self):
        self.options = Options()
        self.options.headless = False

    def get_url(self, url):
        self.try_login = True
        self.driver = self.create_driver()
        self.url = url
        self.driver.get(self.url)
    
    def open_url_iframe(self):
        try:
            self.click_button(elem = 'button', text_value = 'Apply Now')
            iframe = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='apply']")))
            self.driver.switch_to.frame(iframe)
        except:
            self.close_driver()
            raise Exception('Error: Opening iFrame')

    def login(self):
        self.click_button(elem = 'a', text_value = 'Sign in')
        self.complete_auth_form(action = 'Sign in')

    def register(self, email, password):
        self.email = email
        self.password = password
        self.driver = self.create_driver()
        register_url = 'https://www.careerjet.com/register'
        self.driver.get(register_url)
        try:
            self.complete_auth_form(action = 'Create an account')
        except:
            self.close_driver()
            return 'Error'
        else:
            time.sleep(1)
            current_url = self.driver.current_url
            self.close_driver()
            if current_url != register_url:
                return 'Successfully Created a New Account'
            return 'Account already exists'

    def complete_auth_form(self, action):
        sign_in_clicked = False
        try:
            email_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
        except:
            raise Exception('Fields failed to load')
        else:
            while True:
                try:
                    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/apply2/logout']")))
                except:
                    if not sign_in_clicked:
                        self.submit_value(email_field, self.email)
                        password_field = self.driver.find_element(by="xpath", value="//input[@id='password']")
                        self.submit_value(password_field, self.password)
                        self.click_button(elem = 'button', text_value = action)
                        sign_in_clicked = True
                    else:
                        self.driver.find_element(By.ID, 'apply-close').click()
                        self.try_login = False
                        return self.open_url_iframe()
                else:
                    break
            return

    def fill_info(self, user_info, resume_path):
        self.email = user_info['email']
        self.password = user_info['password']
        self.fname = user_info['fname']
        self.lname = user_info['lname']
        self.phone = user_info['phone']
        self.resume = resume_path
        self.jobtitle = user_info['jobtitle']
        self.location = user_info['location']
        self.iter_count = 0

        if self.try_login:
            self.login()
        while True:
            labels = [["First name", self.fname], ["Surname", self.lname], ["Email", self.email]]
            self.iter_count += 1
            for label_text, input_value in labels:
                try:
                    input_id = self.driver.find_element(by="xpath", value=f"//label[contains(text(), '{label_text}')]").get_attribute('for')
                    input_box = self.driver.find_element(by="xpath", value=f"//input[@id='{input_id}']")
                    self.submit_value(input_box, input_value)
                except:
                    time.sleep(0.1)
                    continue

            for fn in (self.fill_phone, self.fill_experience, self.fill_resume):
                try:
                    fn()
                except:
                    pass
                
            for text_value in ('Continue', 'Send'):
                try:
                    self.click_button(elem='button', text_value=text_value)
                except Exception:
                    if self.iter_count >= 5:
                        self.close_driver()
                        raise Exception('Error: Extra Steps Involved')
                    continue
                else:
                    if text_value == 'Send':
                        return
                    else:
                        break
        
    def fill_phone(self):
        phone_box = self.driver.find_element(by="xpath", value=f"//input[@type='tel']")
        self.submit_value(phone_box, self.phone)

    def fill_experience(self):
        jobtitle_box = self.driver.find_element(by="xpath", value=f"//input[@placeholder='Your job title or qualification']")
        self.submit_value(jobtitle_box, self.jobtitle)
        location_box = self.driver.find_element(by="xpath", value=f"//input[@placeholder='Your location']")
        self.submit_value(location_box, self.location)
    
    def fill_resume(self):
        resume_box = self.driver.find_element(by="xpath", value=f"//input[@type='file']")
        try:
            self.driver.find_element(by="xpath", value=f"//label[@class='file-upload-s file-upload complete']")
        except:
            resume_box.send_keys(self.resume)

    def submit_value(self, input_box, value):
        if input_box.get_attribute('value') == '':
            input_box.send_keys(value)
        return

    def click_button(self, elem, text_value):
        if text_value == 'Create an account':
            time.sleep(1)

        try:
            WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, f"//{elem}[contains(text(), '{text_value}')]")))
        except:
            raise Exception('Button not clickable')
        else:
            buttons = self.driver.find_elements(by="xpath", value=f"//{elem}[contains(text(), '{text_value}')]")
            for button in buttons:
                button.click()

        if text_value == 'Send':
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success alert-flat']")))
            except:
                self.close_driver()
                raise Exception('Error: Unable to Submit Application')
            else:
                return self.close_driver()

    def create_driver(self):
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = self.options)
    
    def close_driver(self):
        return self.driver.close()