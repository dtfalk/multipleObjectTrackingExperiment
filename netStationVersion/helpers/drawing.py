# file for drawing various objects on the screen
import pygame as pg
from helpers.constants import *

# draws the black border on the screen
def drawBoundaries(win):
    
    # right boundary
    pg.draw.rect(win, BLACK, pg.Rect(boundaries['right'], 0, boundarySize, winHeight))
    
    # left boundary
    pg.draw.rect(win, BLACK, pg.Rect(0, 0, boundarySize, winHeight))

    # top boundary
    pg.draw.rect(win, BLACK, pg.Rect(0, 0, winWidth, boundarySize))
    
    # bottom boundary
    pg.draw.rect(win, BLACK, pg.Rect(0, boundaries['bottom'], winWidth, boundarySize))

    return


# function that will highlight the targets green
def highlightTargets(distractors, targets, win):

    # color the targets and draw them
    for target in targets:
        target.color = GREEN
        target.drawCircle(win)

    # draw the distractors
    for distractor in distractors:
        distractor.drawCircle(win)

    # display to the user
    pg.display.flip()

    # display for fixed amount of time
    pg.time.delay(highlightDuration)

    # change their color back to the default color
    for target in targets:
        target.color = defaultColor

    # draw to screen
    pg.display.flip()

    return


# function to handle drawing the objects while they are not in motion
def drawStaticBalls(targets, distractors, win):

    # master list containing all of the balls
    masterList = targets + distractors

    # check each ball in the master list
    for ball in masterList:
        ball.drawCircle(win)

    return


# function to handle drawing the objects while they are in motion
def drawMovingBalls(targets, distractors, win):

    # check each ball in the master list
    for ball in targets + distractors:
        ball.detectCollision(targets, distractors)
        ball.drawCircle(win)

    return


# draws the fixation cross users look at before the balls get highlighted
def drawFixationCross(win, color = BLACK):

    # some variables for length of the cross's 4 legs and the width of each leg
    legLength = fixationCrossLength
    legWidth = fixationCrossLength // 5
    widthCenter = winWidth // 2
    heightCenter = winHeight // 2
    
    # draw the horizontal part of the cross
    pg.draw.line(win, color, start_pos = (widthCenter - legLength, heightCenter), end_pos = (widthCenter + legLength, heightCenter), width = legWidth)

    # draw the vertical part of the cross
    pg.draw.line(win, color, start_pos = (widthCenter, heightCenter - legLength), end_pos = (widthCenter, heightCenter + legLength), width = legWidth)

    return


# draws the balls and the fixation cross
def fixationScreen(targets, distractors, win):
    
    # draw the fixation cross
    drawFixationCross(win)

    # draw the balls
    drawStaticBalls(targets, distractors, win)

    return

# draws the screen that the users look at during the eyes open resting state
def drawEyesOpenScreen(win):

    # draw background color
    win.fill(backgroundColor)

    # draw the boundaries
    drawBoundaries(win)

    # draw the fixation cross
    drawFixationCross(win)

    # display to user
    pg.display.flip()

    # put on screen for this amount of time
    pg.time.delay(restingStateTime)

    return

# draws the screen that the users look at during the eyes closed resting state
def drawEyesClosedScreen(win):

    # draw background color
    win.fill(BLACK)

    # display to user
    pg.display.flip()

    # put on screen for this amount of time
    pg.time.delay(restingStateTime)

    # play audio to indicate end of eyes closed
    pg.mixer.music.load(eyesOpenAudioPath)
    pg.mixer.music.set_volume(0.22)
    pg.mixer.music.play()
    pg.time.delay(2000)
    pg.mixer.music.unload()

    return