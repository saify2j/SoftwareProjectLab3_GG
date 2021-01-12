
########## TAKE IMAGE SCREEN SHOT

from selenium import webdriver
import time
from PIL import Image
areas = ['Mohakhali', 'Gulshan']
area = 'Mohakhali'
driver = webdriver.Chrome("C:\webdriver\chromedriver.exe")
driver.get('https://www.google.com/maps/@23.7985053,90.3754991,15z/data=!5m1!1e1')
driver.maximize_window()
searchbar = driver.find_element_by_id("searchboxinput")
searchbar.send_keys(str(area))
searchbutton = driver.find_element_by_id("searchbox-searchbutton").click()
driver.set_window_size(2560, 1440)
driver.execute_script("document.body.style.zoom='120 %'")
#driver.execute_script("document.body.style.zoom='250%'")
time.sleep(10)
fileName = str(area) + str(time.time())+".png"
driver.save_screenshot('Images/'+fileName)


# open the image using Pillow
test_image = 'Images/'+fileName
original = Image.open(test_image)


width, height = original.size   # Get dimensions
left = width/3
top = 0
right = width
bottom = height
cropped_example = original.crop((left, top, right, bottom))

cropped_example.save('Images/'+fileName)
#for area in areas:



    #print(driver.current_url)

########## TAKE IMAGE SCREEN SHOT
