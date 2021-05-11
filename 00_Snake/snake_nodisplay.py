# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 17:16:05 2021

@author: utente
"""

# This game is an adapted version of the Snake game available here: https://github.com/shubham1710/snake-game-python

# Import libraries
import random

# Define display width and heigth
dis_width_nodisplay = 200
dis_height_nodisplay = 200

# Define the width of one snake square
snake_block_nodisplay = 10

# Define the snake's moving speed (put it really high to execute the programm at max speed)
snake_speed = 1000

# Define a function that executes games_to_play games for a given individual 
# and that returns a fitness computed as the average of the fitnesses resulting from these games.
# games_to_play is defined above.
def controlled_run_nodisplay(individual, ind_number, evolution_step, games_to_play, verbose, moves_till_stuck):

    # Initialize a games counter as a global variable
    global games_counter
    games_counter = 0

    # Some printing for debugging purposes
    if verbose:
        print("Games counter initialised.")
        print("Games counter:", games_counter)
    
    
    
    # Define a function that executes the Snake game. It calls itself recursively if games_to_play is greater than 1
    # It returns a list of the fitnesses that result from these games (if games_to_play >1) // this game (if games_to_play = 1)
    def gameLoop_nodisplay(score_list, age_list, verbose, moves_till_stuck):
        
        # Increment the games counter
        global games_counter
        games_counter += 1

        # Some printing for debugging purposes
        if verbose:
            print("Games counter incremented.")
            print("Games counter:", games_counter)

        # Set game_over and game_close to False. These two values determine if the two while loops below keep executing
        game_over = False
        game_close = False

        # Define the snake's starting point
        x1 = dis_width_nodisplay / 2
        y1 = dis_height_nodisplay / 2

        # Initialise variables for the snake's move direction
        x1_change = 0
        y1_change = 0

        # Initialise a list that will contain the positions of the snake's squares and initialise the length of the snake with 1
        snake_List = []
        Length_of_snake = 1

        # Randomly place the first food item
        foodx = round(random.randrange(0, dis_width_nodisplay - snake_block_nodisplay) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height_nodisplay - snake_block_nodisplay) / 10.0) * 10.0

        #Initializing moves and age variables
        moves = 0
        age = 0

        # game_over is declared above and changes to True when the game is supposed to end
        while not game_over:
            
            # game_close is declared above and is set to True when a game ended. 
            # The following code determines what to do next (play another game or finish).
            while game_close == True:



    
                # Determine wether to finish or to play another game
                if games_counter < games_to_play:
                    score_list, age_list = gameLoop_nodisplay(score_list, age_list, verbose, moves_till_stuck)
                else:
                    game_over = True
                    game_close = False


            # In the very first game move, let snake simply go up automatically
            # In all game moves afterwards, call function control(), passing information on the current state of the game and get an action back
            # in oder to receive information on what move to make.
            if snake_List == []:
                
                # Some printing for debugging purposes
                if verbose:
                    print('First iteration - Snake goes up automatically.')

                # Pass the command that refers to 'go up', either in manual or in automatic mode
 
                game_action = 3

            # From the second move onwards      
            else:
                # Gather information on the current state of the game
                game_state = {'snake_Head':snake_Head, 'snake_List':snake_List, 'foodx':foodx, 'foody':foody}
                # Pass it to control()
                game_action = individual.control(game_state)


            # In automatic mode: Process the action received from the NN in the same way a keyboard input would have been processed in the original version of the game
            if game_action == 1:
                x1_change = -snake_block_nodisplay
                y1_change = 0
            elif game_action == 2:
                x1_change = snake_block_nodisplay
                y1_change = 0
            elif game_action == 3:
                y1_change = -snake_block_nodisplay
                x1_change = 0
            elif game_action == 4:
                y1_change = snake_block_nodisplay
                x1_change = 0

            #Increasing age and moves variables
            age += 1
            moves += 1

            # After moves_till_stuck moves without getting a fruit or dying the snake is 'stuck' therefore game is over
            if moves == moves_till_stuck:
                game_close = True
        
            # Some printing for debugging purposes
            if verbose:
                print(f'Moves : {moves}, age : {age}')
    
            # If the snake hit a wall, the game is over
            if x1 >= dis_width_nodisplay or x1 < 0 or y1 >= dis_height_nodisplay or y1 < 0:
                game_close = True

            # Increment / decrement the values of the position of our snake according to the move that is being made
            x1 += x1_change
            y1 += y1_change


            # Update the position of the snake's head and append it to the list that defines the positions of our snake
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)

            # Not sure about the if clause but this part is for deleting the last element of the snake (because it moves forward)
            # I think the if clause is skipped if the snake just ate and therefore grows
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
    
            # If the snake ran into itself, the game is over
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
    
    
            # If the snakes eats a food item, randomly place a new food item, increase the length of the snake by 1, and reset the moves counter to 0
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width_nodisplay - snake_block_nodisplay) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height_nodisplay - snake_block_nodisplay) / 10.0) * 10.0
                Length_of_snake += 1
                moves = 0

        # This would quit Pygame and our programm. We don't want that.
        #pygame.quit()
        #quit()

        # Compute the current score (one less than the snake's length)
        score = Length_of_snake - 1

        # Compute fitness resulting from this game and store it in the list of fitnesses
        score_list.append(score)
        age_list.append(age)

        # Return the current list of fitnesses
        return score_list, age_list
    
    # Initialise a list for storing the fitnesses resulting from the games_to_play games for this individual in this evolution step
    score_list, age_list = [], []

    # Call gameLoop_nodisplay, passing the empty list of fitnesses to it and receiving the list of fitnesses 
    # from it that results from the games_to_play games for this individual in this evolution step
    score_list, age_list = gameLoop_nodisplay(score_list, age_list, verbose, moves_till_stuck)

    # Print the list of fitnesses of this individual in this evolution step
    
    if verbose:
        print()
        print('Score and ages of this/these', games_to_play, 'game(s):', score_list, age_list)

    # Calculate the final fitness of this individual in this evolution step as the mean of the fitnesses contained in the list of fitnesses
    score = sum(score_list) / games_to_play
    age = sum(age_list) / games_to_play
    if verbose:
        print('Resulting (mean) score and age' , score, age)

    # Return the resulting mean fitness for the games_to_play games played by this individual in the evolution step
    return score, age