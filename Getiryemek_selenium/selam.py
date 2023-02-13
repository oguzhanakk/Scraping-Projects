from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:/Users/oguzhann/AppData/Local/Google/Chrome/User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--profile-directory=Profile 3') #e.g. Profile 3
driver = webdriver.Chrome(executable_path=r'C:\path\to\chromedriver.exe', chrome_options=options)
driver.get("https://www.google.co.in")