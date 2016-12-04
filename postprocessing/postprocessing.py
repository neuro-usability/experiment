
# coding: utf-8

# In[194]:

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


# In[271]:

import os
import json
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

path = '../data'
dataMatrix = []
dataColumn = []
labels = []

# for all persons
for filename in os.listdir(path):
    with open('../data/'+filename) as data_file:    
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

for i in range(0,37):
        plt.plot(dataMatrix[:,i])
plt.show()
print(dataMatrix.shape)
print(np.asarray(labels).shape)

#print(json.dumps(dataObject, indent=3, sort_keys=True))
#dataMatrix

