# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:40:35 2021

@author: utente
"""
#Functions that calculate the variance and the entropy, both phenotypic and genotypic

from random import sample, uniform
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
            distances = [ sum([ np.linalg.norm(ind[i] -  origin[i]) for i in range(len(ind)) ]) / len(ind) for ind in pop.individuals]
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
            distances = [ sum([ np.linalg.norm(ind[i] - origin[i]) for i in range(len(ind)) ]) / len(ind) for ind in pop.individuals]
            #calculating the variance over the population
            return sum([ distances.count(distance) / len(distances) * math.log(distances.count(distance) / len(distances), 2) for distance in distances])

def fs(pop):
            #building the distance-half matrix
            #starting by initializing the matrix with zeros
            distance_matrix = np.zeros((len(pop), len(pop)))
            #iterating over the individuals and calculating the euclidean distances
            for i in range(pop.size):
                for j in range(i, pop.size):
                    distance_matrix[i,j] = sum([ np.linalg.norm(pop.individuals[i][index] - pop.individuals[j][index]) for index in range(4) ]) / 4
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
                
                if pop.optim == 'max':
                    
                    individual.fitness = individual.fitness / sharing_coeff[i]
                
                else: 
                    
                    individual.fitness = individual.fitness * int(sharing_coeff[i]) 
                    

                
def mo_selection(pop):
    '''
    Multiobjective optimization selection process, can be used only if the fitness function is a tuple.    

    '''
    #copying all individuals in a list s 
    s = [(pop.individuals.index(i), i.fitness) for i in pop.individuals]
    #Initializing the flag dictionary, the flag and the individuals
    flag = {}
    i = 1 
    fit = s[0]
    fit2 = s[1]    
    
    if pop.optim == 'max':
    
        #keep iterating while the set is not empty
        while len(s) > 0:
            #checking if the individual is dominated
            if fit[1][0] < fit2[1][0] and fit[1][1] < fit2[1][1]:
                #checking if we already compare all individuals
                if s.index(fit) == len(s) - 1:
                    #reinitializing the loop and increasing the flag
                    fit = s[0]
                    fit2 = s[1]
                    i += 1
                #if it is checking for another individual
                fit = s[s.index(fit) + 1 ]
            
            #otherwise
            else:
                #checking if  we already check for all individuals
                if fit2 == s[-1]:
                    #then the individual is not-dominated, saving it in the flag dict with the right flag
                    flag[str(fit[0])] = i
                    #removing it from the list 
                    s.remove(fit)
                    #checking how many individual are left
                    if len(s) == 1:
                        flag[str(s[0][0])] = i + 1
                        break
                    elif len(s) == 0:
                        break
                    else:
                        #reinitializing the individuals
                        fit = s[0]
                        fit2 = s[1]
                #otherwise
                else:
                    #changing the individual to check for 
                    fit2 = s[s.index(fit2) + 1]
                    
    else:
        
        #keep iterating while the set is not empty
        while len(s) > 0:
            #checking if the individual is dominated
            if fit[1][0] > fit2[1][0] and fit[1][1] > fit2[1][1]:
                #checking if we already compare all individuals
                if s.index(fit) == len(s) - 1:
                    #reinitializing the loop and increasing the flag
                    fit = s[0]
                    fit2 = s[1]
                    i += 1
                #if it is checking for another individual
                fit = s[s.index(fit) + 1 ]
            
            #otherwise
            else:
                #checking if  we already check for all individuals
                if fit2 == s[-1]:
                    #then the individual is not-dominated, saving it in the flag dict with the right flag
                    flag[str(fit[0])] = i
                    #removing it from the list 
                    s.remove(fit)
                    #checking how many individual are left
                    if len(s) == 1:
                        flag[str(s[0][0])] = i + 1
                        break
                    elif len(s) == 0:
                        break
                    else:
                        #reinitializing the individuals
                        fit = s[0]
                        fit2 = s[1]
                #otherwise
                else:
                    #changing the individual to check for 
                    fit2 = s[s.index(fit2) + 1]
        
    #assinging to each ind the probability of being picked of 1 - ind.flag / sum(flag)
    tot_flag = sum(flag.values())
    prob = {}
    for ind in list(flag.keys()):
        prob[ind] = 1 - flag[ind]/tot_flag
    
    #sorting the probabilities dictionary
    sorted_prob = {}
    sorted_keys = sorted(prob, key=prob.get) 
    for w in sorted_keys:
        sorted_prob[w] = prob[w]
    #selecting the two parents
    spin = uniform(0, sum(sorted_prob.values()))
    position = 0
    for individual in sorted_prob.keys():
        position += sorted_prob[individual]
        if position > spin:
            index1 = individual
            break
        
    spin = uniform(0, sum(sorted_prob.values()))
    position = 0
    # Find individual in the position of the spin
    for individual in sorted_prob.keys():
        position += sorted_prob[individual]
        if position > spin:
            index2 = individual
            break
    
    return pop.individuals[int(index1)], pop.individuals[int(index2)]

                    
            
    
    
    
            




