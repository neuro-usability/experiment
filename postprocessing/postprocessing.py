# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
    
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn import svm
import pydotplus
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA
import scipy.spatial

path = '/home/jan/Affectiva API/data/'
# set to 0 if not wanted
outlierDetection = 1
# how many data points should be deleted?
outlierRate = 0.1

# function to get a flat structure
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[str(name[:-1])] = str(x)

    flatten(y)
    return out

# convert json data in for ML suitable form
def get_training_data(path):
    dataMatrix = []
    dataColumn = []
    labels = []
    # for all persons
    for filename in os.listdir(path):
        with open(path+filename) as data_file:    
            person = json.load(data_file)
            # for all emojis
            for emoji in person:
                # for all measurements
                for measurement in person[emoji]:
                    # for all objects
                    for dataObject in measurement:
                        del dataObject["emojis"]["dominantEmoji"]
                        flatObject = flatten_json(dataObject)
                        # for all individual values
                        for key, value in flatObject.items():
                            dataColumn.append(float(value))
                        if dataMatrix == []:
                            dataMatrix = dataColumn
                            labels.append(emoji)
                        else:
                            dataMatrix = np.vstack((dataMatrix, dataColumn))
                            labels.append(emoji)
                        dataColumn = []
    return (dataMatrix, labels)

# Outlier detection
def gammaidx(X, k):
    #check input variable k; matrix is assumed to be in suitable shape
    if k < 1 or k > len(X):
        raise ValueError('Number of k nearest neighbors (k) not within the range (1, %d).\n' %len(X))
    #initialize y
    y = np.zeros(X.shape[0])
    #calculates vector-form distance vector
    dist = scipy.spatial.distance.pdist(X, 'euclidean')
    #converts the vector-form distance vector to a square-form distance matrix
    dist = scipy.spatial.distance.squareform(dist)
    #set diagonal distance to infinite as it is the distance of the point to itself 
    np.fill_diagonal(dist, float('inf'), wrap=False)
    #sort the indices of all points by distance descending
    #cut the matrix to k entrys for each data point
    idx = np.argsort(dist)[:,:k]
    #creates row vector with range(X.shape[0]) indices
    #for being able to easily access the values from the dist matrix
    rowIdx = np.arange(X.shape[0]).reshape(X.shape[0],1)
    #calculates mean over coloums
    y = np.mean(dist[rowIdx,idx], axis=1)
    return y    
    

# get data
(X, Y) = get_training_data(path)
# get names of predictors
from flattenedObject import predictorNames

# preprocessing of the data
if outlierDetection == 1:
    # outlier detection
    distances = gammaidx(X, 5)
    # delete outliers from data and label
    indices = np.argsort(distances)[:int(outlierRate*len(distances))]
    X = np.delete(X, indices, 0)
    Y = np.delete(Y, indices, 0)

# Principal component analysis (PCA)
pca = PCA()
pca.fit(X)
predictorImportance = pca.explained_variance_ratio_[0:10]
plt.bar(range(len(predictorImportance)), predictorImportance)

# decision tree classifier
clfTree = tree.DecisionTreeClassifier()
# SVM classifier
clfSVM = svm.SVC(kernel='linear', C=1)
# neural network classifier
clfNN = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)
# evaluation
scoresTree = cross_val_score(clfTree, X, Y, cv=10)
print("Accuracy Decision Tree: %0.2f (+/- %0.2f)" % (scoresTree.mean(), 
                             scoresTree.std() * 2))
scoresSVM = cross_val_score(clfSVM, X, Y, cv=10)
print("Accuracy Support Vector Machine: %0.2f (+/- %0.2f)" % (scoresSVM.mean(), 
                            scoresSVM.std() * 2))
scoresNN = cross_val_score(clfNN, X, Y, cv=10)
print("Accuracy Neural Network: %0.2f (+/- %0.2f)" % (scoresNN.mean(), 
                           scoresNN.std() * 2))

# print decision tree to PDF
# TODO check if class_names order is correct
clfTree = clfTree.fit(X, Y)
dot_data = tree.export_graphviz(clfTree, out_file=None, 
                        feature_names=predictorNames,  
                         class_names=np.unique(Y),  
                         filled=True, rounded=True,  
                         special_characters=True)  
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("clfTree.pdf")


