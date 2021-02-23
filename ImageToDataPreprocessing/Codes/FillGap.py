# from skimage import io, morphology, img_as_bool, segmentation
# from scipy import ndimage as ndi
# import matplotlib.pyplot as plt
#
# image = img_as_bool(io.imread('../Images/satImageTest.PNG'))
# out = ndi.distance_transform_edt(~image)
# out = out < 0.05 * out.max()
# out = morphology.skeletonize(out)
# out = morphology.binary_dilation(out, morphology.selem.disk(1))
# out = segmentation.clear_border(out)
# out = out | image
#
# plt.imshow(out, cmap='gray')
# plt.imsave('../tmp/gaps_filled.png', out, cmap='gray')
# plt.show()
import numpy as np
import cv2
res = cv2.imread("test_for_doc_res.PNG")

#test 1
# # define kernal value
# kernel = np.ones((2, 2), np.uint8)
#
# # grayscale
# gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
#
# dilate = cv2.dilate(gray, kernel, iterations=1)
# dilate1 = cv2.dilate(dilate, kernel, iterations=1)
#
# dilate1 = cv2.morphologyEx(dilate1, cv2.MORPH_OPEN, kernel)
#
# # Canny
# canny = cv2.Canny(dilate1, 160, 160, 3)
#
# dilate = cv2.dilate(canny, kernel, iterations=1)
#
# # Gaussian Blurring
# blur = cv2.GaussianBlur(dilate, (5, 5), 0)
# erode = cv2.dilate(blur, kernel, iterations=1)
# blur = cv2.GaussianBlur(erode, (5, 5), 1)
#
# blur = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
# ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
#
# blur = cv2.GaussianBlur(thresh, (5, 5), 1)
# ret1, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
#
# opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
#
# #cv2.imwrite('opening.jpg', opening)
#
# #contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# test 2
# frame = res.copy()
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# gray = cv2.blur(gray, (5,5))
# gray = cv2.bilateralFilter(gray, 11, 17, 17) #blur. very CPU intensive.
# cv2.imshow("Gray map", gray)
#
# edges = cv2.Canny(gray, 30, 120)
#
# cv2.imshow("Edge map", edges)
#
# #find contours in the edged image, keep only the largest
# # ones, and initialize our screen contour
# # use RETR_EXTERNAL since we know the largest (external) contour will be the card edge.
# _, cnts, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
# screenCnt = None
#
# # loop over our contours
# for c in cnts:
#     # approximate the contour
#     peri = cv2.arcLength(c, True)
#     approx = cv2.approxPolyDP(c, 0.3 * peri, True)
#
#     cv2.drawContours(res, [cnts[0]], -1, (0, 255, 0), 2)
#
#     # if our approximated contour has four points, then
#     # we can assume that we have found our card
#     if len(approx) == 4:
#         screenCnt = approx;
#     break
#
#
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
# dilated = cv2.dilate(res, kernel)
# eroded=cv2.erode(dilated,kernel)

#test 3
import cv2
import numpy as np

img = cv2.imread("test_for_doc_res_object_rem_res.PNG")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,120)
minLineLength = 20
maxLineGap = 5
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow("edges", edges)
cv2.imshow("lines", img)
cv2.waitKey()
cv2.destroyAllWindows()

