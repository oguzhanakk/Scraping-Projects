from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service('C:\chromedrivers\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users/oguzhann/AppData/Local/Google/Chrome/User Data")
options.add_argument("--profile-directory=Profile 3")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--headless')
#options.add_argument('--remote-debugging-port=9222')

# Chrome tarayıcısını açmak için ayarları kullanın
driver = webdriver.Chrome(service=service, options=options)

# Tarayıcıyı maksimize etmek için ayrıca şu kodu kullanabilirsiniz:
driver.maximize_window()

# Belirtilen URL'yi açmak için şu kodu kullanın:
driver.get('https://www.netflix.com/')
