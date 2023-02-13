from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Chrome\User Data")
options.add_argument(f"--profile-directory=Profile 1")
driver = webdriver.Chrome(executable_path='C:\chromedrivers\chromedriver.exe', options=options)
driver.maximize_window()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
driver.get('https://www.netflix.com/')