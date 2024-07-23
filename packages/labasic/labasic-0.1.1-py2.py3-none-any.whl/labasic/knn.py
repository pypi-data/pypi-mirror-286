#Module Importing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')
# Dataset creation, centers = classes, n_features = characteristics (Changed dataset)
X, y = make_blobs(n_samples = 790, n_features = 5, centers = 2, cluster_std = 3.5, random_state = 10)
#Dataset visualization
plt.figure(figsize = (10,10))
plt.scatter(X[:,0], X[:,1], c=y, s=100,edgecolors = 'black')
plt.show()
#Splitting data into training and testing set, 75% for the train set and 25% for the test set (Changed random state from 0 to 4)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 4)
# KNN implementation, Two variants (Changed neighbors)
knn3 = KNeighborsClassifier(n_neighbors = 3)
knn7 = KNeighborsClassifier(n_neighbors=7)
# Predictions for KNN Classifiers (n=3,7)
knn3.fit(X_train, y_train)
knn7.fit(X_train, y_train)
# Accuracy prediction
y_pred_3 = knn3.predict(X_test)
y_pred_7 = knn7.predict(X_test)
from sklearn.metrics import accuracy_score
print("Accuracy with k=3", accuracy_score(y_test, y_pred_3)*100)
print("Accuracy with k=7", accuracy_score(y_test, y_pred_7)*100)
# Predictions visualization
plt.figure(figsize = (15,5))
plt.subplot(1,2,1)
plt.scatter(X_test[:,0], X_test[:,1], c=y_pred_3, marker= '*', s=100,edgecolors='black')
plt.title("Predicted values with k=3", fontsize=20)

plt.subplot(1,2,2)
plt.scatter(X_test[:,0], X_test[:,1], c=y_pred_7, marker= '*', s=100,edgecolor= 'black')
plt.title("Predicted values with k=7", fontsize=20)
plt.show()