# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 19:57:33 2021

@author: utente
"""

from snake_game_neuralnetwork import gameLoop
import keras
from keras import layers, models
import numpy as np
import pygame
import time
import random

model = models.Sequential()
model.add(layers.Dense(16, activation = 'relu', input_dim = 8))
model.add(layers.Dense(4, activation = 'softmax'))

gameLoop(model, speed = 15)