# [ 90  49 116] [110  69 196] grey objects
# [  0 146 255] [  0 166 255] red logo (hosp)
# [89 69 82] [109  89 162] text color range maybe
import cv2
import numpy as np
lower_grey = np.array([50,  19, 60])
upper_grey = np.array([120,  99, 206])

img = "test_for_doc2.PNG"
image = cv2.imread(str(img))

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

## mask of green (36,0,0) ~ (70, 255,255)
mask = cv2.inRange(hsv, lower_grey, upper_grey)
bak = image.copy()

# replace with red
bak[mask > 0] = (255, 255, 255)

lower_red = np.array([80,0,255])
upper_red = np.array([100,0,255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)


# lower_blue = np.array([ 0,146, 255] )
# upper_blue = np.array([ 0, 166, 255])
# blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

bak[mask1>0] = (255, 255, 255)
cv2.imwrite("test_for_doc_res2.PNG", bak)