# This game is an adapted version of the Snake game available here: https://github.com/shubham1710/snake-game-python

# Import libraries
import math
import random

# Decide wether or not we want detailed console outputs (for debugging)
detailed_console_outputs = False

# Define display width and heigth
dis_width = 800
dis_height = 600

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

# Choose how many games should be played per individual and evolution step (the score will be the mean of the scores achieved in these games)
games_to_play = 2

# Choose how many moves an individual is allowed to make until it is considered to be stuck
moves_till_stuck = 100

# Dfeine a function that executes games_to_play (defined above) games for a given individual and that returns a score computed as the average of the scores of these games
def controlled_run(individual, ind_number, evolution_step):

    # Initialize a games counter as a global variable
    global games_counter
    games_counter = 0

    if detailed_console_outputs:
        print("Games counter initialised.")
        print("Games counter:", games_counter)
        
    import pygame
    import time
    import random
    
    pygame.init()
    
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Shubham Snake Game')
    
    clock = pygame.time.Clock()

    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    
    
    def Your_score(score):
        value = score_font.render("Score: " + str(score), True, yellow)
        dis.blit(value, [0, 0])

    def show_games_counter(games_counter):
        value = score_font.render("Game #" + str(games_counter), True, yellow)
        dis.blit(value, [0, 100])

    def show_which_individual(ind_number):
        value = score_font.render("Individual " + str(ind_number), True, yellow)
        dis.blit(value, [0, 200])

    # TO BE IMPLEMENTED
    def show_evolution_step(ind_number):
        value = score_font.render("Evolution step " + str(evolution_step), True, yellow)
        dis.blit(value, [0, 100])
      
    def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
    
    
    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])
    
    
    def gameLoop(fitness_list):
        
        # Increment the games counter
        global games_counter
        games_counter += 1

        if detailed_console_outputs:
            print("Games counter incremented.")
            print("Games counter:", games_counter)

        game_over = False
        game_close = False

        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        #Initializing moves and age variables
        moves = 0
        age = 0

        while not game_over:
    
            while game_close == True:

                dis.fill(blue)
                message("You Lost! Press C-Play Again or Q-Quit", red)
                Your_score(Length_of_snake - 1)
                pygame.display.update()
    
                if not automatic_mode:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_over = True
                                game_close = False
                            if event.key == pygame.K_c:
                                fitness_list = gameLoop(fitness_list)

                if automatic_mode:

                    if games_counter < games_to_play:
                        fitness_list = gameLoop(fitness_list)
                    else:
                        game_over = True
                        game_close = False

                    
    
            # We don't need this in our implementation. Adapted version below.
            if False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            x1_change = -snake_block
                            y1_change = 0
                        elif event.key == pygame.K_RIGHT:
                            x1_change = snake_block
                            y1_change = 0
                        elif event.key == pygame.K_UP:
                            y1_change = -snake_block
                            x1_change = 0
                        elif event.key == pygame.K_DOWN:
                            y1_change = snake_block
                            x1_change = 0
            
            # This part we need
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            # Adapted part:

            # In the very first iteration, let snake simply go up automatically
            # In all iterations afterwards, call function control(), passing information on the current state of the game and get an action back
            if snake_List == []:
                
                if detailed_console_outputs:
                    print('First iteration - Snake goes up automatically.')
                if not automatic_mode:
                    game_action = 'w'
                if automatic_mode:
                    game_action = 3
            else:
                # Gather information on the current state of the game
                game_state = {'snake_Head':snake_Head, 'snake_List':snake_List, 'foodx':foodx, 'foody':foody}
                # Pass it to control()
                game_action = individual.control(game_state)

            if not automatic_mode:
                # Process the action received from the user in the same way a keyboard input would have been processed in the original version of the game
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

            if automatic_mode:
                # Process the action received from the NN in the same way a keyboard input would have been processed in the original version of the game
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
        
            if detailed_console_outputs:
                print(f'Moves : {moves}, age : {age}')
    
            # From here it's original code again
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
    
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
    
            our_snake(snake_block, snake_List)
            Your_score(Length_of_snake - 1)
            #show_games_counter(games_counter)
            show_which_individual(ind_number)
            show_evolution_step(evolution_step)
    
            pygame.display.update()
    
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1
                # Resetting moves to 0
                moves = 0
    
            clock.tick(snake_speed)

        #pygame.quit()
        #quit()

        score = Length_of_snake - 1

        # Compute fitness of this game and store it in fitness_list
        fitness = age*math.exp(score)
        fitness_list.append(fitness)

        return fitness_list
    
    fitness_list = []

    fitness_list = gameLoop(fitness_list)
    print()
    print('Fitnesses of this/these', games_to_play, 'game(s):', fitness_list)

    fitness = sum(fitness_list) / games_to_play
    print('Resulting (mean) fitness', fitness)

    # Return fitness
    return fitness