
import numpy as np
import cv2
########## DETECT LINES

inputImage = cv2.imread("test_for_doc_res_object_rem_res.PNG")
inputImageGray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(inputImageGray, 150, 200, apertureSize = 3)
minLineLength = 30
maxLineGap = 5
lines = cv2.HoughLinesP(edges,cv2.HOUGH_PROBABILISTIC, np.pi/180, 30, minLineLength,maxLineGap)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        #cv2.line(inputImage,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
        pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
        cv2.polylines(inputImage, [pts], True, (0,255,0))

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(inputImage,"Tracks Detected", (500, 250), font, 0.5, 255)
cv2.imwrite('final.png',inputImage)
cv2.imshow("Trolley_Problem_Result", inputImage)
#cv2.imshow('edge', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

########## DETECT LINES