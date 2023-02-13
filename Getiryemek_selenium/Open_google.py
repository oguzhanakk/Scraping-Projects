from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir=C:/Users/oguzhann/AppData/Local/Google/Chrome/User Data")
options.add_argument(f"--profile-directory=Profile 2")

options.add_argument('--no-sandbox')
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get('https://getbootstrap.com/')
time.sleep(10)
print(driver.title)
driver.close()
