# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:19:09 2021

@author: utente
"""

from random import randint, sample, uniform
from numpy.random import randn


def geometric_mutation(individual, constant_ms):
    """Geometric mutation for snake Individual

    Args:
        individual (Individual): A GA individual from call_snake libray.py

    Returns:
        Indivdual: mutated Individual
    """
    #decrement of the constant_ms
    constant_ms = constant_ms / (individual.evolution_step + 1)
    #making a copy of the parent
    weights = individual.weights.copy()
    #We iterate over the weights (matrix, array, matrix, array) 
    for i, matrix in enumerate(weights):
        
        if i == 0 or i == 2: #check if we are handling a matrix
            for i in range(matrix.shape[0]): #we iterate over the matrix
                for j in range(matrix.shape[1]):
                    shift = uniform(-constant_ms, constant_ms) #we select the shift in the interval
                    matrix[i,j] += shift
            
        else: #otherwise we are handling an array
            for i in range(len(matrix)): #iterate over array
                shift = uniform(-constant_ms, constant_ms)
                matrix[i] += shift 
    
    return weights
    
    

def normal_distribution_mutation(individual):
    """ Mutation for snake Individual calculating the shift with a standard normal distribution

    Args:
        individual (Individual): A GA individual from call_snake libray.py

    Returns:
        Indivdual: mutated Individual
    """
    #making a copy of the parent
    weights = individual.weights.copy()
    #We iterate over the weights (matrix, array, matrix, array) 
    for i,matrix in enumerate(weights):
        
        if i == 0 or i == 2: #check if we are handling a matrix
            for i in range(matrix.shape[0]): #we iterate over the matrix
                for j in range(matrix.shape[1]):
                    shift = randn() #we draw the shift from a standard normal distribution
                    matrix[i,j] += shift
            
        else: #otherwise we are handling an array
            for i in range(len(matrix)): #iterate over array
                shift = randn()
                matrix[i] += shift
    
    return weights
    
    