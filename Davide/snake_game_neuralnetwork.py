#!/usr/bin/env python
# coding: utf-8

import pygame
import time
import random
import numpy as np
 
        
#DEFINIG 3 DISPLAY FUNCTIONS
    
def Your_score(score, yellow, score_font, dis):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
    
    
def our_snake(dis, black, snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
    
    
def message(msg, color, dis_width, dis_height, font_style, dis):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
    
#MAIN GAME FUNCTION

def gameLoop(model, speed = 15, sight = 3):
    
    #SETTINGS FOR DISPLAY
    
    pygame.init()
 
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)
     
    dis_width = 800
    dis_height = 600
     
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Shubham Snake Game')
     
    clock = pygame.time.Clock()
     
    snake_block = 10
    snake_speed = speed
    
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    
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
    
    #GAME LOOP
    
    clock.tick(snake_speed)
    #Initializing moves and age variables
    moves = 0
    age = 0
    
    while not game_over:
        
        # end of game; not automatic; will need to remove for final version
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red, dis_width, dis_height, font_style, dis)
            Your_score(Length_of_snake - 1, yellow, score_font, dis)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(model, snake_speed, sight)
        
                        
        #Preparing input for the NN
 
        #distances to walls
        distance_hwall_u = dis_height -y1
        distance_hwall_d = y1
        distance_vwall_u = dis_width - x1
        distance_vwall_d = x1
        #distances to food
        distance_food_y = foody - y1
        distance_food_x = foodx - x1
 
 
        #VISION MATRIX
 
        # Define a sight distance (number of squares counted from the 
        #edges of the snake's head; field of vision is a square as well)
        sight_dist = sight
        edge_length = 1+2*sight_dist
 
        # Compute the "field of vision" of the snake; it is made up of 
        #a square array with the length of 1+2*sight_dist
        # Side note: Possible positions in the game grid (without hitting 
        #the wall): Min: (0,0), Max: (790,590) - This is specified in snake.py
        
        # Initialise a field of vision with all zeros
        fov = np.zeros((edge_length, edge_length))
        
        # Give the snake's head, snake_List, foodx, and foody shorter names
        s_head = (x1, y1)
        s_list = snake_List
        fx, fy = (foodx, foody)
 
 
         # Iterate over all elements of our field of vision array
        for i in range(edge_length):
             for j in range(edge_length):
         
                 # Decrement/increment our indices in such a way that they 
                 #represent the relative position
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
                     #print(fov)
 
        input_nn = [distance_hwall_u, distance_hwall_d, distance_vwall_u, 
                    distance_vwall_d, #distances to walls
                    distance_food_y, distance_food_x, #distances to food
                    x1, y1]#snake head
 
        #Transorm input intpo np.array
        input_nn = np.array(input_nn)
        #Fixing the shape so it can be used for the NN
        input_nn.shape = (1,8)
        #Concatenating the vision matrix to the input array                
        fov.shape = (1,49)
        input_nn = np.concatenate((input_nn, fov), axis = 1)
 
        #Producing output of the model, the output are probabilities
        #for each move, using np.argmax to get the index of the 
        #highest probability
        output = np.argmax(model.predict(input_nn))
 
        #print input and output through the game to check
        print(f'Input : {input_nn[:,:8]}')
        print(f'Vision matrix : \n {fov}')
        print(f'Output : {output}')
 
         #Increasing age and moves variables
        age += 1
        moves += 1
         #After 50 moves without getting a fruit or dying the snake is 'stuck' therefore game is over
        if moves == 50:
            game_close = True
        
        print(f'Moves : {moves}, age : {age}')
                        
        #COMMAND LOOP
        for event in pygame.event.get():


                                    
                #Command pad, moves the snake according to the output of the NN
                if output == 0:
                    x1_change = -snake_block
                    y1_change = 0
                    #Adding random event to pygame.event queque to make it go 
                    #further
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
                    pygame.event.post(event)
                elif output == 1:
                    x1_change = snake_block
                    y1_change = 0
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
                    pygame.event.post(event)
                elif output == 2:
                    y1_change = -snake_block
                    x1_change = 0
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
                    pygame.event.post(event)
                elif output == 3:
                    y1_change = snake_block
                    x1_change = 0
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
                    pygame.event.post(event)
        
        
        #CALCULATIONS OF OUTCOMES OF THE MOVE
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
            #game_over = True NEED TO CHANGE FOR FINAL VERSION
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
                #game_over = True NEED TO CHANGE FOR FINAL VERSION
                
        our_snake(dis, black, snake_block, snake_List)
        Your_score(Length_of_snake - 1, yellow, score_font, dis)
    
        pygame.display.update()
    
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            #Resetting moves to 0
            moves = 0
    
        
    pygame.quit()
    return Length_of_snake, moves







