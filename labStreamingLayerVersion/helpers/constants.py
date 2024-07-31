import os
import pygame as pg
from screeninfo import get_monitors

# ============================================================================
# ============================================================================
# ============================================================================

# frame rate for the game 
FPS = 60 

# Set multiMonitor to True if you are using two monitors and want the game to be displayed
# on the second monitor
# Set to False otherwise
multiMonitor = True

# get window width and height (will handle dpi later?)
winfo = get_monitors()

# if user wants to use a secondary monitor for the game
if multiMonitor and len(winfo) > 1:
    winWidth = winfo[1].width
    winHeight = winfo[1].height
    winX = winfo[1].x
    winY = winfo[1].y
else:
    winWidth = winfo[0].width
    winHeight = winfo[0].height
    winX = winfo[0].x
    winY = winfo[0].y

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (winX, winY)


# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================

# define some font sizes and colors for easy access

# == Font sizes ==
extraLargeFont = winHeight // 5
largeFont = winHeight // 10
mediumFont = winHeight // 20
smallFont = winHeight // 30

# == Greyscale ==
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [128, 128, 128]
SLATEGREY = [112, 128, 144]
DARKSLATEGREY = [47, 79, 79]


# == Yellows ==
YELLOW = [255, 255, 0]
OLIVE = [128,128,0]
DARKKHAKI = [189,183,107]

# == Greens ==
GREEN = [0, 128, 0]
GREENYELLOW = [173, 255, 47]

RED = [255, 50, 50]

# various color constants
# colors
defaultColor = WHITE # default ball color
backgroundColor = GREY # background for the experiment
hoverColor = YELLOW # color of the ball when mouse is hovering over it
clickColor = GREEN # color of the ball when it has been clicked
squareColor = WHITE # color of the square we draw to get the "true time" for tags
borderColor = BLACK # color of the borders on the screen
highlightColor = GREEN # color of ball when selected or highlighted

# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================

# == define the screen boundaries ==

ballRadius = winWidth // 40  # size of balls in pixels
boundarySize = winWidth // 50 # boundary size in pixels
fixationCrossLength = winWidth // 40 # length of the legs on the fixation cross (there are 4 legs)
squareWidth = boundarySize // 2 # width of the "true time" square

# boundaries of the screen (top left corner is considered the origin in pygame)
boundaries = {
    'top': boundarySize, 
    'bottom': winHeight - boundarySize,
    'left': boundarySize,
    'right': winWidth - boundarySize
    }

# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================

# trial progression variables (duration of each phase) in milliseconds

fixationDuration = int(2 * 1000) # time to present fixation cross and objects

highlightDuration = int(2 * 1000)  # time for targets to flash

movementDuration = int(4.5 * 1000)  # time for objects to move around in seconds

selectionDuration = int(60 * 1000)  # time for the user to make a response

squareDuration = int(0.1 * 1000) # how long we display the "true time" square

# ============================================================================
# ============================================================================
# ============================================================================

# paths to the various sounds we use in the game
correctAudioPath = os.path.join(os.path.dirname(__file__), 'sound', 'correct.mp3')
incorrectAudioPath = os.path.join(os.path.dirname(__file__), 'sound', 'incorrect.mp3')
eyesOpenAudioPath = os.path.join(os.path.dirname(__file__), 'sound', 'openEyes.mp3')


# ============================================================================
# ============================================================================
# ============================================================================


# == Game Structure Variables ==

# Attributes and relations between those attributes 
# These are the things that change as the user progresses through levels
# overflow variables are the maximum before an increase in some attribute
# "overflows" into an increase in another attribute. 
distractorsOverflow = 3
speedOverflow = 3

# number of targets and distractors for the first level
startingTargets = 2
startingDistractors = 1

# modify this to change ball speeds
velocityFactor = (winWidth + winHeight) // (2 * 300)

# == how far (in levels) player progresses or regresses based on performance ==
success = 1
failure = -3

# level the practice starts on
startingPracticeLevel = 3

# == Trial variables ==
timeOrTrialsDict = {

    # time that real trials last (in milliseconds)
    # just modify the first number to get game time in minutes
    # you multiply num_minutes by (60 * 1000) to get the number of minutes in milliseconds
    'real' :  1 * (60 * 1000), 

    # number of practice trials
    'practice': 5,

    # number of guide trials
    'guide': 1
}


# ============================================================================
# ============================================================================
# ============================================================================

# == Lengths of time we display various screens ==

# how long we show the highscore screen for (in milliseconds)
highscoreScreenTime = int(5 * 1000)

# how long we show the final score for (in milliseconds)
finalScoreScreenTime = int(1.5 * 1000)

# how long we show the user what level they are on between rounds (in milliseconds)
levelScreenTime = int(1.5 * 1000)

# how long each resting state lasts for (in milliseconds)
restingStateTime = 1000 #int(3 * (60 * 1000))

# how long to show the current score for (in milliseconds)
currentScoreScreenTime = int(2 * 1000)

# how long to inform the user about their new highscore for (in milliseconds)
newHighscoreScreenTime = int(4 * 1000)

# how long to inform the user about their performance on a trial for (in milliseconds)
trialPerformanceScreenTime = int(2 * 1000)

# how long to inform the user that the they took to respond (in milliseconds)
timeupScreenTime = int(2 * 1000)


# ============================================================================
# ============================================================================
# ============================================================================

# == Keys user must press to proceed through various screens ==

# key that the user must press to begin eyes open resting state
eyesOpenContinueKey = pg.K_o

# key that the user must press to begin eyes closed resting state
eyesClosedContinueKey = pg.K_c

# key that the user must press to exit the break screen
breakScreenContinueKey = pg.K_b

# key the user must press to proceed through the instructions
instructionsScreenContinueKey = pg.K_f

# key the user must press to begin the practice trials
startPracticeTrialsKey = pg.K_j

# key the user must press to begin the real trials
startRealTrialsKey = pg.K_m

# key ot press once everything is finished and want to exit the game
exitOnceFinishedKey = pg.K_q

# key to click to submit responses
submitAnswerKey = pg.K_SPACE
submitAnswerKeyString = 'SPACEBAR'

# key to click to quit the game
generalQuitKey = pg.K_ESCAPE
generalQuitKeyString = 'ESCAPE'

# key to skip through some phases of the game
skipKey = pg.K_s

# ============================================================================
# ============================================================================
# ============================================================================

# == Dictionaries for translating between tags and event IDs ==

# Given a dictionary, swaps keys for values and values for keys
# (assumes that the given dictionary constitutes an injection)
def reverseADictionary(dictionary):
    reverseDictionary = {}
    for key, value in dictionary.items():
        reverseDictionary[str(value)] = key
    return reverseDictionary

# Translates each level tag to an event ID number
# 'level 15' ----> 15
def levelTags(tagToEventIdNumberDictionary):
    for i in range(1, 100):
        tagToEventIdNumberDictionary[f'level {i}'] = i
    
    return tagToEventIdNumberDictionary

# Translates each level tag to an event ID number
# 'level 15' ----> 15
def trialTags(tagToEventIdNumberDictionary):
    for i in range(1, 199):
        tagToEventIdNumberDictionary[f'trial {i}'] = 700 + i
    
    return tagToEventIdNumberDictionary

# Translates a user's performance on a trial to a number
def performanceTags(tagToEventIdNumberDictionary):

    for totalTargets in range(1, 15):
        for selectedTargets in range(totalTargets + 1):
            for numberOfDistractors in range(totalTargets + 3):
                tagToEventIdNumberDictionary[f'{selectedTargets} out of {totalTargets} targets identified with {numberOfDistractors} distractors'] = int(f'9{selectedTargets}{totalTargets}{numberOfDistractors}')


# initalize the dictionary with the bulk of the event tags/event ID numbers
tagToEventIdNumberDictionary = {
    'eyesOpenStart': 101,
    'eyesOpenEnd': 102,
    'eyesClosedStart': 103,
    'eyesClosedEnd': 104,
    'startOfRealTrials': 105,
    'fixationStart': 106,
    'highlightStart': 107,
    'movementStart': 108,
    'selectionStart': 109,
    'ballSelected': 110,
    'ballUnselected': 111,
    'selectionSubmitted': 112,
    'timeup': 113,
    'breakStart': 114,
    'breakEnd': 115,
    'endOfRealTrials': 116,
    'endOfExperiment': -1
}

# add in the level tags
tagToEventIdNumberDictionary = levelTags(tagToEventIdNumberDictionary)
performanceTags(tagToEventIdNumberDictionary)
trialTags(tagToEventIdNumberDictionary)

eventIdNumberToTagDictionary = reverseADictionary(tagToEventIdNumberDictionary)


