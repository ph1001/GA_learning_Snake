# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 16:36:47 2021

@author: utente
"""

#
#
#
# Run everything by running this script.
# For me it works best to click "Run" -> "Run Without Debugging" for that.
# Also the game window always opend behind the editor for some reason.
#
# Please not that right now 'moves_till_stuck' is set to 100, which is quite low.
# This can be changed in snake.py.
#
#
#

# This script is heavily inspired by this blogpost: https://thingsidobysanil.wordpress.com/2018/11/12/87/

# Import libraries and components from snake
from snake import controlled_run, dis_width, dis_height, snake_block, automatic_mode
from snake_nodisplay import controlled_run_nodisplay, dis_width_nodisplay, dis_height_nodisplay, snake_block_nodisplay
import numpy as np
from keras import layers, models
from random import random, randint
from tqdm import tqdm
from operator import  attrgetter
import math
from utils import phen_variance, gen_variance, phen_entropy, gen_entropy, fs, mo_selection
import os
import csv


# Class Individual. Instances of this class play snake and make up a population.
class Individual():

    # init function of class Individual
    def __init__(self,
                ind_number = randint(1,9),
                evolution_step = 1,
                verbose = False,
                input_dim = 53,
                sight_dist = 3,
                games_to_play = 1,
                fitness_function = lambda x,y: x*math.exp(y) ,
                weights = None,
                moves_till_stuck = 50,
                show = False, #wheter to show the snake game window
                hidden_layers = 1):
        
        self.input_dim = input_dim
        self.sight_dist = sight_dist
        self.games_to_play = games_to_play
        self.verbose = verbose
        self.fitness_function = fitness_function
        self.moves_till_stuck = moves_till_stuck
        self.show = show
        self.hidden_layers = hidden_layers

        # Give this individual a number
        self.ind_number = ind_number

        # Initialise this individual's evolution step with 1
        self.evolution_step = evolution_step

        # Print game's width, height and snake's width
        if self.verbose:
            print(dis_width, dis_height, snake_block)

        # Create a neural network that will learn to play snake
        self.model = models.Sequential()
        self.model.add(layers.Dense(16, activation = 'sigmoid', input_dim = 6))
        # for _ in range(self.hidden_layers):
        #     self.model.add(layers.Dense(64, activation = 'sigmoid', input_dim = input_dim))
        self.model.add(layers.Dense(3, activation = 'softmax'))
        
        if weights != None:
            self.model.set_weights(weights)

        self.weights = self.model.get_weights()
        # Play a game
        self.play()
        
    def __getitem__(self, position):
        return self.weights[position]

    def __setitem__(self, position, value):
         self.weights[position] = value
    
    def __len__(self):
        return len(self.weights)
    
    def __repr__(self):
        return f'Neural Network with {self.input_dim} input nodes, {self.model.layers[0].weights[1].shape[0]} hidden layer neurons and {self.model.layers[1].weights[1].shape[0]} output layer neurons'
         
    # Define a function that lets an individual play snake
    def play(self, show = False):

        # Start the game by calling the function controlled_run from snake.py and receive the fitness resulting 
        # from the games_to_play games played by this individual in this evolution step
        # MOVED games_to_play here, defined together with the individual
        
        #the controlled_run function return the score and the age of the Individual
        if self.show or show:
            score, age = controlled_run(self, self.ind_number, self.evolution_step, self.games_to_play, self.verbose, self.moves_till_stuck)
        else:
            score, age = controlled_run_nodisplay(self, self.ind_number, self.evolution_step, self.games_to_play, self.verbose, self.moves_till_stuck)
        
        self.score = score
        self.age = age
        
        if self.verbose:
            print('Evolution step ' + str(self.evolution_step) + ':, Individual ' + str(self.ind_number) + ' is done playing.')

        # INDIVIDUAL FITNESS FUNCTION
        self.fitness = self.fitness_function(age, score)
            
        
    # Define a function that communicates with snake.py. It is called from snake.py from inside the function gameLoop
    def control(self, game_state):

        # Some printing for debugging purposes
        if self.verbose:
            print("control() was called.")

        # In the very first iteration, simply pass "up"
        if game_state['snake_List'] == []:

            # Some printing for debugging purposes
            if self.verbose:
                print('"Up" was passed automatically.')
            return 'w'
        # Process the information received about the current state of the game
        snake_List = game_state['snake_List']
        snake_Head = game_state['snake_Head']
        direction = game_state['direction']
        food = (game_state['foodx'], game_state['foody'])
        #check if going straight is clear(1) or there is an obstacle(0)
        possible_position = (snake_Head[0] + direction[0], snake_Head[1] + direction[1])
        if possible_position[0] >= 400 or possible_position[1] >= 400 or possible_position[0] < 0 or possible_position[1] < 0 or possible_position in snake_List:
            clear_straight = 0
        else:
            clear_straight = 1
        #checking if it's clear right or left
        #first identify what's left/right
        if direction[1] == -10: #recognize if it's moving up vertically
        
            right = (snake_Head[0] + 10, snake_Head[1])
            left = (snake_Head[0] - 10, snake_Head[1])
            
            if snake_Head[0] == food[0] and snake_Head[1] >= food[1]: #check if the food is ahead
                food_ahead = 1
                food_right = 0
                food_left = 0
            elif snake_Head[0] < food[0]: #food on the right
                food_ahead = 0
                food_right = 1
                food_left = 0
            else: #food on the left
                food_ahead = 0
                food_right = 0
                food_left = 1
                
        elif direction[1] == 10: #recognize if it's moving down vertically
        
            right = (snake_Head[0] - 10, snake_Head[1])
            left = (snake_Head[0] + 10, snake_Head[1])

            if snake_Head[0] == food[0] and snake_Head[1] - food[1] <= 0: #check if the food is ahead
                food_ahead = 1
                food_right = 0
                food_left = 0
            elif snake_Head[0] < food[0]: #food on the right
                food_ahead = 0
                food_right = 0
                food_left = 1
            else: #food on the left
                food_ahead = 0
                food_right = 1
                food_left = 0
            
        elif  direction[0] == -10: #recognize if it's moving left horizontally
        
            right = (snake_Head[0], snake_Head[1] - 10)
            left = (snake_Head[0], snake_Head[1] + 10)
            
            if snake_Head[1] == food[1] and snake_Head[0] - food[0] <= 0: #check if the food is ahead
                food_ahead = 1
                food_right = 0
                food_left = 0
            elif snake_Head[1] < food[1]: #food on the right
                food_ahead = 0
                food_right = 0
                food_left = 1
            else: #food on the left
                food_ahead = 0
                food_right = 1
                food_left = 0
            
        else: #recognize if it's moving right horizontally
        
            right = (snake_Head[0], snake_Head[1] + 10)
            left = (snake_Head[0], snake_Head[1] - 10
                    )
            
            if snake_Head[1] == food[1] and snake_Head[0] - food[0] >= 0: #check if the food is ahead
                food_ahead = 1
                food_right = 0
                food_left = 0
            elif snake_Head[1] < food[1]: #food on the right
                food_ahead = 0
                food_right = 1
                food_left = 0
            else: #food on the left
                food_ahead = 0
                food_right = 0
                food_left = 1
            
        #then check if it's occupied
        if right[0] >= 400 or right[1] >= 400 or right[0] < 0 or right[1] < 0 or right in snake_List:
            
            clear_right = 0
        else:
            clear_right = 1
            
        if left[0] >= 400 or left[1] >= 400 or left[0] < 0 or left[1] < 0 or left in snake_List:
            
            clear_left = 0
        else:
            clear_left = 1
        
        input_nn = np.array([
                    clear_straight, clear_right, clear_left,
                    food_ahead, food_right, food_left
                    ])
        
        input_nn.shape = (1,6)
        
        game_action = np.argmax(self.model.predict(input_nn))
        
        if self.verbose:
            print(f'Input : {input_nn}')
            print(f'Output : {game_action}')
        
        return game_action

class Population:
    
    def __init__(self, 
                 size,
                 verbose = False,
                 evolution_step = 0,
                 moves_till_stuck = 50,
                 show = False,
                 fitness_function = lambda x,y: x*math.exp(y) ,
                 hidden_layers = 1):
        self.individuals = []
        self.size = size
        self.verbose = verbose
        self.evolution_step = evolution_step
        self.moves_till_stuck = moves_till_stuck
        self.show = show
        self.fitness_function = fitness_function
        self.hidden_layers = hidden_layers
        
        
        # Create individuals and add them to the population. Creating an individual will execute the __init__ function 
        # of class Individual, which then will result in this individual playing snake.
        for i in tqdm(range(size)):
            individual = Individual(ind_number = i+1,
                                    evolution_step  = self.evolution_step,
                                    verbose = self.verbose,
                                    moves_till_stuck = self.moves_till_stuck,
                                    show = self.show,
                                    fitness_function = self.fitness_function,
                                    hidden_layers = self.hidden_layers)
            
            self.individuals.append(individual)
            
    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)})"
    
    def log_bestfit(self, config_name, run_number):
        
        dir_path = os.path.join('data', config_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            
        with open(os.path.join('data', config_name, f'{config_name}_{run_number}.csv'), mode = 'a', newline='') as file:
            
            writer = csv.writer(file)
            
            for gen, best_fit in enumerate(self.evolution_process):
                writer.writerow([gen, best_fit])

    def log_diversity(self, config_name, run_number):
        
            dir_path = os.path.join('data', config_name)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
                
            with open(os.path.join('data', config_name, f'{config_name}_{run_number}.csv'), mode = 'a', newline='') as file:
                
                writer = csv.writer(file)
                
                for gen in range(self.evolution_step):
                    writer.writerow([gen,
                                     self.phen_variance_dict[str(self.evolution_step)],
                                     self.gen_variance_dict[str(self.evolution_step)],
                                     self.phen_entropy_dict[str(self.evolution_step)],
                                     self.gen_entropy_dict[str(self.evolution_step)],])
    
    # Define a funcion that receives a population and evolves it using a GA. It also receives evolution_step to keep track of where we are at in the process.
    def evolve( self,
                gens, #Number of generations to be produced
                select, #Selection function
                crossover, #Crossover function
                mutate, #Mutation function
                co_p, #crossover probability
                mu_p, #mutation probability
                multi_objective = False, #wheter to perform multiobjective optimization (fitness has to be a tuple)
                tournament_size = None, #size of the sample for the tournament selction
                constant_ms = None, #Geometric Mutation coefficient 
                elitism = False, #wheter to perform elitisim, cannot be used with multiobjective optimization 
                record_diversity = False, #wheter to record diversity
                fitness_sharing = False): #wheter to perform fitness sharing
        
        self.evolution_process = []
        
        if record_diversity:
            self.phen_variance_dict = {}
            self.gen_variance_dict = {}
            self.phen_entropy_dict = {}
            self.gen_entropy_dict = {}
            
        for gen in tqdm(range(gens), desc = 'Evolving Population'): #argument of evolve attribute
                
    
                
                #recording the variance of the Population
                if record_diversity: #argument of evolve attribute
                    
                    self.phen_variance_dict[str(self.evolution_step)] = phen_variance(self)
                    self.gen_variance_dict[str(self.evolution_step)] = gen_variance(self) 
                    self.phen_entropy_dict[str(self.evolution_step)] = phen_entropy(self)
                    self.gen_entropy_dict[str(self.evolution_step)] = gen_entropy(self)
                
                #FITNESS SHARING
                if fitness_sharing: #argument of evolve attribute
                    fs(self)
                
                #Elitism
                if elitism: #argument of evolve attribute
                    #saving a deepcopy of the best individual of the population
                    elite = max(self.individuals, key = attrgetter('fitness')).weights
                    
                new_pop = []
                while len(new_pop) < self.size:
                    #selection
                    if multi_objective:
                        parent1, parent2 = mo_selection(self)
                    else:
                        if tournament_size != None:
                            parent1, parent2 = select(self, tournament_size), select(self, tournament_size)
                        else:
                            parent1, parent2 = select(self), select(self) #argument of evolve attribute
                    # Crossover
                    if random() < co_p: #argument of evolve attribute
                        offspring1, offspring2 = crossover(parent1, parent2) #argument of evolve attribute
                    else:
                        offspring1, offspring2 = parent1.weights.copy(), parent2.weights.copy()
                        
                    # Mutation
                    if random() < mu_p: #argument of evolve attribute
                        if constant_ms != None:
                            #GEOMETRIC MUTATION
                            offspring1 = mutate(offspring1, constant_ms, self.evolution_step) #argument of evolve attribute
                        else:
                            offspring1 = mutate(offspring1)
                    if random() < mu_p: #argument of evolve attribute
                        if constant_ms != None:
                            #GEOMETRIC MUTATION
                            offspring2 = mutate(offspring2, constant_ms, self.evolution_step) #argument of evolve attribute
                        else:
                            offspring2 = mutate(offspring2)
    
                    new_pop.append(Individual(ind_number = len(new_pop),
                                              weights = offspring1,
                                              moves_till_stuck = self.moves_till_stuck,
                                              evolution_step = gen + 1,
                                              fitness_function = self.fitness_function,
                                              hidden_layers = self.hidden_layers))
                   
                    if len(new_pop) < self.size:
                        new_pop.append(Individual(ind_number = len(new_pop),
                                                  weights = offspring1,
                                                  moves_till_stuck = self.moves_till_stuck,
                                                  evolution_step = gen + 1,
                                                  fitness_function = self.fitness_function,
                                                  hidden_layers = self.hidden_layers))
                
                if elitism: #argument of evolve attribute
                    #finding worst Individual of the new population
                    least_fit = min(new_pop, key = attrgetter('fitness'))
                    #substituting the worst individual of the new population with the best one from the previous one
                    new_pop[new_pop.index(least_fit)] = Individual(ind_number = new_pop.index(least_fit),
                                                                   weights = elite,
                                                                   moves_till_stuck = self.moves_till_stuck,
                                                                   evolution_step = gen + 1,
                                                                   fitness_function = self.fitness_function,
                                                                   hidden_layers = self.hidden_layers)
                    
                
                self.individuals = new_pop
                
                
                
                #updating the evolution step                
                self.evolution_step += 1
                for indiv in self.individuals:
                    indiv.evolution_step = self.evolution_step
                    
                if multi_objective:
                    
                    #selecting the best solution
                    min_fit_x = min([i.fitness[0] for i in self.individuals])
                    min_fit_y = min([i.fitness[1] for i in self.individuals])
            
                    #calculating the distances to the best solution
                    distances = [ math.sqrt((i.fitness[0] - min_fit_x)**2) + math.sqrt((i.fitness[1] - min_fit_y)**2) for i in self.individuals]
                    #selecting the individual that is closer to the optimal solution
                    best_fit = self.individuals[distances.index(min(distances))].fitness
                    
                    
                else:
                    best_fit = max(self, key=attrgetter("fitness")).fitness
                
                self.evolution_process.append(best_fit)
                print(f'Best Individual: {best_fit}')
