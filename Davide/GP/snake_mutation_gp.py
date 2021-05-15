# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:19:09 2021

@author: utente
"""

import random
from utils_gp import create_randomfunct


def gp_mutation(individual, pop):
    
    ind = individual.split('(')
    
    try:
        mut_point = random.choice(list(range(1, len(ind))))
   
    except:
        mut_point = len(ind) - 1
        
    _, random_funct = create_randomfunct(len_functions = pop.len_functions,
                                         terminals = pop.terminals,
                                         operators = pop.operators,
                                         max_depth = len(ind) - 1, 
                                         impose_depth = True)
    
    
    random_funct = random_funct.split('(')
    
    ind = ind[:mut_point] + random_funct[mut_point:]
    
    par = ')' * (len(ind) - len(random_funct))
        
    return '('.join(ind) 

    
    