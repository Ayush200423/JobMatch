from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class AutoApply:
    def __init__(self, email, password, firstname, surname, phone, resume_path, jobtitle, location):
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.phone = phone
        self.resume_path = resume_path
        self.jobtitle = jobtitle
        self.location = location
        self.password = password
        self.q_num = 4
        self.options = Options()
        self.options.headless = False   # For debugging purposes, change to True
    
    def open_url_iframe(self, url, refresh_page = True):
        self.driver = self.create_driver()
        self.url = url
        self.refresh_page = refresh_page
        self.driver.get(self.url)
        try:
            self.click_button(elem = 'button', text_value = 'Apply Now')
            iframe = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='apply']")))
            time.sleep(0.1)
            self.driver.switch_to.frame(iframe)
        except:
            self.refresh()

    def fill_personal_info(self):
        self.login()
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='q0']")))
        except:
            raise Exception('Error locating elements')
        general_text_to_fill = [['q0', self.firstname], ['q1', self.surname], ['q2', self.email], ['q30', self.phone]]
        for value, input in general_text_to_fill:
            try:
                input_box = self.driver.find_element(by = "xpath", value=f"//input[@name='{value}']")
                if input_box.get_attribute("value") == "":
                    input_box.send_keys(input)
                else:
                    continue
            except:
                self.q_num -= 1
            time.sleep(0.1)
        return

    def fill_work(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//input[@name='q{self.q_num}']")))
        except:
            raise Exception('Error locating elements')
        resume_information = [[f'q{self.q_num}', self.resume_path], [f'q{self.q_num}-occupation', self.jobtitle], [f'q{self.q_num}-location', self.location]]
        for value, input in resume_information:
            try:
                input_box = self.driver.find_element(by = "xpath", value = f"//input[@name='{value}']")
                if input_box.get_attribute("value") == "":
                    input_box.send_keys(input)
                time.sleep(0.1)
            except:
                if self.q_num != 5:
                    self.q_num = 5
                    self.click_button(elem = 'button', text_value = 'Continue')
                    self.fill_work()
                else:
                    raise Exception('Error filling in resume details')
        else:
            self.click_button(elem = 'button', text_value = 'Continue')
            self.click_button(elem = 'button', text_value = 'Send')

    def click_button(self, elem, text_value):
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, f"//{elem}[contains(text(), '{text_value}')]")))
        except:
            raise Exception('Error locating specified button')
        else:
            if text_value == 'Create an account':
                time.sleep(1)
        buttons = self.driver.find_elements(by="xpath", value=f"//{elem}[contains(text(), '{text_value}')]")
        for button in buttons:
            try:
                button.click()
                if text_value == 'Send':
                    try:
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success alert-flat']")))
                    except:
                        raise Exception('Error submitting application')
                    else:
                        self.close_driver()
            except:
                continue

    def register(self):
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

    def login(self):
        try:
            self.click_button(elem = 'a', text_value = 'Sign in')
            self.complete_auth_form(action = 'Sign in')
        except:
            return

    def complete_auth_form(self, action):
        email_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
        email_field.clear()
        email_field.send_keys(self.email)
        time.sleep(0.1)
        password_field = self.driver.find_element(by="xpath", value="//input[@id='password']")
        password_field.clear()
        password_field.send_keys(self.password)
        self.click_button(elem = 'button', text_value = action)

    def refresh(self):
        if self.refresh_page == True:
            self.driver.refresh()
        else:
            raise Exception("Error refreshing page")

    def create_driver(self):
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = self.options)
    
    def close_driver(self):
        return self.driver.close()

    def apply(self, url):
        try:
            self.open_url_iframe(url = url)
            self.fill_personal_info()
            self.fill_work()
        except:
            return 'Error'
        else:
            return f'Successfully Applied to: {url}'