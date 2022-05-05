# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 10:57:35 2021

@author: suman
"""

##############################################################################
# 1. Read the signatures saved in csv file
# 2. Get no. of traffic types and no. of devices.
# 3. A dataset list (dataset): for each traffic type a dataset will have in the list
#    (here we consider only icmp packets)
# 4. For each dataset: extract signatures in x and device id in y
# 5. Split the dataset into training and testing
# 6. Encode device ids into categorical(combination of 1 and 0)
# 6. define the model
# 7. Train and evaluate the model
# 8. Save the model
##############################################################################

# =============================== Packges =====================================
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import pickle

# =============================================================================

# ===================== Import the training set ===============================
# Load the data
original_data = pd.read_csv('udp_pic6_1400_pi6a_64_pi79_56_pc7b_56_pi09_56_pie1_84.csv', header=None)
print("========================================================================")
print("Reading the training datasetset...")
#print("original dataset: \n", original_data)

# per traffic type dataset
traffic_types = original_data.iloc[:, 300].unique()
print("========================================================================")
print("traffic types are", traffic_types)
classes = original_data.iloc[:, 301].unique()
print("========================================================================")
print("no of devices are", len(classes), classes)
print("========================================================================")

x = original_data.iloc[:, :200]
print("input: \n", x)

y = original_data.iloc[:, 301]
print("labels:\n", y)

# =============================================================================

# ========================= Split =============================================
# split dataset to train test
Xtrain, Xtest, Ytrain, Ytest = train_test_split(x, y, test_size=0.2, random_state=100)

print("========================================================================")
print("Shuffling the training data...")
print("xtrain data:\n", Xtrain)
print("ytrain data:\n", Ytrain)

# ============================= Encoder =======================================
# convert IDs to onehot
encoder = LabelEncoder()
y_dash = encoder.fit_transform(Ytrain)
print(y_dash.shape)
ytr = to_categorical(y_dash)
print("========================================================================")
print("Encoding the the labels...")
print("after encoding ids: \n", ytr, "\n", ytr.shape)

y_dash = encoder.transform(Ytest)
print(y_dash.shape)
yts = to_categorical(y_dash)
#print("after encoding ids: \n", yts, "\n", yts.shape)

 # save the encoder
filename = 'encoder.sav'
pickle.dump(encoder, open(filename, 'wb'))

# ============================================================================= 

# ========================= Ann model =========================================
# ANN model
model = Sequential()
model.add(Dense(300, activation='sigmoid', input_dim=200))
model.add(Dense(100, activation='sigmoid'))
model.add(Dense(50, activation='sigmoid'))
model.add(Dense(len(classes), activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print("========================================================================")
# train the model
history = model.fit(Xtrain, ytr, epochs=300, batch_size=4, validation_split=0.2)

#testing accuracy
_, accur = model.evaluate(Xtest, yts)
print("test accuracy:", accur)

# save the model
model.save('trained_model_200sig.h5')
print("========================================================================")

# =============================================================================

# ======================= Save true positive values ===========================
# predict the model using training set to store the TP
pred_train = model.predict(Xtrain)
train_class = np.argmax(ytr, axis=1)
pred_train_class = np.argmax(pred_train, axis=1)


# how many predected classes are right(True Positive) and store there probablities 
TP_probs = dict()
count_test = 0
for i in range(len(train_class)):
    if train_class[i] == pred_train_class[i]:
        count_test += 1
        prob = pred_train[i][pred_train_class[i]]
        dev = encoder.inverse_transform([pred_train_class[i]])
        TP_probs.setdefault(dev[0], []).append(prob)
print("total", count_test, "True Positives of", len(train_class))

# save the TPs
file = open("TP_probs.pkl", "wb")
pickle.dump(TP_probs, file)
file.close()

# =============================================================================
# # set the threashold
# pred_classes = []
# for i in range(len(pred_class)):
#     prob = pred[i][pred_class[i]]
#     if float(prob)>=0.10:
#         pred_classes.append(pred_class[i])
#     else:
#         pred_classes.append(-1)
#            
# =============================================================================


# for each traffic type a dataset will be stored
# =============================================================================
# dataset = []
# for items in range(len(traffic_types)):
#     d = original_data[original_data[300] == traffic_types[items]]
#     dataset.append(d)
# 
# print(dataset[0])
# =============================================================================
  
# print("after encoding ids: \n", unknown_y_dash)



# =============================================================================
# pred_unknown = model.predict(unknown_x.iloc[0:20,:])
# pred_unknown_class = np.argmax(pred_unknown, axis=1)
# prob_unknown = np.max(pred_unknown, axis=1)
# =============================================================================

# get 90th percentile element from TP probablities
      
        
    # elif status == -1:
    #     print(item, "is may be a compromised device ")
    

# =============================================================================
# # save the probablity for detect unknown devices
# devices = yts[200:210]
# pred_dev
# prob = pred * devices
# for i in range(len(pred_class)):
#     prob[i] = pred[i][pred_class[i]]
# 
# =============================================================================


# =============================================================================
# _, accur = new_model.evaluate(Xtest, Ytest)
# print("test accuracy:", accur)
# =============================================================================

# =============================================================================
# new_pred = new_model.predict(Xtest.iloc[50:70,])
# test_class = np.argmax(Ytest[50:70], axis=1)
# new_pred_class = np.argmax(new_pred, axis=1)
# =============================================================================
