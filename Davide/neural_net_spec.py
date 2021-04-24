# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:35:39 2021

@author: utente
"""

import keras
from keras import layers, models
import numpy as np

model = models.Sequential()
model.add(layers.Dense(16, activation = 'relu', input_dim = 8))
model.add(layers.Dense(4, activation = 'softmax'))

#model.layers[0].set_weights([np.zeros((16,16)), np.zeros((16,))])

weights1 = model.layers[0].weights #1 matrix + 1 array for bias
weights2 = model.layers[1].weights