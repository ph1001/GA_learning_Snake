# This script is heavily inspired by this blogpost: https://thingsidobysanil.wordpress.com/2018/11/12/87/

# Import libraries and components from snake
from snake import controlled_run, dis_width, dis_height, snake_block, automatic_mode, detailed_console_outputs
import numpy as np
from keras import layers, models
import math

# Define a funcion that receives a population and evolves it using a GA. It also receives evolution_step to keep track of where we are at in the process.
def evolve(population, evolution_step):

    # IMPLEMENT HERE: Genetic evolution of the population







    # Update each individual's evolution_step by using evolution_step that is passed to this function
    for indiv in population:
        indiv.evolution_step = evolution_step

    return population

# Class Individual. Instances of this class play snake and make up a population.
class Individual():

    # Define a function that lets an individual play snake
    def play(self):

        # Start the game by calling the function controlled_run from snake.py and receive the fitness resulting 
        # from the games_to_play games played by this individual in this evolution step
        # games_to_play is defined in snake.py
        fitness = controlled_run(self, self.ind_number, self.evolution_step)
        print('Evolution step ' + str(self.evolution_step) + ':, Individual ' + str(self.ind_number) + ' is done playing.')

        # Update this individual's fitness
        self.fitness = fitness

    # init function of class Individual
    def __init__(self, ind_number, evolution_step):

        # Give this individual a number
        self.ind_number = ind_number

        # Initialise this individual's evolution step with 1
        self.evolution_step = evolution_step

        # Print game's width, height and snake's width
        if detailed_console_outputs:
            print(dis_width, dis_height, snake_block)

        # Create a neural network that will learn to play snake
        self.model = models.Sequential()
        self.model.add(layers.Dense(64, activation = 'relu', input_dim = 53))
        self.model.add(layers.Dense(4, activation = 'softmax'))

        # Play a game
        self.play()

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
        sight_dist = 3
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

# This is where the execution of this script starts.
if __name__ == '__main__':

    # Initialise an evolution step counter
    evolution_step = 1

    # Initialise a boolean that says that evolution should go on
    keep_evolving = True

    # Initialise an empty list for our population and define how large the population should be
    population = []
    pop_size = 2

    # Create individuals and add them to the list. Creating an individual will execute the __init__ function of class Individual,
    # which then will result in this individual playing snake
    for i in range(pop_size):
        individual = Individual(i+1, evolution_step)
        population.append(individual)
    
    # While we want to keep evolving... 
    while keep_evolving:

        # Increment evolution_step
        evolution_step += 1

        # Evolve our population
        population = evolve(population, evolution_step)

        # Let evolved population play
        for i in population:
            i.play()

        # REMOVE THIS LATER; Should be replaced by something that sets keep_evolving to False if optimum is reached
        if evolution_step >= 4:
            keep_evolving = False

    # Print a final message to show that the program finished executing.
    print()
    print('All done.')