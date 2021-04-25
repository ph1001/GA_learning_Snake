# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 19:57:33 2021

@author: utente
"""

from snake_game_neuralnetwork import gameLoop
from keras import layers, models
#import numpy as np

model = models.Sequential()
model.add(layers.Dense(64, activation = 'relu', input_dim = 57))
model.add(layers.Dense(4, activation = 'softmax'))

fitness, moves = gameLoop(model, speed = 60)