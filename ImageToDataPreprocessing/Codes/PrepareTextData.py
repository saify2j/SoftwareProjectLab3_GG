import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

# path = [cv2.imread(file) for file in glob.glob("F:/Projects/Python Project/Images/*.png")]

lower_yellow = np.array([10, 160, 240])
upper_yellow = np.array([80, 250, 255])


lower_blue = np.array([	51, 127, 174])
#upper_blue = np.array([145, 255, 255])
upper_blue = np.array([71, 147, 254])

# Range for lower red
lower_red1 = np.array([0,120,70])
upper_red1 = np.array([10,255,255])

# Range for upper range
lower_red = np.array([170,120,70])
upper_red = np.array([180,255,255])

images = []

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


f = open("inter4.txt", "a+")
# pixels = open("pixels3.txt","a+")
Colored_Pixels = []

imgNo = 0

for img in glob.glob("G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Codes\TextualData\*.PNG"):
    print("Reading image no ", imgNo)
    imgNo += 1
    #    if(imgNo==2):
    #        break
    inputImage = cv2.imread(str(img))
    #    if(str(img).find("Sep")==-1):
    #        continue

    arr = str(img)[:-4].split('_')
    print(arr)
    arr1 = arr[0][8:].split(' ')
    #    if(arr[1]!='Fri'):
    #        continue
    f.write('\n')
    f.write(arr1[0])
    f.write(",")
    f.write(arr[4])
    f.write(",")
    if (arr[4].find('Fri') or arr[4] == 'Sat'):
        f.write("Yes,")
    else:
        f.write("No,")
    f.write(arr[4])
    f.write(',')


    hsv = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)

    maskred1 = cv2.inRange(hsv, lower_red1, upper_red1)
    maskred2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_red = maskred1 + maskred2
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    inputImageGray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    seg = 1
    height, width, channels = inputImage.shape

    start = findInit(width, height)
    finish = findFinish(width, height)

    for j in range(start, height, 40):
        #          print(j)
        red = 0
        blue = 0
        yellow = 0
        for k in range(j, j + 40):
            for i in range(0, width):
                if (k > height):
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
            f.write("B,")
        seg = seg + 1

f.close()
# pixels.close()


# pixels = open("pixels2.txt","a+")
#
# for i in range(0,len(Colored_Pixels)):
#    pixels.write(str(Colored_Pixels[i][0])+","+str(Colored_Pixels[i][1])+"\n") 
# pixels.close()