########## SEGMENT IMAGE AND NOISE CANCELLATION
import numpy as np
import cv2

#img = "mohakhali2.PNG"
img = "test_for_doc_res_object_rem.PNG"
image = cv2.imread(str(img))

mask = cv2.threshold(image, 210, 255, cv2.THRESH_BINARY)[1][:, :, 0]
dst = cv2.inpaint(image, mask, 7, cv2.INPAINT_NS)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow('masked', mask)
cv2.waitKey(0)
############ For Yellow Color ############

lower_yellow = np.array([10, 160, 240])
upper_yellow = np.array([80, 250, 255])

mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
res_yellow = cv2.bitwise_and(image, image, mask=mask)
cv2.imwrite('yellow.png', res_yellow)

######### For Green Color##############
#[ 51 127 174] [ 71 147 254]
lower_blue = np.array([	51, 127, 174])
upper_blue = np.array([71, 147, 254])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
res_blue = cv2.bitwise_and(image, image, mask=mask)
cv2.imwrite('green.png', res_blue)

#########  For Red Color ###########
#[  2 168 255] [ 22 188 255]
#dark red [  0 184  89] [  0 204 169]
#less dark red [  0 192 255] [  0 212 255]
# lower_red = np.array([0, 184, 255])
# upper_red = np.array([0, 204, 169])
#
# mask = cv2.inRange(hsv, lower_red, upper_red)

# Range for lower red
lower_red = np.array([0,120,70])
upper_red = np.array([10,255,255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)

# Range for upper range
lower_red = np.array([170,120,70])
upper_red = np.array([180,255,255])
mask2 = cv2.inRange(hsv,lower_red,upper_red)

# Generating the final mask to detect red color
mask = mask1+mask2


res_red = cv2.bitwise_and(image, image, mask=mask)
cv2.imwrite('red.png',res_red)
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



cv2.imwrite(str("test_for_doc_res_object_rem_res.PNG"), res)

########## SEGMENT IMAGE AND NOISE CANCELLATION
