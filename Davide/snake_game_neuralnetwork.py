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

def gameLoop(model, speed = 15):
    
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
    
    while not game_over:
        
        # end of game; not automatic yet need to change to return also
        #the fitness
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
                        gameLoop(model, speed)
                        
        #COMMAND LOOP
        for event in pygame.event.get():
                
                #Preparing input for the NN
                
                #distances to walls
                distance_hwall_u = dis_height -y1
                distance_hwall_d = y1
                distance_vwall_u = dis_width - x1
                distance_vwall_d = x1
                #distances to food
                distance_food_y = foody - y1
                distance_food_x = foodx - x1
                
                input_nn = [distance_hwall_u, distance_hwall_d, distance_vwall_u, 
                distance_vwall_d, #distances to walls
                distance_food_y, distance_food_x, #distances to food
                x1, y1] #snake head
                
                #NEED TO ADD VISION MATRIX
                
                #Transorm input intpo np.array
                input_nn = np.array(input_nn)
                #Fixing the shape so it can be used for the NN
                input_nn.shape = (1,8)
                
                #Producing output of the model, the output are probabilities
                #for each move, using np.argmax to get the index of the 
                #highest probability
                output = np.argmax(model.predict(input_nn))
                
                #print input and output through the game to check
                print(f'Input : {input_nn}')
                print(f'Output : {output}')
                
                
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
                
        our_snake(dis, black, snake_block, snake_List)
        Your_score(Length_of_snake - 1, yellow, score_font, dis)
    
        pygame.display.update()
    
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
    
        clock.tick(snake_speed)
        

    pygame.quit()







