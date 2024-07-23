#pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# pip install webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd


#setting up chrome options with specific arguments
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")

#setting up the chrome driver with WebDriverManager and options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

#creating the URL for the website using the current working directory
website = "https://allorizenproject1.netlify.app/"