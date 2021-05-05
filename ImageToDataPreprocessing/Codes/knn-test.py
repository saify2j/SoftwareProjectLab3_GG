import cv2
import pandas as pd
import numpy as np  # linear algebra
from sklearn.model_selection import train_test_split
from pprint import pprint
from sklearn.metrics import confusion_matrix
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
dataset = pd.read_csv(r'Gulshan-test-final.csv', sep=',', error_bad_lines=False)
pos = 3
X = dataset.iloc[:, :4]
# Y = dataset.iloc[:,pos+1]
predictions = []
# print(X)
print(dataset.shape[1])
for pos in range(4, dataset.shape[1]):
    Y = dataset.iloc[:, pos]
    #    pos = pos+1
    # print(Y)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
    # test_size: if integer, number of examples into test dataset; if between 0.0 and 1.0, means proportion
    #    print('There are {} samples in the training set and {} samples in the test set'.format(X_train.shape[0], X_test.shape[0]))

    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import cross_val_score

    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)

    # Applying Knn
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score

    knn = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
    # knn.fit(X_train_std, y_train)
    knn.fit(X, Y)
    #predicted = knn.predict([[1,1,0,21.30]]);
    #acc = accuracy_score(Y, predicted)
    predictions.append(knn.predict([[1,0,2,10.15]]))
    #predictions.append(knn.predict([[3, 0, 2, 10.00]]))

print('The accuracy of the Knn  classifier on training data is {:.2f}'.format(knn.score(X_train_std, y_train)))
print('The accuracy of the Knn classifier on test data is {:.2f}'.format(knn.score(X_test_std, y_test)))
#print(type(predictions))
pprint(predictions)

inputImage = cv2.imread("Gulshan_Tuesday_02022021_15_15_27.png")
inputImage1 = inputImage
areaName = 'Gulshan'
pixel_file_name = f'{areaName}-pixels.txt'
with open(pixel_file_name, 'r') as file:
    # read a list of lines into data
    data = file.readlines()
seg = 0
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

start = findInit(width, height)
finish = findFinish(width, height)
# definePixels(start,finish,width)
print(len(predictions))

for line in range(0, len(data)):
    X = int(data[line].split(",")[0])
    Y = int(data[line].split(",")[1])
    seg = -1
    for f in range(0, 21):
        if (X >= start + 40 * f and X < start + 40 * (f + 1)):
            seg = f
    if (seg == -1):
        seg = 9

    if (predictions[seg] == 'Y'):
        inputImage1[X, Y] = (0, 255, 255)
    if (predictions[seg] == 'R'):
        inputImage1[X, Y] = (255, 0, 0)
    if (predictions[seg] == 'G'):
        inputImage1[X, Y] = (0, 0, 0)
    if (len(data) % 50 == 0):
        print("Working on line ", line)

# inputImage1 = inputImage
# for i in range(0,100):
#    for j in range(0,100):
#        inputImage1[i,j]=(0,0,0)
#
cv2.imshow('final', inputImage)
cv2.waitKey(0)
cv2.destroyAllWindows()

   # predicted = knn.predict([[3,0,2,12.25]]);
   # acc = accuracy_score(Y, predicted)
   #
   #
   # print('The accuracy of the Knn  classifier on training data is {:.2f}'.format(knn.score(X_train_std, y_train)))
   # print('The accuracy of the Knn classifier on test data is {:.2f}'.format(knn.score(X_test_std, y_test)))

