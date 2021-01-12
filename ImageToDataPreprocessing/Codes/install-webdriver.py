from selenium import webdriver
import time
driver = webdriver.Chrome("C:\webdriver\chromedriver.exe")
driver.get('https://www.google.com/maps/place/%E0%A6%A4%E0%A7%87%E0%A6%9C%E0%A6%97%E0%A6%BE%E0%A6%81%E0%A6%93,+%E0%A6%A2%E0%A6%BE%E0%A6%95%E0%A6%BE/@23.7637175,90.3794455,15z/data=!3m1!4b1!4m5!3m4!1s0x3755c75f68e3e199:0x1091c4aa2634b568!8m2!3d23.759815!4d90.3913172'+'!5m1!1e1')
driver.maximize_window()


time.sleep(10)

driver.save_screenshot("screen.png")
print(driver.current_url)