import cv2
import numpy as np
import glob
import os
def findInit(w,h):
    for j in range (0,h):
        for i in range (0,w):
            if(mask_red[j,i]>0 or mask_blue[j,i]>0 or mask_yellow[j,i]>0):
                return j

def findFinish(w,h):
   last = -1
   for j in range (0,h):
        for i in range (0,w):
            if(mask_red[j,i]>0 or mask_blue[j,i]>0 or mask_yellow[j,i]>0):
                last = j
   return last

def definePixels(s,f,w, areaName):
   print(s,f)
   pixelFileName = f'{areaName}-pixels.txt'
   fi= open(pixelFileName,"a+")
   for j in range (s,f):
        for i in range (0,w):
             if(mask_red[j,i]>0 or mask_blue[j,i]>0 or mask_yellow[j,i]>0):
                 fi.write(str(j))
                 fi.write(',')
                 fi.write(str(i))
                 fi.write('\n')
def process_minute_time(minute_time):
    if(int(minute_time)>0 and int(minute_time)<15) :
        return '00'
    elif(int(minute_time)>15 and int(minute_time)<30):
        return '15'
    elif (int(minute_time) > 30 and int(minute_time) < 45):
        return '30'
    elif (int(minute_time) > 45 and int(minute_time) < 59):
        return '45'
    else:
        return minute_time
def process_day(day):
    switcher = {
         "Saturday":0,
         "Sunday" :1,
         "Monday":2,
         "Tuesday":2,
         "Wednesday":2,
         "Thursday":1,
         "Friday":0
    }
    return switcher.get(day, "ERROR")
def process_holiday(day):
    if(day =='Friday' or day =='Saturday'):
        return 1
    else:
        return 0

imageNo = 1
areas = ['Tejgaon', 'Mohammadpur', 'Katabon']
#areas  = ['Uttara','Farmgate','Dhanmondi','Karwan Bazar','Sadarghat','Kalabagan','Mirpur 1','Mirpur 10','Shahbagh', 'Kamalapur','Tejgaon','Mohammadpur','Katabon']
for area in areas:
    print(f'Doing area {area}\n')
    arename = area
    folderPath = f'G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Test Dataset\{arename}\Cleaned\*png'
    # imagePath = f'G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Test Dataset\Mohakhali\Cleaned\Mohakhali_Thursday_04022021_10_10_21.png'
    pixel_define_done =0
    for imagePath in glob.iglob(folderPath):
        #print(imagePath)
        print(f'Reading image no {imageNo}')
        imageNo+=1
        inputImage = cv2.imread(imagePath)
        height, width, channels = inputImage.shape
        hsv = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([10, 160, 240])
        upper_yellow = np.array([80, 250, 255])

        lower_blue = np.array([51, 127, 174])
        upper_blue = np.array([71, 147, 254])

        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # Range for upper range
        lower_red = np.array([170, 120, 70])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)
        mask_red = mask1 + mask2
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        start = findInit(width,height)
        finish = findFinish(width,height)
        #print(f'Start {start} === Finish {finish}')
        if(pixel_define_done == 0):
            definePixels(start, finish, width,arename)
            pixel_define_done = 1

        # inputImage1 = inputImage
        # with open('pixels.txt', 'r') as file:
        #     # read a list of lines into data
        #     data = file.readlines()
        # for line in range (0,len(data)):
        #     X = int(data[line].split(",")[0])
        #     Y = int(data[line].split(",")[1])
        #     inputImage1[X,Y] = (215,84,247)
        # cv2.imshow('test',inputImage1)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        csvFileName = arename +'-test-final.csv'
        f = open(csvFileName, "a+")
        Colored_Pixels = []
        imgNo = 0
        seg = 1
        image_name = imagePath.split('\\')[-1]
        area_name = image_name.split('_')[0]
        date = image_name.split('_')[2]
        day = image_name.split('_')[1]
        #print(day)
        #test = input()
        time = image_name.split('_')[3] + '.' + process_minute_time(image_name.split('_')[4])
        total_string = '1,'+ str(process_holiday(day))+','+ str(process_day(day)) + ',' + time + ','
        #print(total_string)
        f.write(total_string)
        #test = input("wait")
        for j in range(start, height, 40):
            #
            # print(j)
            red = 0
            blue = 0
            yellow = 0
            for k in range(j, j + 40):
                for i in range(0, width):
                    if (k > finish):
                        break
                    if (mask_red[k, i] > 0):
                        red = red + 1
                        if (imgNo == 1):
                            Colored_Pixels.append([k, i])

                    if (mask_blue[k, i] > 0):
                        blue = blue + 1
                        if (imgNo == 1):
                            Colored_Pixels.append([k, i])

                    if (mask_yellow[k, i] > 0):
                        yellow = yellow + 1
                        if (imgNo == 1):
                            Colored_Pixels.append([k, i])

            #          print("Seg-->",seg,red,"  ",blue," ",yellow,"\n")
            if (yellow > red and yellow > blue):
                f.write("Y,")
            elif (red > yellow and red > blue):
                f.write("R,")
            elif (blue > red and blue > yellow):
                f.write("G,")
            #          else:
            #              print("Image ",imgNo," Segment ",seg, "kisu korte pari nai")
            seg = seg + 1
        f.write('\n')
        f.close()

    #print(seg)