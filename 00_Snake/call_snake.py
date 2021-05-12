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
from utils import phen_variance, gen_variance, phen_entropy, gen_entropy, fs

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
        for _ in range(self.hidden_layers):
            self.model.add(layers.Dense(64, activation = 'sigmoid', input_dim = input_dim))
        self.model.add(layers.Dense(4, activation = 'softmax'))
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

        # Some printing for debugging purposes
        if self.verbose:
            print('snake_List:', game_state['snake_List'])
            print('snake_Head:', game_state['snake_Head'])
            print('food position:', game_state['foodx'], game_state['foody'])
           
        # Define a sight distance (number of squares counted from the edges of the snake's head; field of vision is a square as well)
        sight_dist = self.sight_dist
        # Compute the square's edge length
        edge_length = 1+2*sight_dist

        # Compute the "field of vision" of the snake; it is made up of a square array with the length of 1+2*sight_dist
        # Side note: Possible positions in the game grid (without hitting the wall): Min: (0,0), Max: (790,590) - This is specified in snake.py
        
        # Initialise a field of vision with all elemente being 0.5 (0.5 means neutral)
        fov = np.zeros((edge_length, edge_length)) + 0.5
        
        # Give the snake's head, snake_List, foodx, and foody shorter names
        s_head = game_state['snake_Head']
        s_list = game_state['snake_List']
        fx, fy = game_state['foodx'], game_state['foody']
        

        # Iterate over all elements of our field of vision array
        for i in range(edge_length):
            for j in range(edge_length):
                
                # Decrease our indices in such a way that they represent the relative position
                rel_pos_x = j - sight_dist
                rel_pos_y = i - sight_dist
                # Get the values of the currently looked at field of vision element in our grid space
                x = s_head[0] + rel_pos_x * snake_block
                y = s_head[1] + rel_pos_y * snake_block

                # Check if the currently looked at field of vision element contains a part of our snake
                snake_body = [x, y] in s_list
                # If so, write 0 in the respective field of vision cell (0 means not good)
                if snake_body:
                    fov[i,j] = 0

                # Check if the currently looked at field of vision element is outside the allowed grid
                outside_grid = x >= dis_width or x < 0 or y >= dis_height or y < 0
                # If so, write 0 in the respective field of vision cell (0 means not good)
                if outside_grid:
                    fov[i,j] = 0

                # Check if the currently looked at field of vision element contains food
                food = (x == fx and y == fy)
                # If so, write 1 in the respective field of vision cell (1 means good)
                if food:
                    fov[i,j] = 1

        # Rename head position
        x1 = s_head[0]
        y1 = s_head[1]
        foodx = fx
        foody = fy

        #distances to food
        distance_food_y = foody - y1
        distance_food_x = foodx - x1

        # Create the NN's input and compute its output
        # Only in automatic mode though
        if automatic_mode:
            #SCALE INPUTS to [0,1]
            distance_food_y_scaled = (distance_food_y + (dis_height - snake_block))/(2*(dis_height - snake_block))
            distance_food_x_scaled = (distance_food_x + (dis_width - snake_block))/(2*(dis_width - snake_block))
            snake_head_x_scaled = x1 / (dis_width - snake_block)
            snake_head_y_scaled = y1 / (dis_height - snake_block)

            # Create the input with the distance to food and the snake's position first
<<<<<<< Updated upstream
            if False:
                input_nn = [distance_food_y_scaled, distance_food_x_scaled, #distances to food
                        snake_head_x_scaled, snake_head_y_scaled]#snake head
            
            input_nn = [distance_food_y, distance_food_x, #distances to food
                        x1, y1]
=======
<<<<<<< Updated upstream
            input_nn = [distance_food_y_scaled, distance_food_x_scaled, #distances to food
                        snake_head_x_scaled, snake_head_y_scaled]#snake head

=======
            
            input_nn = [distance_food_y_scaled, distance_food_x_scaled, #distances to food
                        snake_head_x_scaled, snake_head_y_scaled]#snake head
            
            # input_nn = [distance_food_y, distance_food_x, #distances to food
            #             x1, y1]
>>>>>>> Stashed changes
>>>>>>> Stashed changes
            # Transorm input intpo np.array
            input_nn = np.array(input_nn)
            # Fixing the shape so it can be used for the NN
            input_nn.shape = (1,4)
            # Concatenating the vision matrix to the input array                
            fov.shape = (1,49)
            input_nn = np.concatenate((input_nn, fov), axis = 1)

            # Producing output of the model, the output are probabilities
            # for each move, using np.argmax to get the index of the 
            # highest probability
            output = np.argmax(self.model.predict(input_nn))
 
        # Some printing for debugging purposes
        # print input and output
        if self.verbose:
            print(f'Input without vision matrix: {input_nn[:,:4]}')
            print('Vision matrix:')
            print(fov)
            print(f'Output : {output}')

        # If automatic_mode is False, the user is asked to provide an input (direction of the snake to go) via the keyboard with keys w, a, s, and d
        if not automatic_mode:

            # Define some valid inputs (this will not be relevant anymore once the Neural Network is implemented)
            valid_inputs = ['w','a','s','d']
            # Initialise a variable that scays if a valid input was received
            no_valid_input = True
            # Until a valid input was received, ask for one
            while no_valid_input:
                game_action = str(input())
                if game_action in valid_inputs:
                    no_valid_input = False

        # If automatic_mode is True, use the NNs output as the decision on where to go next
        if automatic_mode:
            game_action = output

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
    
    # Define a funcion that receives a population and evolves it using a GA. It also receives evolution_step to keep track of where we are at in the process.
    def evolve( self,
                gens, #Number of generations to be produced
                select, #Selection function
                crossover, #Crossover function
                mutate, #Mutation function
                co_p, #crossover probability
                mu_p, #mutation probability
                tournament_size = None, #size of the sample for the tournament selction
                constant_ms = None, #Geometric Mutation coefficient 
                elitism = False, #wheter to perform elitisim
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
                    
                
                best_fit = max(self, key=attrgetter("fitness")).fitness
                self.evolution_process.append(best_fit)
                print(f'Best Individual: {best_fit}')
            