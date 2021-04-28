# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:40:35 2021

@author: utente
"""
#Functions that calculate the variance and the entropy, both phenotypic and genotypic

from random import sample
from numpy.linalg import norm
import math

def phen_variance(pop):
            #Calculating the avg fitness of the population
            avg_fitness = sum([i.fitness for i in pop.individuals])/pop.size
            #calculating the variance over the population
            return sum([(i.fitness-avg_fitness)**2 for i in pop.individuals]) / (pop.size- 1)


def gen_variance(pop):
            #selecting a random individual to be the origin
            origin = sample(pop.individuals, 1)[0]
            #calculating the distances of each point to the distance
            distances = [ sum([ norm((ind[i], origin[i])) for i in range(len(ind)) ]) / len(ind) for ind in pop.individuals]
            #calculating the average distance over the population
            avg_distance = sum(distances) / pop.size
            #calculating the variance over the population
            return sum([(distance-avg_distance)**2 for distance in distances]) / (pop.size- 1)

def phen_entropy(pop):
            #Calculating the fitnesses of the population
            fitnesses = [i.fitness for i in pop.individuals]
            #calculating the entropy over the population
            return sum([ fitnesses.count(fitness) / len(fitnesses) * math.log(fitnesses.count(fitness) / len(fitnesses)) for fitness in set(fitnesses)])

def gen_entropy(pop):
            #selecting a random individual to be the origin
            origin = sample(pop.individuals, 1)[0]
            #calculating the distances of each point to the distance
            distances = [ sum([ norm((ind[i], origin[i])) for i in range(len(ind)) ]) / len(ind) for ind in pop.individuals]
            #calculating the variance over the population
            return sum([ distances.count(distance) / len(distances) * math.log(distances.count(distance) / len(distances)) for distance in set(distances)])

        




