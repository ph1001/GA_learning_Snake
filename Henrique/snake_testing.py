from call_snake_hv import Individual, Population
from snake_hv import controlled_run, dis_width, dis_height, snake_block, automatic_mode, detailed_console_outputs
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
from copy import deepcopy
from utils_hv import phen_variance, gen_variance, phen_entropy, gen_entropy, fs

snake = Population(
    size=20
)

snake.evolve(
    gens=100, 
    select= tournament,
    crossover= arithmetic_co,
    mutate=geometric_mutation,
    co_p=0.5,
    mu_p=0.5,
    elitism=True,
    fitness_sharing = False,
    record_diversity = False,
    constant_ms = 0.3
)