# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:40:35 2021

@author: utente
"""
#Functions that calculate the variance and the entropy, both phenotypic and genotypic

from random import sample
from scipy.spatial.distance import euclidean
import math
import numpy as np

def phen_variance(pop):
            #Calculating the avg fitness of the population
            avg_fitness = sum([i.fitness for i in pop.individuals])/pop.size
            #calculating the variance over the population
            return sum([(i.fitness-avg_fitness)**2 for i in pop.individuals]) / (pop.size- 1)


def gen_variance(pop):
            #selecting a random individual to be the origin
            origin = sample(pop.individuals, 1)[0]
            #calculating the distances of each point to the distance
            distances = [ sum([ euclidean(ind[i], origin[i]) for i in range(len(ind)) ]) / len(ind) for ind in pop.individuals]
            #calculating the average distance over the population
            avg_distance = sum(distances) / pop.size
            #calculating the variance over the population
            return sum([(distance-avg_distance)**2 for distance in distances]) / (pop.size- 1)

def phen_entropy(pop):
            #Calculating the fitnesses of the population
            fitnesses = [i.fitness for i in pop.individuals]
            #calculating the entropy over the population
            return sum([ fitnesses.count(fitness) / len(fitnesses) * math.log(fitnesses.count(fitness) / len(fitnesses),  2) for fitness in fitnesses])

def gen_entropy(pop):
            #selecting a random individual to be the origin
            origin = sample(pop.individuals, 1)[0]
            #calculating the distances of each point to the distance
            distances = [ sum([ euclidean(ind[i], origin[i]) for i in range(len(ind)) ]) / len(ind) for ind in pop.individuals]
            #calculating the variance over the population
            return sum([ distances.count(distance) / len(distances) * math.log(distances.count(distance) / len(distances), 2) for distance in distances])

def fs(pop):
            #building the distance-half matrix
            #starting by initializing the matrix with zeros
            distance_matrix = np.zeros((len(pop), len(pop)))
            #iterating over the individuals and calculating the euclidean distances
            for i in range(pop.size):
                for j in range(i, pop.size):
                    distance_matrix[i,j] = sum([ euclidean(pop.individuals[i][index].flatten(), pop.individuals[j][index].flatten()) for index in range(4) ]) / 4
            #normalizing distances in [0,1] and reverting them, so the result is big if the distance was small and viceversa
            max_ = distance_matrix.max()
            min_ = distance_matrix.min()
            distance_matrix = 1 - (distance_matrix - min_)/(max_ - min_)
            #defining a sharing coeffient for each element in the population
            sharing_coeff = []
            for i in range(pop.size):
                sharing_coeff.append( sum(distance_matrix[i] + distance_matrix.T[i]) )
            #updating the individuals fitness
            for i, individual in enumerate(pop.individuals):
                individual.fitness = individual.fitness / sharing_coeff[i]
                
                    
            
    
    
    
            




