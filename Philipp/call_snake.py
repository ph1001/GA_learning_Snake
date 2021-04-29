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
from snake import controlled_run, dis_width, dis_height, snake_block, automatic_mode, detailed_console_outputs
from snake_crossover import arithmetic_co
import numpy as np
from keras import layers, models
import random
from random import sample
from tqdm import tqdm
from operator import  attrgetter
import math
from copy import deepcopy
from utils import phen_variance, gen_variance, phen_entropy, gen_entropy, fs

use_tqdm = False
   
# Class Individual. Instances of this class play snake and make up a population.
class Individual():

    # init function of class Individual
    def __init__(self,
                ind_number = random.randint(1,9),
                evolution_step = 1,
                verbose = False,
                input_dim = 53,
                sight_dist = 3,
                games_to_play = 1,
                fitness_function = lambda x,y: x*math.exp(y) ,
                weights = None):

        # Give this individual a number
        self.ind_number = ind_number

        # Initialise this individual's evolution step with 1
        self.evolution_step = evolution_step

        # Print game's width, height and snake's width
        if detailed_console_outputs:
            print(dis_width, dis_height, snake_block)

        # Create a neural network that will learn to play snake
        self.model = models.Sequential()
        self.model.add(layers.Dense(64, activation = 'relu', input_dim = input_dim))
        self.model.add(layers.Dense(4, activation = 'softmax'))
        if weights != None:
            model.set_weights(weights)

        self.weights = self.model.get_weights()
        self.input_dim = input_dim
        self.sight_dist = sight_dist
        self.games_to_play = games_to_play
        self.verbose = verbose
        self.fitness_function = fitness_function
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
    def play(self):

        # Start the game by calling the function controlled_run from snake.py and receive the fitness resulting 
        # from the games_to_play games played by this individual in this evolution step
        # MOVED games_to_play here, defined together with the individual
        
        #the controlled_run function return the score and the age of the Individual
        score, age = controlled_run(self, self.ind_number, self.evolution_step, self.games_to_play, self.verbose)
        
        self.score = score
        self.age = age
        
        if self.verbose:
            print('Evolution step ' + str(self.evolution_step) + ':, Individual ' + str(self.ind_number) + ' is done playing.')

        # INDIVIDUAL FITNESS FUNCTION
        self.fitness = self.fitness_function(age, score)
            
        
    # Define a function that communicates with snake.py. It is called from snake.py from inside the function gameLoop
    def control(self, game_state):

        # Some printing for debugging purposes
        if detailed_console_outputs:
            print("control() was called.")

        # In the very first iteration, simply pass "up"
        if game_state['snake_List'] == []:

            # Some printing for debugging purposes
            if detailed_console_outputs:
                print('"Up" was passed automatically.')
            return 'w'

        # Process the information received about the current state of the game

        # Some printing for debugging purposes
        if detailed_console_outputs:
            print('snake_List:', game_state['snake_List'])
            print('snake_Head:', game_state['snake_Head'])
            print('food position:', game_state['foodx'], game_state['foody'])
           
        # Define a sight distance (number of squares counted from the edges of the snake's head; field of vision is a square as well)
        sight_dist = self.sight_dist
        # Compute the square's edge length
        edge_length = 1+2*sight_dist

        # Compute the "field of vision" of the snake; it is made up of a square array with the length of 1+2*sight_dist
        # Side note: Possible positions in the game grid (without hitting the wall): Min: (0,0), Max: (790,590) - This is specified in snake.py
        
        # Initialise a field of vision with all zeros
        fov = np.zeros((edge_length, edge_length))
        
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
                # If so, write -1 in the respective field of vision cell
                if snake_body:
                    fov[i,j] = -1

                # Check if the currently looked at field of vision element is outside the allowed grid
                outside_grid = x >= dis_width or x < 0 or y >= dis_height or y < 0
                # If so, write -1 in the respective field of vision cell
                if outside_grid:
                    fov[i,j] = -1

                # Check if the currently looked at field of vision element contains food
                food = (x == fx and y == fy)
                # If so, write 1 in the respective field of vision cell
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
            input_nn = [distance_food_y_scaled, distance_food_x_scaled, #distances to food
                        snake_head_x_scaled, snake_head_y_scaled]#snake head

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
        if detailed_console_outputs:
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
                 evolution_step = 1,
                 **kwargs):
        self.individuals = []
        self.size = size
        self.verbose = verbose
        self.evolution_step = evolution_step
        
        
        # Create individuals and add them to the population. Creating an individual will execute the __init__ function 
        # of class Individual, which then will result in this individual playing snake.
        if use_tqdm:
            for i in tqdm(range(size), desc = 'Building Population'):
                individual = Individual(i+1, self.evolution_step, self.verbose)
                self.individuals.append(individual)
        else:
            for i in range(size):
                individual = Individual(i+1, self.evolution_step, self.verbose)
                self.individuals.append(individual)
            
    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)})"
    # Define a funcion that receives a population and evolves it using a GA. It also receives evolution_step to keep track of where we are at in the process.
    #def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism):
    def evolve(self):

        # IMPLEMENT HERE: Genetic evolution of the population



        ########
        # CODE #
        ########



        # ARITHMETIC CROSSOVER

        # CHANGE THIS ACCORDING TO HOW WE WANT TO DO THIS - For now: Get two random indices from our population and get the corresponding individuals
        parents_indices = sample(range(len(self.individuals)), 2)

        # Perform arithmetic crossover on those two parents.
        # This will change the weights of these individuals! This means that there is no need to catch what the function returns
        # because it writes the changes into our original individuals. The parents become the offspring.
        arithmetic_co(self.individuals[parents_indices[0]], self.individuals[parents_indices[1]])



        ########
        # CODE #
        ########



        # Update the population's evolution step
        self.evolution_step += 1
        if self.verbose:
            print()
            print("Evolution step updated. New evolution step:", self.evolution_step)

        # Update each individual's evolution_step
        for indiv in self.individuals:
            indiv.evolution_step = self.evolution_step

        return self.individuals

    # Dave's evolve method. Will keep it here for now for inspiration
        if False:
            # evolve(self,
                    # gens, #Number of generations to be produced
                    # select, #Selection function
                    # crossover, #Crossover function
                    # mutate, #Mutation function
                    # constant_ms = None, #Geometric Mutation coefficient 
                    # co_p, #crossover probability
                    # mu_p, #mutation probability
                    # elitism = False, #wheter to perform elitisim
                    # record_diversity = False, #wheter to record diversity
                    # fitness_sharing = False #wheter to perform fitness sharing
                    # )
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
                if elitism == True: #argument of evolve attribute
                    #saving a deepcopy of the best individual of the population
                    elite = deepcopy(max(self.individuals, key = attrgetter('fitness')))
                    
                new_pop = []
                while len(new_pop) < self.size:
                    offspring1, offspring2 = select(self), select(self) #argument of evolve attribute
                    # Crossover
                    if random() < co_p: #argument of evolve attribute
                        crossover(offspring1, offspring2) #argument of evolve attribute
                        
                    # Mutation
                    if random() < mu_p: #argument of evolve attribute
                        if constant_ms != None:
                            #GEOMETRIC MUTATION
                            mutate(offspring1, constant_ms) #argument of evolve attribute
                        else:
                            mutate(offspring1)
                    if random() < mu_p: #argument of evolve attribute
                        if constant_ms != None:
                            #GEOMETRIC MUTATION
                            mutate(offspring2, constant_ms) #argument of evolve attribute
                        else:
                            mutate(offspring2)
    
                    new_pop.append(Individual(weights = offspring1.weights))
                    if len(new_pop) < self.size:
                        new_pop.append(Individual(weights = offspring1.weights))
                
                if elitism == True: #argument of evolve attribute
                    #finding worst Individual of the new population
                    least_fit = min(new_pop, key = attrgetter('fitness'))
                    #substituting the worst individual of the new population with the best one from the previous one
                    new_pop[new_pop.index(least_fit)] = elite
                
                self.individuals = new_pop
                
                #updating the evolution step                
                self.evolution_step += 1
                for indiv in self.individuals:
                    indiv.evolution_step = self.evolution_step
         
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')



if False:
    # This is where the execution of this script starts.
    if __name__ == '__main__':

        # Initialise an evolution step counter
        evolution_step = 1

        # Initialise a boolean that says that evolution should go on
        keep_evolving = True

        # Define how large our population should be and initialise it by calling Population (and executing its __init__ function)
        pop_size = 5
        population = Population(pop_size, verbose=True)
        
        # While we want to keep evolving... 
        while keep_evolving:

            # Increment evolution_step
            evolution_step += 1

            # Evolve our population
            population.evolve()

            # Let evolved population play
            for i in population:
                i.play()

            # REMOVE THIS LATER; Should be replaced by something that sets keep_evolving to False if optimum is reached.
            # For now this defines after how many evolutions steps the program terminates.
            if evolution_step >= 3:
                keep_evolving = False

        # Print a final message to show that the program finished executing.
        print()
        print('All done.')