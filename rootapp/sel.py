from selenium import webdriver
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--headless")
from time import sleep

usr='sanchitcop19@gmail.com'
pwd='Scorpio97Scorpio97'
driver = webdriver.Chrome(options = chrome_options)
driver.implicitly_wait(8)
driver.get('https://www.facebook.com/')
print ("Opened facebook")

username_box = driver.find_element_by_id('email')
username_box.send_keys(usr)
print ("Email Id entered")

password_box = driver.find_element_by_id('pass')
password_box.send_keys(pwd)

print ("Password entered")
login_box = driver.find_element_by_id('loginbutton')
login_box.click()
print("Logging in...")
driver.get('https://www.facebook.com/rachel.mcperson.7')
print("Rachel's profile arrived")
add_friend = driver.find_elements_by_class_name('FriendRequestAdd')[0]
add_friend.click()
print ("Done")
input('Press anything to quit')
driver.quit()
print("Finished")
