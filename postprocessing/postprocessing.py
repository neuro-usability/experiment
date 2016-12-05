# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
    
import os
import json
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn import svm
import pydotplus
from IPython.display import Image  
from sklearn.neural_network import MLPClassifier

path = '/home/jan/Affectiva API/data/'

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
    
# get data with function above
(X, Y) = get_training_data(path)
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
clfTree = clfTree.fit(X, Y)
dot_data = tree.export_graphviz(clfTree, out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("clfTree.pdf")
