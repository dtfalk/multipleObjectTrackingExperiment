import pygame as pg
import sys
from helpers.constants import *
from helpers.messageScreens import multiLineMessage

# returns true if user enters a valid key (a-z or 0-9 or spacebar)
def isValid(key, requestType):

    # response only allows a-z and spaces
    if requestType == 'name':
        if 97 <= key <= 122 or key == 32:
            return True

    # subject number and level selection only allow digits
    elif requestType == 'subject number' or requestType == 'starting level (1 - 99)':
        if 48 <= key <= 57:
            return True
        
    return False
    
# gets user's response and subject ID
def getUserInfo(requestType, win):

    response = "" 
    exit = False

    # event loop
    while True:
        for event in pg.event.get():

            # if user presses a key, then...
            if event.type == pg.KEYDOWN:

                # lets the user quit
                if event.key == generalQuitKey:
                    exit_key = generalQuitKey
                    exit = True
                    
                # if they press enter or return, then...
                if event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    
                    if requestType == 'name' or requestType == 'subject number' or \
                    (requestType == 'starting level (1 - 99)' and (1 <= int('0' + response) <= 99)):
                        
                        # set the exit key to the key they pressed and set the exit boolean to true
                        exit_key = event.key
                        exit = True
                
                # delete last character if they press backspace or delete
                elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                    response = response[:-1] 
                
                # if they enter a valid key (a-z, 0-9, or spacebar)
                elif isValid(event.key, requestType):
                    if (pg.key.get_mods() & pg.KMOD_CAPS) or (pg.key.get_mods() & pg.KMOD_SHIFT):
                        response = response + chr(event.key).upper()
                    else:
                        response = response + chr(event.key)
        if exit == True:
            break
        win.fill(backgroundColor) 
        text = "Please enter the requested information. Then press Enter or Return to continue. Press ESC to exit or inform the observer of your decision. \n\n"
        multiLineMessage(text + f'\n{requestType}: ' + response, mediumFont, win)
        pg.display.flip()

    # if the user pressed either return or enter, then we continue
    if exit_key == pg.K_RETURN or exit_key == pg.K_KP_ENTER:
        return response 
    
    # otherwise, they pressed the exit key and we exit the game
    else:
        pg.quit()
        sys.exit()