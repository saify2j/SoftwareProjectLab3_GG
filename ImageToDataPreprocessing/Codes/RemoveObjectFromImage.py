import cv2
import numpy as np
import glob

def  maintain_aspect_ratio_resize(image,  width=None,  height=None,  inter=cv2.INTER_AREA):
     dim =  None
     (h, w)  = image.shape[:2]
     if width is  None  and height is  None:
        return image
     if width is  None:
         r = height /  float(h)
         dim =  int(w * r), height
     else:
         r = width /  float(w)
         dim = (width,  int(h * r))
         return cv2.resize(image, dim,  interpolation=inter)


for filepath in glob.iglob(r'C:\Users\User\PycharmProjects\map_image_automation\Icons\*.png'):

    template = cv2.imread(filepath)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    #cv2.imshow("template", template)

    original_image = cv2.imread('test_for_doc_res_object_rem.PNG')
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
    #cv2.imshow('detected', original_image)

    cv2.rectangle(final, (start_x, start_y), (end_x, end_y), (255, 255, 255), -1)
    cv2.imshow('result', final)
    #cv2.waitKey(0)

    cv2.imwrite('test_for_doc_res_object_rem.PNG', final)