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
 


## WITH THIS CONFIG APPROX 17h

RUN_NUM = 15 #number of runs to do for each config 
for run in range(RUN_NUM):
    
    snakes = Population(size = 2, 
                    moves_till_stuck = 100,
                    fitness_function = lambda x,y: (x,y),
                    optim = 'max'
                    )
    
    snakes.evolve(  gens = 2, #Number of generations to be produced
                select = tournament, #Selection function
                crossover = arithmetic_co, #Crossover function
                mutate = geometric_mutation, #Mutation function
                co_p = 0.5, #crossover probability
                mu_p = 0.2, #mutation probability
                multi_objective = True, #wheter to perform multiobjective optimization (fitness has to be a tuple)
                tournament_size = 2, #size of the sample for the tournament selction
                constant_ms = 2000, #Geometric Mutation coefficient 
                elitism = True, #wheter to perform elitisim 
                record_diversity = False, #wheter to record diversity
                fitness_sharing = True) #wheter to perform fitness sharing

    snakes.log_bestfit(config_name = 'fit_funct_henrique_recorddiv_on_fit', run_number = run+15)
    snakes.log_diversity(config_name = 'fit_funct_henrique_recorddiv_on_div', run_number = run+15)