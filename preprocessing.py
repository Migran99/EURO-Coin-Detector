########################
#
#      --- - Data Preprocessing for the EURO Coin Detector - ---
#   
#
#                   Miguel Granero Ramos 2021
####

import numpy as np
import os
import cv2
import pickle
import tensorflow as tf
import time
from tensorflow.python.keras.backend import learning_phase
import coinDetector as cd
import matplotlib.pyplot as plt

def changeBackground(img, originalColor, goalColor):
    
    new = np.zeros(img.shape)
    new[:] = goalColor
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low = originalColor[0]
    high = originalColor[1]
    mask = cv2.inRange(hsv,low,high)

    res = cv2.bitwise_and(img, img, mask = mask)
    fg = img - res
    fg = np.where(fg == 0, new, fg)
    fg = cv2.convertScaleAbs(fg)
    return fg

def convertDataset(CATEGORIES, DIRECTORY):
    lowH = 90
    highH = 120
    background = [(lowH/360*255,-1,-1),(highH/360*255,256,256)]
    for category in CATEGORIES:
        path = os.path.join(DIRECTORY, category)
        if(not os.path.isdir('dataset/'+category)):
            print(path,' does not exist')
            os.mkdir('dataset/'+category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img))
                img_array = changeBackground(img_array,background,(0,0,0))
                coins = cd.getCoins(img_array)
                c = cd.processCoins(img_array,coins,path='dataset/'+category+'/'+img, save=True)
                #print(len(c))
            except Exception as e:
                print(e)
    


def create_data(CATEGORIES, DIRECTORY, N):
    '''
    Parse the data
    '''
    IMG_SIZE = 128
    X = []
    y = []
    for category in CATEGORIES:
        path = os.path.join(DIRECTORY, category)
        class_num_label = CATEGORIES.index(category)
        n = 0
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img))
                img_array = cv2.resize(img_array, (IMG_SIZE,IMG_SIZE))
                X.append(img_array)
                y.append(class_num_label)
                n += 1
                if(n >= N):
                    break
            except Exception as e:
                pass
    return X,y


def flattenImages(X):
    flat = []
    for i in X:
        x = np.array(X)
        flat.append(x.flatten())

    return flat

def saveData(X,y,data, path="output"):
    '''
    Saves the data to be used by the ANN
    '''
    pickle_out = open(path+"/X.pickle", "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open(path+"/y.pickle", "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()

    pickle_out = open(path+"/data.pickle", "wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()


if __name__ == "__main__":
    DIRECTORY = "dataset" # Windows/PC
    CATEGORIES = ['1c', '1e', '2c','2e','5c','10c','20c','50c']  
    #print('Converting Dataset')
    #convertDataset(CATEGORIES,DIRECTORY)
    print('Creating data structure')
    features = []
    X, y = create_data(CATEGORIES,'train',2000)
    #features = flattenImages(X)
    print("Features length: ", len(features))
    print("X length: ", X[0].shape)
    print("y length: ", len(y))
    print('DONE!!')
    #classification(X,y,model)
    saveData(X,y,features)