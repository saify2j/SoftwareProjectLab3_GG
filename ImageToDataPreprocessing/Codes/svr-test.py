import cv2
import pandas as pd
import numpy as np  # linear algebra
from pprint import  pprint
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

dataset = pd.read_csv('data.csv')
pos = 3
X = dataset.iloc[:, 2:3]
# pprint(X)
# Y = dataset.iloc[:,pos+1]
predictions = []
for pos in range(4, 14):
    Y = dataset.iloc[:, pos]
    pprint(Y)
    #    pos = pos+1
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
    # test_size: if integer, number of examples into test dataset; if between 0.0 and 1.0, means proportion
    #    print('There are {} samples in the training set and {} samples in the test set'.format(X_train.shape[0], X_test.shape[0]))

    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import cross_val_score

    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)

    from sklearn.svm import SVC, SVR

    svm = SVR(kernel='rbf', random_state=0, gamma=.10, C=1.0)
    svm.fit(X, Y)
    print('The accuracy of the SVM classifier on training data is {:.2f}'.format(svm.score(X_train_std, y_train)))
    print('The accuracy of the SVM classifier on test data is {:.2f}'.format(svm.score(X_test_std, y_test)))
