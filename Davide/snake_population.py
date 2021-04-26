# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 11:43:02 2021

@author: utente
"""
from snake_game_neuralnetwork import gameLoop
from keras import layers, models
from random import random
import math

class Individual:
    
    def __init__(
        self,
        input_dim = 53,
        weights = None,
        
    ):
        model = models.Sequential()
        model.add(layers.Dense(64, activation = 'relu', input_dim = input_dim))
        model.add(layers.Dense(4, activation = 'softmax'))
        
        if weights != None:
            model.set_weights(weights)
            
        self.model = model
        self.fitness = self.evaluate()
        self.input_dim = input_dim
        
        
    def evaluate(self):
        score, age = gameLoop(self.model, speed = 10000, verbose = False)
        self.evaluate = age*math.exp(score)

    def __getitem__(self, position):
        raise Exception('Need to implement')

    def __setitem__(self, position, value):
        raise Exception('Need to implement')

    def __repr__(self):
        return f'Neural Network with {self.input_dim} input nodes, {self.representation.layers[0].weights[1].shape[0]} hidden layer neurons and {self.representation.layers[1].weights[1].shape[0]} output layer neurons'


class Population:
    
    def __init__(self, size, **kwargs):
        self.individuals = []
        self.size = size
        for _ in range(size):
            self.individuals.append(
                Individual(
                    input_dim = 53,
                    representation=None,  
                )
            )
    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism):
        for gen in range(gens):
            new_pop = []
            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                # Crossover
                if random() < co_p:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2
                # Mutation
                if random() < mu_p:
                    offspring1 = mutate(offspring1)
                if random() < mu_p:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))
            if elitism == True:
                raise NotImplementedError

            self.individuals = new_pop
            print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}"
