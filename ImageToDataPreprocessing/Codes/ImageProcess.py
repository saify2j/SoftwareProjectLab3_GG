import cv2
import numpy as np
import glob
import os

def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = int(w * r), height
    else:
        r = width / float(w)
        dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation=inter)
def remove_object(immageToProcessPath):
    for filepath in glob.iglob(r'C:\Users\User\PycharmProjects\map_image_automation\Icons\*.png'):

        template = cv2.imread(filepath)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        # cv2.imshow("template", template)

        original_image = cv2.imread(immageToProcessPath)
        final = original_image.copy()
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        found = None

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            resized = maintain_aspect_ratio_resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            if resized.shape[0] < tH or resized.shape[1] < tW:
                break
            canny = cv2.Canny(resized, 50, 200)
            detected = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF)
            (_, max_val, _, max_loc) = cv2.minMaxLoc(detected)

            if found is None or max_val > found[0]:
                found = (max_val, max_loc, r)

        (_, max_loc, r) = found
        (start_x, start_y) = (int(max_loc[0] * r), int(max_loc[1] * r))
        (end_x, end_y) = (int((max_loc[0] + tW) * r), int((max_loc[1] + tH) * r))

        cv2.rectangle(original_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        # cv2.imshow('detected', original_image)

        cv2.rectangle(final, (start_x, start_y), (end_x, end_y), (255, 255, 255), -1)
        #cv2.imshow('result', final)
        # cv2.waitKey(0)

        cv2.imwrite(immageToProcessPath, final)
def segment_image(imagePath):
    # img = "mohakhali2.PNG"
    print(imagePath)
    img = imagePath
    image = cv2.imread(str(img))

    mask = cv2.threshold(image, 210, 255, cv2.THRESH_BINARY)[1][:, :, 0]
    dst = cv2.inpaint(image, mask, 7, cv2.INPAINT_NS)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #cv2.imshow('masked', mask)
    #cv2.waitKey(0)
    ############ For Yellow Color ############

    lower_yellow = np.array([10, 160, 240])
    upper_yellow = np.array([80, 250, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res_yellow = cv2.bitwise_and(image, image, mask=mask)
    #cv2.imwrite('yellow.png', res_yellow)

    ######### For Green Color##############
    # [ 51 127 174] [ 71 147 254]
    lower_blue = np.array([51, 127, 174])
    # upper_blue = np.array([145, 255, 255])
    upper_blue = np.array([71, 147, 254])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(image, image, mask=mask)
    #cv2.imwrite('green.png', res_blue)

    #########  For Red Color ###########
    # [  2 168 255] [ 22 188 255]
    # dark red [  0 184  89] [  0 204 169]
    # less dark red [  0 192 255] [  0 212 255]
    # lower_red = np.array([0, 184, 255])
    # upper_red = np.array([0, 204, 169])
    #
    # mask = cv2.inRange(hsv, lower_red, upper_red)

    # Range for lower red
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # Range for upper range
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Generating the final mask to detect red color
    mask = mask1 + mask2

    res_red = cv2.bitwise_and(image, image, mask=mask)
    #cv2.imwrite('red.png', res_red)
    # cv2.imshow('red',cv2.imread('messi_red.png'))
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    height, width, channels = image.shape

    res = res_red + res_blue + res_yellow
    for i in range(0, height):
        for j in range(0, width):
            a, b, c = res_red[i, j]
            if (a > 0 or b > 0 or c > 0):
                a, b, c = res_blue[i, j]
                if (a > 0 or b > 0 or c > 0):
                    a, b, c = res_blue[i, j]
                    if (a > 0 or b > 0 or c > 0):
                        res[i, j] = 0, 0, 0

    # res[:, 850:] = [0, 0, 0]
    # res[:, 0:640] = [0, 0, 0]
    # res[350:, :700] = [0, 0, 0]

    kernel = np.ones((20, 1), np.uint8)  # note this is a horizontal kernel
    d_im = cv2.dilate(res, kernel, iterations=1)
    e_im = cv2.erode(d_im, kernel, iterations=1)

    imageName = imagePath.split('\\')[-1]
    area_name = imageName.split('_')[0]
    savepath = f'G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Test Dataset\{area_name}\Cleaned'
    cv2.imwrite(os.path.join(savepath, imageName), res)
def calcPercentage(msk):
	'''
	returns the percentage of white in a binary image
	'''
	height, width = msk.shape[:2]
	num_pixels = height * width
	count_white = cv2.countNonZero(msk)
	percent_white = (count_white/num_pixels) * 100
	percent_white = round(percent_white,2)
	return percent_white

def image_to_text(imagePath):
    img = cv2.imread(imagePath)
    size = img.size
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([51, 127, 174])
    upper_blue = np.array([71, 147, 254])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('test',mask)
    # cv2.waitKey()
    # print('green:' + str(calcPercentage(mask)))
    green_val = str(calcPercentage(mask))

    lower_yellow = np.array([10, 160, 240])
    upper_yellow = np.array([80, 250, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #print('yellow/orange:' + str(calcPercentage(mask)))
    yellow_val = str(calcPercentage(mask))
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # Range for upper range
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Generating the final mask to detect red color
    mask = mask1 + mask2
    # print('red:' + str(calcPercentage(mask)))
    red_val = str(calcPercentage(mask))
    image_name = imagePath.split('\\')[-1]
    area_name = image_name.split('_')[0]
    date = image_name.split('_')[1]
    day = image_name.split('_')[2]
    time = image_name.split('_')[3]+ ':' +image_name.split('_')[4]+  ':' +image_name.split('_')[5].split('.')[0]
    total_string = area_name + ',' + date + ',' + day + ','+ time + ','+ green_val+','+ yellow_val +',' + red_val
    savepath = f'G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Test Dataset'
    f = open(os.path.join(savepath, area_name+'.txt'), "a+")
    # f.write(total_string)
    # f.write('\n')
    # print(total_string)

def main():
    #areas  = ['Uttara','Farmgate','Dhanmondi','Karwan Bazar','Sadarghat','Kalabagan','Mirpur 1','Mirpur 10','Shahbagh', 'Kamalapur', 'Tejgaon','Mohammadpur','Katabon']
    areas = ['Tejgaon', 'Mohammadpur', 'Katabon']
    #areas = ['Mohakhali2']
    for areaName in areas:
        fileNo = 1
        folderPath = f'G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Test Dataset\{areaName}\*.png'
        for filepath in glob.iglob(folderPath):
            # print(filepath)
            print(f'working on image {fileNo}')
            remove_object(filepath)
            segment_image(filepath)
        cleaned_path = f'G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Test Dataset\{areaName}\Cleaned\*.png'

        # for filepath in glob.iglob(cleaned_path):
        #     image_to_text(filepath)
        #     print(f'working on image {fileNo}')
if __name__ == "__main__":
    main()