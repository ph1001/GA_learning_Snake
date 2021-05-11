# -*- codingng: utf-8 -*-
"""
Created on Fri Apr 30 10:39:58 2021

@author: utente
"""

from call_snake import Population
from snake_crossover import arithmetic_co
from snake_mutation import geometric_mutation, normal_distribution_mutation
from snake_selection import fps, tournament, ranking
import math

snakes = Population(size = 25, 
                    moves_till_stuck = 50,
                    fitness_function = lambda x,y: math.exp(y), #using exp so odds of chosing best individual as a parent increase for rbs and fbs
                    hidden_layers = 3)

snakes.evolve(  gens = 500, #Number of generations to be produced
                select = tournament, #Selection function
                crossover = arithmetic_co, #Crossover function
                mutate = geometric_mutation, #Mutation function
                co_p = 0.5, #crossover probability
                mu_p = 0.2, #mutation probability
                constant_ms = 2000, #Geometric Mutation coefficient 
                tournament_size = 5,
                elitism = True, #wheter to perform elitisim
                record_diversity = True, #wheter to record diversity
                fitness_sharing = True)