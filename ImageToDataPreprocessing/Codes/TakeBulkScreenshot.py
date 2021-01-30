from selenium import webdriver
from datetime import datetime
import os
import time
from PIL import Image

areas = ['Mohakhali', 'Gulshan', 'Uttara']
driver = webdriver.Chrome("C:\webdriver\chromedriver.exe")
driver.get('https://www.google.com/maps/@23.7985053,90.3754991,15z/data=!5m1!1e1')
driver.maximize_window()
path = 'G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Dataset'


# Check whether the
# specified path is an
# existing directory or not

for area in areas:
    searchbar = driver.find_element_by_id("searchboxinput")
    searchbar.clear()
    searchbar.send_keys(str(area))
    searchbutton = driver.find_element_by_id("searchbox-searchbutton").click()
    driver.set_window_size(2560, 1440)
    driver.execute_script("document.body.style.zoom='120 %'")

    now = datetime.now()
    date_time = now.strftime("%d%m%Y%H_%M_%S")

    time.sleep(3)
    fileName = str(area)+date_time+".png"
    pathtoSave = path+"\\"+area
    isdir = os.path.isdir(pathtoSave)
    #fileName = os.path.join(pathtoSave, fileName)
    if(isdir):
        print("Path found");
        print(fileName)
        driver.save_screenshot(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), pathtoSave, fileName))
        #driver.save_screenshot(fileName)
    time.sleep(3)



    # open the image using Pillow
    # test_image = 'Images/' + fileName
    # original = Image.open(test_image)
    #
    # width, height = original.size  # Get dimensions
    # left = width / 3
    # top = 0
    # right = width
    # bottom = height
    # cropped_example = original.crop((left, top, right, bottom))
    #
    # cropped_example.save('Images/' + fileName)