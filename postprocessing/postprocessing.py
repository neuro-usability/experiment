# coding: utf-8
import json
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt


# main 
with open('../data/tobias.json') as data_file:    
    data = json.load(data_file)

emoList = []
array =[]
for values in data['joy'][0]:
    tmp = flatten_json(values)
    for key, value in tmp.items():
        array.append(value)
    if emoList == []:
        emoList = array
    else:
        emoList = np.vstack((emoList, array))
    array = []
    
print(emoList[:,1])
print(emoList.shape)

for i in range(0,37):
        plt.plot(emoList[:,i])
plt.show()


# flatten function
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