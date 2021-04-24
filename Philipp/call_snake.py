from snake import controlled_run, dis_width, dis_height, snake_block
import numpy as np

# This script is heavily inspired by this blogpost: https://thingsidobysanil.wordpress.com/2018/11/12/87/

class Wrapper():

    def __init__(self):

        # Print game's width, height and snake's width
        print(dis_width, dis_height, snake_block)

        # Start the game
        controlled_run(self)

    def control(self, game_state):

        # No input implemented yet. This function will receive information from a running snake game about the current state of the game.

        print("controll() was called.")

        # In the very first iteration, simply pass "up"
        if game_state['snake_List'] == []:
            print('"Up" was passed automatically.')
            return 'w'

        # Process the information received about the current state of the game

        print('snake_List:', game_state['snake_List'])
        print('snake_Head:', game_state['snake_Head'])
           
        # Define a sight distance (number of squares counted from the edges of the snake's head; field of vision is a square as well)
        sight_dist = 3
        edge_length = 1+2*sight_dist

        # Compute the "field of vision" of the snake; it is made up of a square array with the length of 1+2*sight_dist
        # Side note: Possible positions in the game grid (without hitting the wall): Min: (0,0), Max: (790,590) - This is specified in snake.py
        
        # Initialise a field of vision with all zeros
        fov = np.zeros((edge_length, edge_length))
        
        # Give the snake's head and snake_List a shorter name
        s_head = game_state['snake_Head']
        s_list = game_state['snake_List']

        # Iterate over all elements of our field of vision array
        for i in range(edge_length):
            for j in range(edge_length):
                
                # Decrement/increment our indices in such a way that they represent the relative position
                rel_pos_x = j - sight_dist
                rel_pos_y = i - sight_dist

                # Check if the currently looked at field of vision element contains a part of our snake
                snake_body = [s_head[0] + rel_pos_x * snake_block, s_head[1] + rel_pos_y * snake_block] in s_list
                # If so, write -1 in the respective field of vision cell
                if snake_body:
                    fov[i,j] = -1
        print(fov)

        # Define some valid inputs (this will not be relevant anymore once the Neural Network is implemented)
        valid_inputs = ['w','a','s','d']

        # Initialise a variable that says if a valid input was received
        no_valid_input = True

        # Until a valid input was received, ask for one
        while no_valid_input:
            game_action = str(input())
            if game_action in valid_inputs:
                no_valid_input = False

        return game_action

if __name__ == '__main__':
    w = Wrapper()