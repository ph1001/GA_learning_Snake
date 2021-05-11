# This game is an adapted version of the Snake game available here: https://github.com/shubham1710/snake-game-python

# Import libraries
import random
import pygame


# Define display width and heigth
dis_width = 200
dis_height = 200

# Define the width of one snake square
snake_block = 10

# Define the snake's moving speed (put it really high to execute the programm at max speed)
snake_speed = 1000

# Define some colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Define if we want the NNs to be in control (True) or the user via w,a,s, and d (False)
automatic_mode = True

# Choose how many moves an individual is allowed to make until it is considered to be stuck
#MOVED IN controll_game input

# Define a function that executes games_to_play games for a given individual 
# and that returns a fitness computed as the average of the fitnesses resulting from these games.
# games_to_play is defined above.
def controlled_run(individual, ind_number, evolution_step, games_to_play, verbose, moves_till_stuck):

    # Initialize a games counter as a global variable
    global games_counter
    games_counter = 0

    # Some printing for debugging purposes
    if verbose:
        print("Games counter initialised.")
        print("Games counter:", games_counter)
    
    # Start pygame and set up the display
    pygame.init()
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Shubham Snake Game')
    
    # Create a Clock instance
    clock = pygame.time.Clock()

    # Define font styles
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    
    # Define a function that takes the current score and displays it
    def Your_score(score):
        value = score_font.render("Score: " + str(score), True, yellow)
        dis.blit(value, [0, 0])

    # Define a function that takes the current games counter value and displays it (currently not used)
    def show_games_counter(games_counter):
        value = score_font.render("Game #" + str(games_counter), True, yellow)
        dis.blit(value, [0, 100])

    # Define a function that displays the number associated to the currently playing individual
    def show_which_individual():
        value = score_font.render("Individual " + str(ind_number), True, yellow)
        dis.blit(value, [0, 200])

    # Define a finction that displays the current evolution step
    def show_evolution_step():
        value = score_font.render("Evolution step " + str(evolution_step), True, yellow)
        dis.blit(value, [0, 100])
      
    # Define a function that displays the current snake
    def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
    
    # A function to display the "You lost" message
    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])
    
    # Define a function that executes the Snake game. It calls itself recursively if games_to_play is greater than 1
    # It returns a list of the fitnesses that result from these games (if games_to_play >1) // this game (if games_to_play = 1)
    def gameLoop(score_list, age_list, verbose, moves_till_stuck):
        
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
        x1 = dis_width / 2
        y1 = dis_height / 2

        # Initialise variables for the snake's move direction
        x1_change = 0
        y1_change = 0

        # Initialise a list that will contain the positions of the snake's squares and initialise the length of the snake with 1
        snake_List = []
        Length_of_snake = 1

        # Randomly place the first food item
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        #Initializing moves and age variables
        moves = 0
        age = 0

        # game_over is declared above and changes to True when the game is supposed to end
        while not game_over:
            
            # game_close is declared above and is set to True when a game ended. 
            # The following code determines what to do next (play another game or finish).
            while game_close == True:

                # Update display when a game has ended
                dis.fill(blue)
                message("You Lost! Press C-Play Again or Q-Quit", red)
                Your_score(Length_of_snake - 1)
                pygame.display.update()
    
                # Determine wether to finish or to play another game

                # By user input in manual mode
                if not automatic_mode:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_over = True
                                game_close = False
                            if event.key == pygame.K_c:
                                score_list, age_list = gameLoop(score_list, age_list, verbose, moves_till_stuck)
                # By comparing the current value of games_counter with the value of games_to_play in automatic mode
                if automatic_mode:
                    if games_counter < games_to_play:
                        score_list, age_list = gameLoop(score_list, age_list, verbose, moves_till_stuck)
                    else:
                        game_over = True
                        game_close = False
            
            # Process some pygame events - Not sure what it does exactly
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            # In the very first game move, let snake simply go up automatically
            # In all game moves afterwards, call function control(), passing information on the current state of the game and get an action back
            # in oder to receive information on what move to make.
            if snake_List == []:
                
                # Some printing for debugging purposes
                if verbose:
                    print('First iteration - Snake goes up automatically.')

                # Pass the command that refers to 'go up', either in manual or in automatic mode
                if not automatic_mode:
                    game_action = 'w'
                if automatic_mode:
                    game_action = 3

            # From the second move onwards      
            else:
                # Gather information on the current state of the game
                game_state = {'snake_Head':snake_Head, 'snake_List':snake_List, 'foodx':foodx, 'foody':foody}
                # Pass it to control()
                game_action = individual.control(game_state)

            # In manual mode: Process the action received from the user in the same way a keyboard input would have been processed in the original version of the game
            if not automatic_mode:
                if game_action == 'a':
                    x1_change = -snake_block
                    y1_change = 0
                elif game_action == 'd':
                    x1_change = snake_block
                    y1_change = 0
                elif game_action == 'w':
                    y1_change = -snake_block
                    x1_change = 0
                elif game_action == 's':
                    y1_change = snake_block
                    x1_change = 0

            # In automatic mode: Process the action received from the NN in the same way a keyboard input would have been processed in the original version of the game
            if automatic_mode:
                if game_action == 1:
                    x1_change = -snake_block
                    y1_change = 0
                elif game_action == 2:
                    x1_change = snake_block
                    y1_change = 0
                elif game_action == 3:
                    y1_change = -snake_block
                    x1_change = 0
                elif game_action == 4:
                    y1_change = snake_block
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
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True

            # Increment / decrement the values of the position of our snake according to the move that is being made
            x1 += x1_change
            y1 += y1_change

            # Some display stuff
            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

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
    
            # Inside the game display the updated snake, the current score, (the games counter,) 
            # the number associated to our current individual, and the current evolution step
            our_snake(snake_block, snake_List)
            Your_score(Length_of_snake - 1)
            #show_games_counter(games_counter)
            show_which_individual()
            show_evolution_step()
            pygame.display.update()
    
            # If the snakes eats a food item, randomly place a new food item, increase the length of the snake by 1, and reset the moves counter to 0
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1
                moves_till_stuck += 100
    
            # Let the clock iterate
            clock.tick(snake_speed)

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

    # Call gameLoop, passing the empty list of fitnesses to it and receiving the list of fitnesses 
    # from it that results from the games_to_play games for this individual in this evolution step
    score_list, age_list = gameLoop(score_list, age_list, verbose, moves_till_stuck)

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