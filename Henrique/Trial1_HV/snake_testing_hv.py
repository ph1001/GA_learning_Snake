from call_snake_hv import Individual, Population
from snake_hv import controlled_run, dis_width, dis_height, snake_block, automatic_mode
from snake_crossover_hv import arithmetic_co
from snake_mutation_hv import geometric_mutation, normal_distribution_mutation
from snake_selection_hv import fps, ranking, tournament
import numpy as np
from keras import layers, models
import random
from random import sample
from tqdm import tqdm
from operator import  attrgetter
import math
import copy
from copy import deepcopy as deepcopy
from utils_hv import phen_variance, gen_variance, phen_entropy, gen_entropy, fs

snake = Population(
    size=20,
    show = False
)

snake.evolve(
    gens=100, 
    select= tournament,
    tournament_size = 5,
    crossover= arithmetic_co,
    mutate=geometric_mutation,
    co_p=0.2,
    mu_p=0.2,
    elitism=True,
    fitness_sharing = True,
    record_diversity = False,
    constant_ms = 0.3
)