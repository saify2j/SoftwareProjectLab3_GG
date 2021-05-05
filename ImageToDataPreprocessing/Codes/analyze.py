import sys
import os
import base64
from pathlib import Path
dir = os.path.dirname(__file__)

area_input = str(sys.argv[1])
day_input = str(sys.argv[2])
time_input = str(sys.argv[3])

dir = os.path.dirname(__file__)
import cv2
import pandas as pd
import numpy as np  # linear algebra
from sklearn.model_selection import train_test_split
from pprint import pprint
from sklearn.metrics import confusion_matrix

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
fileToReadCSV = f'{area_input}-test-final.csv'
fullCSVPath = "G:\SPL3Repo\SoftwareProjectLab3_GG\TrafficAnalyzerUI\\bin\Debug\Dataset_CSV\\"+fileToReadCSV
csvFilePath = os.path.join(dir, fullCSVPath)
dataset = pd.read_csv(fullCSVPath, sep=',', error_bad_lines=False)
pos = 3
X = dataset.iloc[:, :4]
predictions = []
for pos in range(4, dataset.shape[1]):
    Y = dataset.iloc[:, pos]
    #    pos = pos+1
    # print(Y)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
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
    timeToPredict = 0.00
    tmp = []
    for i in range(0, 13):
        tmp.append(knn.predict([[1,process_holiday('Sunday'), process_day('Sunday'), timeToPredict]]))
        timeToPredict += 2.00
    predictions.append(tmp)
summations = []
for i in range(0, 13):
    summations.append(0)

#print(predictions)
for i in range(0, 13):
    for j in range(0, 21):
        if (predictions[j - 1][i] == 'Y'):
            summations[i] += 2
        if (predictions[j - 1][i] == 'R'):
            summations[i] += 3
        if (predictions[j - 1][i] == 'G'):
            summations[i] += 1
labels = ['00:00','02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00','18:00','20,00','22.00', '23.59']
import matplotlib.pyplot as plt
import io
import urllib, base64
#print(len(summations))
plt.bar(labels,summations)

plt.title('Traffic Intensity Per Day')
plt.xlabel('Time')
plt.ylabel('Traffic Intensity')
#plt.show()
fig = plt.gcf()
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
string = base64.b64encode(buf.read()).decode("utf-8")
print(string)





