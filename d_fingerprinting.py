#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 19:10:24 2021

@author: root
"""
# ============================ Import Packages ================================
from tensorflow import keras
import pandas as pd
import numpy as np
import pickle
from time import sleep

# ============================ Load the all saved files =======================
# load saved model
saved_model = keras.models.load_model('trained_model_200sig.h5')
saved_encoder = pickle.load(open("encoder.sav", "rb"))
saved_TP_probs = pickle.load(open("TP_probs.pkl", "rb"))

# =============================================================================


# ========================= Read the unknown signatures =======================
# read unknown signatures
print("Reading the unknown signatures")
unknown_data = pd.read_csv('demo.csv', header=None)
#print("unknown dataset: \n", unknown_data)

unknown_traffic_types = unknown_data.iloc[:, 300].unique()
#print("traffic types are", unknown_traffic_types)
unknown_classes = unknown_data.iloc[:, 301].unique()
print("no of devices are", len(unknown_classes), unknown_classes)
print("======================================================================")
sleep(1)
# get signatures
unknown_x = unknown_data.iloc[:, :200]
    # x.append(temp)
print("input: \n", unknown_x)

# get device ids
unknown_y = unknown_data.iloc[:, 301]
    # x.append(temp)
print("devices: \n", unknown_y)
print("======================================================================")
sleep(1)
# convert the mac id to number
unknown_y_dash=[]
for items in unknown_y:
    try:
        x = saved_encoder.transform([items])
    except:
        x = [-1]
    unknown_y_dash.append(x[0])  
#print(unknown_y_dash)

#  ============================================================================

# ============================== Predect unknown signatures ===================
# predect the classes based on unknown signatures
print("Predicting unknown signatures...")
pred_unknown = saved_model.predict(unknown_x)
pred_unknown_class = np.argmax(pred_unknown, axis=1)
prob_unknown = np.max(pred_unknown, axis=1)
#print("predected classes: ", pred_unknown_class)
print("======================================================================")

sleep(1)
# =============================================================================

# ========================== Load TP values for predect =======================
# get the TP values for corrosponding device ids
print("Loading True Positive values...")
print("======================================================================")

TPs = dict()
for items in unknown_classes:
    if items not in saved_TP_probs:
        TPs.setdefault(items, []).append([0])
        pass
    else:
        TPs.setdefault(items, []).append(saved_TP_probs[items])
sleep(1)

# ====================== Set the threashold ===================================
# threashold for devices 
print("Setting the acceptance threashold...")
threshold = dict()  
for item in TPs:
    # probs = TP_probs[item]
    percentile = np.percentile(TPs[item], 10)
    # probs = np.sort(probs)
    # index = round(0.2 * len(probs))
    threshold.setdefault(item, []).append(percentile)
print(threshold)
print("======================================================================")

sleep(1)
# =============================================================================
    
# ======================== fingerprinting the unknown devices =================
print("Validating unknown Signatures...")
detection = dict()
# check the closeness> the percentile of TPs
for i in range(len(unknown_y)):
    dev = unknown_y[i]
    if pred_unknown_class[i]==unknown_y_dash[i]:
        if prob_unknown[i]>=threshold[dev]:       
            print("signature", i, "belongs to device", pred_unknown_class[i])
            detection.setdefault(dev, []).append(1)
    else:
        print("signature", i, "belongs to an unknown device.")
        detection.setdefault(dev, []).append(0)
print("======================================================================")

sleep(1)
# ======================= device detection ====================================
# check which a device either known or unknown or compromised
for item in detection:
    values = detection[item]
    total = len(values)
    values, counts = np.unique(values, return_counts=True)
    index = counts.argmax()
    status = values[index]
    if status == 0:
        print(item, "is a unknown device")
    elif status == 1:
        print(item, "is a known device ")
  
 # ============================================================================   
