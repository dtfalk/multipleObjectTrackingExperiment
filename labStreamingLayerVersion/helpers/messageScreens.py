import sys
import pygame as pg
from .constants import backgroundColor, BLACK, winWidth, winHeight, boundarySize, correctAudioPath, incorrectAudioPath, selectionDuration
from .constants import levelScreenTime, currentScoreScreenTime, trialPerformanceScreenTime, \
                        newHighscoreScreenTime, finalScoreScreenTime, highscoreScreenTime, timeupScreenTime
from .constants import extraLargeFont, largeFont, mediumFont
from .constants import eyesOpenContinueKey, eyesClosedContinueKey, startPracticeTrialsKey, startRealTrialsKey, \
                        instructionsScreenContinueKey, breakScreenContinueKey, exitOnceFinishedKey, \
                        submitAnswerKeyString, generalQuitKey
from .drawing import drawBoundaries, blankSquareScreen


# function to centralize/handle the different message screens
def messageScreen(messageType, args, eventsOutlet, win):

    # ==============================================================
    # select message based on message screen
    # general pattern is to collect the text in the "text" variable
    # and then call the function that draws that text on the screen
    # --------------------------------------------------------------
    # [Conditions are shown in (rough) order of appearance]
    # ==============================================================

    # message screen displaying the instructions for the eyes open resting state
    if messageType == 'eyesOpenScreen':
        multiLineMessage(eyesOpenText, extraLargeFont, win)
        pg.display.flip()
        waitKey(eyesOpenContinueKey, eventsOutlet, win)

    # message screen displaying the instructions for the eyes closed resting state   
    elif messageType == 'eyesClosedScreen':
        multiLineMessage(eyesClosedText, extraLargeFont, win)
        pg.display.flip()
        waitKey(eyesClosedContinueKey, eventsOutlet, win)
    
    # message screen before starting guide trials
    elif messageType == 'guideStartScreen':
        text = instructionsText(args[0], args[1])
        multiLineMessage(text, extraLargeFont, win)
        pg.display.flip()
        waitKey(instructionsScreenContinueKey, eventsOutlet, win)
    
    # message screen before starting practice trials
    elif messageType == 'practiceStartScreen':
        multiLineMessage(practiceStartText, extraLargeFont, win)
        pg.display.flip()
        waitKey(startPracticeTrialsKey, eventsOutlet, win)

    # message screen before starting real trials
    elif messageType == 'realTrialsStartScreen':
        multiLineMessage(realTrialsStartText, extraLargeFont, win)
        pg.display.flip()
        waitKey(startRealTrialsKey, eventsOutlet, win)
    
    # message screen displaying the user's current level
    elif messageType == 'levelScreen':
        win.fill(backgroundColor)
        drawBoundaries(win)
        text = levelText(args[0])
        messageToScreenCentered(text, largeFont, win)
        pg.display.flip()
        pg.time.delay(levelScreenTime)
    
    # message screen displaying the user's current score
    elif messageType == 'scoreScreen':
        win.fill(backgroundColor)
        drawBoundaries(win)
        text = scoreText(args[0])
        messageToScreenCentered(text, largeFont, win)
        pg.display.flip()
        pg.time.delay(currentScoreScreenTime)
    
    # message screen for if the user selects an incorrect number of balls and tries to submit
    elif messageType == 'incorrectNumberOfSelectionsScreen':
        text = tooFewSelectedText(args[0])
        messageToScreenCentered(text, largeFont, win)
        pg.display.flip()
    
    # message screen for if user correctly identified all of the targets
    elif messageType == 'correctScreen':
        win.fill(backgroundColor)
        drawBoundaries(win)
        text = correctText(args[0])
        messageToScreenCentered(text, largeFont, win)
        pg.display.flip()

        # play audio
        pg.mixer.music.load(correctAudioPath)
        pg.mixer.music.set_volume(0.22)
        pg.mixer.music.play()
        pg.time.delay(trialPerformanceScreenTime)
        pg.mixer.music.unload()
    
    # message screen for if the user identified at least one of the distractors as a target
    elif messageType == 'incorrectScreen':
        win.fill(backgroundColor)
        drawBoundaries(win)
        text = incorrectText(args[0], args[1])
        messageToScreenCentered(text, largeFont, win)
        pg.display.flip()

        # play audio
        pg.mixer.music.load(incorrectAudioPath)
        pg.mixer.music.set_volume(0.22)
        pg.mixer.music.play()
        pg.time.delay(trialPerformanceScreenTime)
        pg.mixer.music.unload()

    # displays if the user takes too long to submit their answers
    elif messageType == 'timeupScreen':
        win.fill(backgroundColor)
        drawBoundaries(win)
        messageToScreenCentered(timeUpText, largeFont, win)
        pg.display.flip()
        pg.time.delay(timeupScreenTime)

    # message screen informing the user that they have earned a break
    elif messageType == 'breakScreen':
        win.fill(backgroundColor)
        drawBoundaries(win)
        messageToScreenCentered(breakText, mediumFont, win)
        pg.display.flip()
        waitKey(breakScreenContinueKey, eventsOutlet, win)
    
    # message screen displaying the user's final score
    elif messageType == 'finalScoreScreen':
        win.fill(backgroundColor)
        drawBoundaries(win)
        text = finalScoreText(args[0])
        messageToScreenCentered(text, largeFont, win)
        pg.display.flip()
        pg.time.delay(finalScoreScreenTime)

    # message screen informing the user that they have attained a highscore
    elif messageType == 'newHighscoreScreen':
        win.fill(backgroundColor)
        drawBoundaries(win)
        text = newHighscoreText(args[0])
        messageToScreenCentered(text, largeFont, win)
        pg.display.flip()
        pg.time.delay(newHighscoreScreenTime)
    
    # message screen displaying the current highscores
    elif messageType == 'highscoresScreen':
        win.fill(backgroundColor)
        text = highscoresText(args[0])
        multiLineMessage(text, extraLargeFont, win)
        pg.display.flip()
        pg.time.delay(highscoreScreenTime)

    # message screen for once the entire experiment is done
    elif messageType == 'experimentFinishedScreen':
        multiLineMessage(experimentFinishedText, extraLargeFont, win)
        pg.display.flip()
        waitKey(exitOnceFinishedKey, eventsOutlet, win)

    elif messageType == 'LSLPrepScreen':
        drawBoundaries(win)
        win.fill(backgroundColor)
        messageToScreenCentered(LSLPrepText, mediumFont, win)
        pg.display.flip()
        pg.time.delay(5000)

    return

# function to draw/fit a multiline message to the screen
def multiLineMessage(text, textsize, win):

    # set font and text color
    font = pg.font.SysFont("arial", textsize)
    color = BLACK

    # Initialize variables for layout calculations
    xPos_start = 0.05 * (winWidth - boundarySize)
    yPos_start = 0.05 * (winHeight - boundarySize)
    xMax = 0.95 * (winWidth - boundarySize)
    yMax = 0.95 * (winHeight - boundarySize)

    # Function to calculate if the text fits within the designated area
    def fitsWithinArea(text, font):

        # starting x and y coordinate for the text
        xPos = xPos_start
        yPos = yPos_start

        # Get line height based on font size
        lineHeight = font.get_linesize() 
        lines = text.split('\n')
        for line in lines:

            # Handle empty lines for consecutive newlines
            if line == '':
                yPos += lineHeight
            
            # Handle non-empty lines
            else:
                words = line.split()
                for word in words:
                    word_surface = font.render(word, True, color)
                    wordWidth, _ = word_surface.get_size()

                    # Check if new word exceeds the line width
                    if xPos + wordWidth > xMax: 

                        # Reset to start of the line
                        xPos = xPos_start

                        # Move down by the height of the previous line
                        yPos += lineHeight

                    # Check if adding another line exceeds the page height
                    if yPos + lineHeight > yMax:
                        return False
                    
                    # Blit here for size calculation
                    win.blit(word_surface, (xPos, yPos))

                    # Move xPos for the next word, add space
                    xPos += wordWidth + font.size(" ")[0] 
                
                # reset x position and increment y position by height of text
                xPos = xPos_start
                yPos += lineHeight
        return True

    # Adjust font size until the text fits within the area
    while not fitsWithinArea(text, font) and textsize > 1:
        textsize -= 1
        font = pg.font.SysFont("arial", textsize)

    # Draw the background and boundaries only once
    win.fill(backgroundColor)
    drawBoundaries(win)

    # Now draw the text with the properly adjusted font size
    xPos = xPos_start
    yPos = yPos_start
    lineHeight = font.get_linesize()
    lines = text.split('\n')

    # iterate over each line
    for line in lines:

        # Handle empty lines for consecutive newlines
        if line == '':
            yPos += lineHeight

        # Handle non-empty lines
        else:

            # split the line into its constituent words
            words = line.split()

            # iterate over each words
            for word in words:

                # render the word and get the size of the word
                word_surface = font.render(word, True, color)
                wordWidth, _ = word_surface.get_size()

                # Check if word exceeds line width
                if xPos + wordWidth > xMax:

                    # reset x position and increment y position
                    xPos = xPos_start
                    yPos += lineHeight
                
                # draw word
                win.blit(word_surface, (xPos, yPos))

                # increment x position by word width
                xPos += wordWidth + font.size(" ")[0]
            
            # reset x position and increment y position
            xPos = xPos_start
            yPos += lineHeight

    return


# function to draw a message that is centered (will be drawn on top of existing things on the screen)
def messageToScreenCentered(text, textsize, win, color = BLACK):

    # set the font and the fontsize
    msg = pg.font.SysFont("arial", textsize)

    # create a text surface
    textSurface = msg.render(text, True, color)

    # extract the rectangle the text is drawn on so we can center it
    textRect = textSurface.get_rect()

    # set the center of the text rectangle to the center of the screen
    textRect.center = (winWidth / 2, winHeight / 2)

    # draw the message and display
    win.blit(textSurface, textRect)
    
    return


# stops game execution until a particular key is pressed
def waitKey(key, eventsOutlet, win):

    # just keep waiting until the relevant key is pressed
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == key:
                    return
                elif event.key == generalQuitKey:
                    blankSquareScreen('endOfExperiment', eventsOutlet, win)
                    pg.quit()
                    sys.exit()

# ======================================================================================
# ======================================================================================
# ======================================================================================
# ======================================================================================
# ====  The functions below are for returning text for the messageScreens function  ====

# function to return the text displaying which level the user is on
def levelText(level):
    return f'Level {level}'

# function to generate text for when the user gets a level correct
def correctText(totalTargets):
    return f'Good! {totalTargets} out of {totalTargets} correct'

# function to generate text for when the user gets a level incorrect
def incorrectText(numberOfSelectedTargets, totalTargets):
    return f'Sorry... {numberOfSelectedTargets} out of {totalTargets} correct'

# function to return text for when the user tries to submit without having selected
# enough targets
def tooFewSelectedText(numberOfTargets):
    return f'You must select {numberOfTargets} circles'

# instructions for how the experiment is played 
def instructionsText(numberOfTargets, totalBalls):
    return f'You will first see a cross at the center of the screen. Please focus your gaze to that cross.\n\n\
{totalBalls} circles will appear on the screen, and the cross will disappear.\n\n\
{numberOfTargets} of the circles will be highlighted and then all of the circles will start to move.\n\n\
Keep track of those {numberOfTargets} flashed circles.\n\n\
When the circles stop moving select which circles you have been tracking by clicking them.\n\n\
When you have made your selection press {submitAnswerKeyString} to submit.\n\n\
You will have {int(selectionDuration / 1000)} seconds to make your choice.\n\n\
Please remember to focus your eyes on the cross.\n\n\
After the cross disappears you may move your eyes, but please keep them focused on the screen.\n\n\
If you need to stop, then let the experimenter know.\n\n\
Press the "{chr(instructionsScreenContinueKey - pg.K_a + ord('a'))}" key to start when you are ready.\n\n'

# function to return the text informing the user of their score
def scoreText(score):
    return f'Score: {score}'

# function to return the text informing the user of their score
def finalScoreText(score):
    return f'Final Score: {score}'

# returns the text informign the user of the current high scores
def highscoresText(highScores):
    return f'High Scores\n\n\
1. {highScores[0]}\n\
2. {highScores[1]}\n\
3. {highScores[2]}\n\
4. {highScores[3]}\n\
5. {highScores[4]}'

# returns the text for the rank on the leaderboard that the subject achieved
def newHighscoreText(rank):
    return f'New High Score! You are now #{rank}!'

# ======================================================================================
# ======================================================================================
# ======================================================================================
# ======================================================================================
# ====  The constants below are text for the various messageScreens conditions  ========

# text we show user after they complete the guide
practiceStartText = f'These are practice rounds where you will go through the experiment in normal order, but your answers will not be recorded.\n\n\
After the practice is finished you will move to the real experiments where your responses will be recorded.\n\n\
Press "{chr(startPracticeTrialsKey - pg.K_a + ord('a'))}" to begin the practice rounds.'

# text we show user after they complete the practice trials
realTrialsStartText = f'Remember to keep track of the targets and submit your answers by pressing {submitAnswerKeyString}.\n\n\
Be as quick and accurate as you can!\n\n\
Press the "{chr(startRealTrialsKey - pg.K_a + ord('a'))}" key when you are ready to begin the real experiment.'

# text we show user after they complete the entire experiment
experimentFinishedText = f'The real trials are now over; please let the experimenter know.\n\n\
Thank you for participating!\n\n\
Press "{chr(exitOnceFinishedKey - pg.K_a + ord('a'))}" to exit.'

# text to show the user during their break
breakText = f'You have earned a break! Press "{chr(breakScreenContinueKey - pg.K_a + ord('a'))}" when you are ready to continue.'

# text to show when the user takes too long to submit an answer
timeUpText = "Time's up! Now resetting..."

# text to show user during the eyes open portion of the experiment
eyesOpenText =  f'Please focus your eyes on the cross that will appear at the center of the screen.\n\n\
Do your best to keep your eyes still and your jaw/other muscles relaxed.\n\n\
Press the "{chr(eyesOpenContinueKey - pg.K_a + ord('a'))}" key when you are ready to begin.'

# text to show user during the eyes closed portion of the experiment
eyesClosedText = f'Please close your eyes and do your best not to fall asleep.\n\n\
Do your best to keep your eyes still and your jaw/other muscles relaxed.\n\n\
You will hear a noise when it is time for you to open your eyes.\n\n\
Press the "{chr(eyesClosedContinueKey - pg.K_a + ord('a'))}" key when you are ready to begin.'

# text to show when we are initializing the LSL inlets and outlets
LSLPrepText = 'Initializing LSL connections...'