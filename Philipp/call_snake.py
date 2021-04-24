from snake import controlled_run

# This script is heavily inspired by this blogpost: https://thingsidobysanil.wordpress.com/2018/11/12/87/

class Wrapper():

    def __init__(self):
        # Start the game
        controlled_run(self)

    def control(self):

        # No input implemented yet. This function will receive information from a running snake game about the current state of the game.

        print("controll() was called.")

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