from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import base64
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier as dt
from sklearn.naive_bayes import GaussianNB as gnb
from sklearn import metrics
import pickle5 as pickle

# 1: load our dataset
df = pd.read_csv('dataset/flowers_features_json.csv')


# 2: convert encoded hog image features to multi d array
def decode_features(x):
    # get the encoded json dump
    enc = json.loads(x)
    # build the numpy data type
    data_type = np.dtype(enc[0])
    # decode the base64 encoded numpy array data and create a new numpy array with this data & type
    return np.frombuffer(base64.decodebytes(enc[1].encode('utf-8')), data_type).reshape(enc[2])


# hog images features
features = []


def append_features_2_list(x):
    # get the encoded json dump
    enc = json.loads(x)
    # build the numpy data type
    data_type = np.dtype(enc[0])
    # decode the base64 encoded numpy array data and create a new numpy array with this data & type
    image = np.frombuffer(base64.decodebytes(enc[1].encode('utf-8')), data_type).reshape(enc[2])
    features.append(image.flatten())


# 3: extract features and labels from our dataset
images = df['image'].apply(lambda x: decode_features(x))
hog = df['hog'].apply(lambda x: decode_features(x))
df['hog'].map(lambda x: append_features_2_list(x))
y = df['label'].to_numpy()
X = features

# convert labels to integer values
number = LabelEncoder()
y = number.fit_transform(y.astype('str'))

# 4: split our data to train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# show hog feature image for specific dataset row
plt.axis("off")
plt.imshow(hog[40], cmap="gray")
plt.show()
# show original image for specific dataset row
plt.axis("off")
plt.imshow(images[40], cmap="gray")
plt.show()

# 5: use KNN Classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn_y_pred = knn.predict(X_test)

# Its important to use binary mode
knnPickle = open('models/knnpickle_file', 'wb')
# source, destination
pickle.dump(knn, knnPickle)

print("Score KNN:", knn.score(X_train, y_train))
print("Report KNN:", metrics.classification_report(y_test, knn_y_pred))

# 6: use Decision Tree Classifier
dt_model = dt(random_state=1)
dt_model.fit(X_train, y_train)
dt_y_pred = dt_model.predict(X_test)

# Its important to use binary mode
dtPickle = open('models/dtickle_file', 'wb')
# source, destination
pickle.dump(dt_model, dtPickle)

print("Score DT:", dt_model.score(X_train, y_train))
print("Report DT:", metrics.classification_report(y_test, dt_y_pred))

# 7: use Naive Bayes Classifier
gnb_model = gnb()
gnb_model.fit(X_train, y_train)
gnb_y_pred = gnb_model.predict(X_test)
# Its important to use binary mode
nvPickle = open('models/gnbPickle_file', 'wb')
# source, destination
pickle.dump(gnb_model, nvPickle)

print("Score NV:", gnb_model.score(X_train, y_train))
print("Report NV:", metrics.classification_report(y_test, gnb_y_pred))
