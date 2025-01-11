import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


load_dotenv("./examples/autoclick/.env")


login = str(os.environ.get("mail"))
password = str(os.environ.get("password"))


class Brow:
    def __init__(self):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument("--disable-blink-features=AutomationControlled") 
        driver = webdriver.Chrome(options=options)
        self.driver = driver

    def __del__(self):
        self.driver.close()

    def auth(self):
        self.driver.get("https://lk.sut.ru/cabinet")
        elem = self.driver.find_element(By.NAME, "users")
        elem.clear()
        elem.send_keys(login)
        
        elem = self.driver.find_element(By.NAME, "parole")
        elem.clear()
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        
        elem = self.driver.find_element(By.NAME, "logButton")
        elem.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(6) # seconds
    
    def get_token(self):
        self.auth()
        token = self.driver.get_cookie("miden")["value"]
        time.sleep(0.25)
#         self.driver.close()
        return token
