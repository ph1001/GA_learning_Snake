# -*- codingng: utf-8 -*-
"""
Created on Fri Apr 30 10:39:58 2021

@author: utente
"""

from call_snake_gp import Population
from snake_crossover_gp import *
from snake_mutation_gp import *
from snake_selection import fps, tournament, ranking
import math
 


## WITH THIS CONFIG APPROX 17h

RUN_NUM = 3 #number of runs to do for each config 
for run in range(RUN_NUM):
    
    snakes = Population(size = 25, 
                    moves_till_stuck = 100,
                    fitness_function = lambda x,y: x*y,
                    impose_depth = False,
                    max_depth = 100
                    )
    
    snakes.evolve(  gens = 100, #Number of generations to be produced
                    select = tournament, #Selection function
                    crossover = gp_co, #Crossover function
                    mutate = gp_mutation, #Mutation function
                    co_p = 0.5, #crossover probability
                    mu_p = 0.2, #mutation probability
                    multi_objective = False, #wheter to perform multiobjective optimization (fitness has to be a tuple)
                    tournament_size = 5, #size of the sample for the tournament selection
                    elitism = True, #wheter to perform elitisim 
                    record_diversity = False, #wheter to record diversity
                    fitness_sharing = False) #wheter to perform fitness sharing

    snakes.log_bestfit(config_name = 'gp_davide', run_number = run)
    # snakes.log_diversity(config_name = , run_number = run)