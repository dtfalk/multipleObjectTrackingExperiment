import os
import pygame as pg
from screeninfo import get_monitors

# ============================================================================
# ============================================================================
# ============================================================================

# get window width and height (will handle dpi later?)
winfo = get_monitors()
winWidth = winfo[0].width
winHeight = winfo[0].height
FPS = 60

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

responseDuration = int(60 * 1000)  # time for the user to make a response

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

# == how far (in levels) player progresses or regresses based on performance ==
success = 1
failure = -3

# level the practice starts on
startingPracticeLevel = 3

# == Trial variables ==
timeOrTrialsDict = {

    # time that real trials last (in milliseconds)
    'real' : 120 * 1000,

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
restingStateTime = int(3 * 1000)

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