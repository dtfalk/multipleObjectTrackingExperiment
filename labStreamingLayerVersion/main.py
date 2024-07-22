# lab streaming layer version of the MOT task
# written by David Tobias Falk, APEX Lab at the University of Chicago
# TODO: make single object tracking easy?
# TODO: check for existence of subject number and reprompt user?
from helpers.constants import *
from helpers.classes import *
from helpers.dataStorage import *
from helpers.drawing import *
from helpers.gameInfo import *
from helpers.getUserInfo import *
from helpers.messageScreens import *
from helpers.statistics import *
from helpers.gameOptions import *
from helpers.LSLHelpers import *
import pygame as pg

# end times of each phase
fixationEnd = fixationDuration
highlightEnd = fixationDuration + highlightDuration
movementEnd = fixationDuration + highlightDuration + movementDuration
selectionEnd = fixationDuration + highlightDuration + movementDuration + selectionDuration

# == Runs trials ==
def trials(gametype, startingLevel, subjectNumber, name, win, eventsOutlet, clock):
    
    # == Generates the game ==
    # use the selected starting level for the real trials
    if gametype == 'real':
        game = initializeGame(startingLevel, gametype)
    
    # use the practice starting level (defined in constants.py) for the practice trials
    elif gametype == 'practice':
        game = initializeGame(startingPracticeLevel, gametype)
    
    # use level 1 for the guide trials
    else:
        game = initializeGame(1, gametype)


    targets, distractors = generateBalls(game)

    timeOrTrialsCompleted = 0
    trialsCount = 0

    # variables for insufficient selections, taking too long to respond, 
    # if the user has submitted an answer, and if we need to reset for a new trial
    reset = False
    submitted = False
    incorrectNumberOfSelections = False
    timeup = False
    clickCountdown = 0

    # tag push variables
    fixationTagPushed = False
    fixationTagFlipped = False

    highlightTagPushed = False
    highlightTagFlipped = False
    
    movementTagPushed = False
    movementTagFlipped = False

    selectionTagPushed = False
    selectionTagFlipped = False

    # initially show that we are starting level for the real trials
    if gametype == 'real':
        args = [game['level']]
        messageScreen('levelScreen', args, eventsOutlet, win)
    
    # variables to store how long the experiment has been running for
    startTime = pg.time.get_ticks()
    totalTime = 0

    # variable to store how long a particular trial has been running for
    trialStartTime = pg.time.get_ticks()

    # variable to track if we have given the user their break yet
    breakGiven = False

    # == Controls the "game" part of the game ==
    while True:

        # draw background and boundaries
        win.fill(backgroundColor) 
        drawBoundaries(win)

        # get the x and y coordinates of the mouse
        mouseX, mouseY = pg.mouse.get_pos() 


        # Grabs the time after each frame and total time passed in the trial and in the entire run
        curTime = pg.time.get_ticks()
        timeElapsedSinceStartOfTrial = curTime - trialStartTime # in milliseconds
        totalTime = curTime - startTime # in milliseconds

        # if the user still has trials/time to complete in the experiment
        if timeOrTrialsCompleted < timeOrTrialsDict[gametype]:
            
            # main event loop to iterate over each event in the event queue
            for event in pg.event.get():

                # handles keypresses
                if event.type == pg.KEYDOWN:

                    # if the user presses escape (the quit key), then we quit the game
                    if event.key == generalQuitKey:
                        blankSquareScreen('endOfExperiment', eventsOutlet, win)
                        pg.quit()
                        sys.exit()
                    
                    # if the user presses the skip key (meant for devs only), then it skips
                    # the current stage
                    if event.key == skipKey:
                        return game
                    # if the user presses space bar during the selection phase...
                    if event.key == submitAnswerKey and (movementEnd < timeElapsedSinceStartOfTrial <= selectionEnd):

                        selectedBalls = [] # list for all selected balls
                        selectedTargets = [] # list for all selected targets

                        # iterate over each ball
                        for ball in targets + distractors:

                            # add all selected balls to the list of selected balls
                            if ball.isSelected:
                                selectedBalls.append(ball)

                                # add selected targets to list of selected targets
                                if ball in targets:
                                    selectedTargets.append(ball)
                            
                        # if the user has selected the correct number of balls, then we set submitted to True
                        if len(selectedBalls) == len(targets):
                            submitted = True

                            # draw the true time square
                            if gametype == 'real':
                                drawSquare(win)
                                sendTag('selectionSubmitted', eventsOutlet)
                                pg.display.flip()
                                pg.time.delay(squareDuration)
                            
                        # otherwise we set the insufficient selections variable to true
                        else:
                            incorrectNumberOfSelections = True
                            insufficientSelectionTime = pg.time.get_ticks() 
                
                # handles mouse behavior
                for ball in targets + distractors:
                    
                    if ball.inCircle(mouseX, mouseY):

                        # if the user releases a click over a ball, then...
                        if event.type == pg.MOUSEBUTTONUP:

                            # if the ball is not already selected, then we color it selected
                            if not ball.isSelected:

                                # no clicking more than once per squareDuration
                                if clickCountdown <= 0:
                                    ball.stateControl("selected")

                                    # variables to reference to show square for a click
                                    clickCountdown = squareDuration
                                    clickTime = pg.time.get_ticks()
                                    clickType = 'select'
                                    clickTagSent = False
                            
                            # if the ball is already selected, then we color it unselected
                            else: 

                                # no unclicking more than once per squareDuration
                                if clickCountdown <= 0:                               
                                    ball.stateControl("neutral")

                                    # variables to reference to show square for a click
                                    clickCountdown = squareDuration
                                    clickTime = pg.time.get_ticks()
                                    clickType = 'unselect'
                                    clickTagSent = False
                    
                        # if the mouse is hovering over the ball and the ball is not selected, then we apply the hover color
                        elif event.type == pg.MOUSEMOTION:
                            if not ball.isSelected:
                                ball.stateControl("hovered")
                    
                    # if the cursor is not in the ball's radius
                    else: 

                        # if the ball is not selected, then color it white
                        if not ball.isSelected:
                            ball.stateControl("neutral")


            # handle game by phase
            if not reset:

                # handling the fixation phase
                if timeElapsedSinceStartOfTrial <= fixationEnd:
                    
                    # flip this variable to true to indicate that we 
                    # should push the tag right before (or after... needs testing) the screen flip
                    if not fixationTagFlipped:
                        fixationTagFlipped = True

                    # draw the true time square
                    if timeElapsedSinceStartOfTrial <= squareDuration and gametype == 'real':
                        drawSquare(win)
                    
                    # hide mouse in this phase
                    pg.mouse.set_visible(False)

                    # ensure hovering does not change color
                    for ball in targets + distractors: 
                        ball.color = defaultColor
                    
                    # draw the fixation cross and the balls
                    fixationScreen(targets, distractors, win)

                # handling the highlighting balls phase
                elif fixationEnd < timeElapsedSinceStartOfTrial <= highlightEnd:

                    # flip this variable to true to indicate that we 
                    # should push the tag right before (or after... needs testing) the screen flip
                    if not highlightTagFlipped:
                        highlightTagFlipped = True

                    # draw the true time square
                    if timeElapsedSinceStartOfTrial <= fixationEnd + squareDuration and gametype == 'real':
                        drawSquare(win)
                    
                    # hide mouse in this phase
                    pg.mouse.set_visible(False)

                    # highlight the targets
                    for target in targets:
                        target.color = clickColor
                    
                    # ensure hovering does not highlight the distractors
                    for distractor in distractors:
                        distractor.color = defaultColor
                    
                    # draw the balls
                    drawStaticBalls(targets, distractors, win)
                
                # handling the ball movement phase
                elif highlightEnd < timeElapsedSinceStartOfTrial <= movementEnd:

                    # flip this variable to true to indicate that we 
                    # should push the tag right before (or after... needs testing) the screen flip
                    if not movementTagFlipped:
                        movementTagFlipped = True

                    # draw the true time square
                    if timeElapsedSinceStartOfTrial <= highlightEnd + squareDuration and gametype == 'real':
                        drawSquare(win)

                    # hide mouse in this phase
                    pg.mouse.set_visible(False)

                    # hovering does not change color
                    for ball in targets + distractors:
                        ball.color = defaultColor
                    
                    # draw the balls in motion
                    drawMovingBalls(targets, distractors, win)

                    # keep mouse centered so it will be centered when selection phase begins
                    pg.mouse.set_pos(winWidth // 2, winHeight // 2)
                
                # handling the response/selection phase
                elif movementEnd < timeElapsedSinceStartOfTrial <= selectionEnd:

                    # flip this variable to true to indicate that we 
                    # should push the tag right before (or after... needs testing) the screen flip
                    if not selectionTagFlipped:
                        selectionTagFlipped = True

                    # draw the true time square
                    if timeElapsedSinceStartOfTrial <= movementEnd + squareDuration and gametype == 'real':
                        drawSquare(win)

                    # draw square if a ball has been clicked recently ("recently" with resepect to "squareDuration")
                    if clickCountdown > 0:
                        
                        if gametype == 'real':
                            drawSquare(win)

                        # send the tag for the click if it hasn't been sent yet
                        if not clickTagSent and gametype == 'real':
                            if clickType == 'select':
                                sendTag('ballSelected', eventsOutlet)
                            else:
                                sendTag('ballUnselected', eventsOutlet)
                            clickTagSent = True
                        
                        # decrement the countdown
                        clickCountdown = squareDuration - (pg.time.get_ticks() - clickTime)
                    
                    # make the mouse visible again so the user can make selections
                    pg.mouse.set_visible(True)
                    
                    # draw the balls
                    drawStaticBalls(targets, distractors, win)

                    if incorrectNumberOfSelections:

                        # display the insufficient selections text
                        args = [len(targets)]
                        messageScreen("incorrectNumberOfSelectionsScreen", args, eventsOutlet, win)

                        # remove the message after half of a second
                        if pg.time.get_ticks() - insufficientSelectionTime > 500:
                            incorrectNumberOfSelections = False
                    
                # handle taking too long to answer
                else:

                    # draw true time square and delay for a tenth of a second
                    if gametype == 'real':
                        drawSquare(win)
                        sendTag('timeup', eventsOutlet)
                        pg.display.flip()
                        pg.time.delay(squareDuration)

                    pg.mouse.set_visible(False)
                    timeup = True

            # handles what happens after the user submits their selections
            if submitted:

                # hide mouse
                pg.mouse.set_visible(False)
                
                # == message screen stating performance on that trial ==

                # if the user identified all of the targets, then display the correct screen
                if gametype == 'real':
                    sendTag(f'{len(selectedTargets)} out of {len(targets)} targets identified with {len(distractors)} distractors', eventsOutlet)
                if len(selectedTargets) == len(targets):
                    args = [len(targets)]
                    messageScreen('correctScreen', args, eventsOutlet, win)
                
                # otherwise display the incorrect screen
                else:
                    args = [len(selectedTargets), len(targets)]
                    messageScreen('incorrectScreen', args, eventsOutlet, win)
                
                # == Records info for the trial ==

                # calculate dprime for the trial
                dprime = dPrime(len(selectedTargets), game)

                # calculate how long it took the user to make their submission
                submissionTime = (timeElapsedSinceStartOfTrial - (fixationDuration + highlightDuration + movementDuration)) / 1000
                
                # increment number of trials completed by 1
                trialsCount += 1

                # record user selection if in the real trials
                if gametype == 'real':
                    recordTrialData(trialsCount, subjectNumber, name, submissionTime, totalTime / 1000, game, len(selectedTargets), dprime, False)

                # Based on the user's performance, we update the game and return a new list of targets and distractors
                game, targets, distractors = updateGame(game, len(selectedTargets))

                # increment the amount of trials or time completed
                # (we don't count rounds where the user didn't answer towards play time)
                if gametype == 'real':
                    timeOrTrialsCompleted = totalTime
                else:
                    timeOrTrialsCompleted += 1
                
                # set trial reset variable to true so we begin the resetting process
                reset = True

            # handles the case when the user takes too long to respond
            if timeup: 

                # keep mouse invisible
                pg.mouse.set_visible(False)

                # incrememnt number of trials completed by 1
                trialsCount += 1

                # record the timeup
                if gametype == 'real':
                    recordTrialData(trialsCount, subjectNumber, name, "timed out", totalTime / 1000, game, "NA", "NA", True)
                
                # show timeup message screen
                args = []
                messageScreen("timeupScreen", args, eventsOutlet, win)

                # set the reset variable to true 
                # (don't need to update the game because the user will be given the same level)
                reset = True

            # prepare for the next trial (note that the game has already been updated)
            if reset: 

                # keep mouse invisible
                pg.mouse.set_visible(False)

                # gives user break after certain amount of time in real trials
                if gametype == 'real' and breakScreenEnabled:

                    # give user a break halfway through the real trials
                    if totalTime > (timeOrTrialsDict[gametype] // 2) and not breakGiven:

                        # note the start time of the break
                        breakStart = pg.time.get_ticks()

                        # display break screen
                        pg.event.clear()
                        args = []
                        sendTag('breakStart', eventsOutlet)
                        messageScreen('breakScreen', args, eventsOutlet, win)
                        sendTag('breakEnd', eventsOutlet)

                        # subtract the total break time from the total time played
                        # don't want user taking a 10 minute break and having that cut into their play time
                        breakLength = pg.time.get_ticks() - breakStart
                        totalTime -= breakLength

                        # set break given variable to true so the user only gets one break
                        breakGiven = True
                
                # reset variables tracking user behavior in the trials
                submitted = False
                timeup = False
                incorrectNumberOfSelections = False
                reset = False

                # reset tag push variables
                fixationTagPushed = False
                fixationTagFlipped = False

                highlightTagPushed = False
                highlightTagFlipped = False

                movementTagPushed = False
                movementTagFlipped = False

                selectionTagPushed = False
                selectionTagFlipped = False
                
                # if gametype is real, the show level and score
                if gametype == 'real':

                    # display the user's current score if score showing is enabled
                    if scoreEnabled:
                        args = [game['score']]
                        messageScreen('scoreScreen', args, eventsOutlet, win)

                    # display level the user is on if there is another level to play
                    if totalTime < timeOrTrialsDict[gametype]:
                        args = [game['level']]
                        messageScreen('levelScreen', args, eventsOutlet, win)

                # reset the trial start time
                trialStartTime = pg.time.get_ticks()

        # handles the end of experiment/practice/guide (if not timeOrTrialsCompleted < timeOrTrials) 
        else:
            
            # make mouse invisible
            pg.mouse.set_visible(False)

            # return the game with its info about user performance
            # e.g. highest level achieved, score, etc...
            return game

        totalTime = pg.time.get_ticks() - startTime

        # == phase start tag sending logic ==
        if gametype == 'real':
            if fixationTagFlipped and not fixationTagPushed:
                # start of fixation phase and current level
                sendTag(f'level {game['level']}', eventsOutlet)
                sendTag('fixationStart', eventsOutlet)
                fixationTagPushed = True
            elif highlightTagFlipped and not highlightTagPushed:
                # start of highlight phase
                sendTag('highlightStart', eventsOutlet)
                highlightTagPushed = True
            elif movementTagFlipped and not movementTagPushed:
                # start of movement phase
                sendTag('movementStart', eventsOutlet)
                movementTagPushed = True
            elif selectionTagFlipped and not selectionTagPushed:
                # start of selection phase
                sendTag('selectionStart', eventsOutlet)
                selectionTagPushed = True

        pg.display.flip()
        clock.tick(FPS)

# Main Loop
def main():
        
# =========================================================================================================================

    # == Initiate pygame and collect user information ==
    pg.init()
    pg.mixer.init()

    # == Set window ==
    win = pg.display.set_mode((winWidth, winHeight), pg.FULLSCREEN)

    # initialize a pygame clock to control the frame rate
    clock = pg.time.Clock()

    # make mouse invisible
    pg.mouse.set_visible(False)

# =========================================================================================================================

    # == Collecting user info ==

    # get user's name
    name = getUserInfo('name', win)

    # get user's subject number
    subjectNumber = getUserInfo('subject number', win)

    # == Initialize event stream outlet ==
    eventsOutlet = initializeEventsOutlet(subjectNumber)

    # level the user starts on
    startingLevel = 1
    if levelSelectEnabled:
        startingLevel = int(getUserInfo('starting level (1 - 99)', win))
    
    # draw screen to inform user about LSL preparation
    args = []
    messageScreen('LSLPrepScreen', args, eventsOutlet, win)

# =========================================================================================================================

    # == Pre-trials resting state screens ==

    # show users the eyes open resting state instructions and screen
    if eyesOpenPreRestScreenEnabled:
        pg.event.clear()
        args = []
        messageScreen('eyesOpenScreen', args, eventsOutlet, win)
        drawEyesOpenScreen(win, eventsOutlet = eventsOutlet)
        pg.event.clear()


    # show users the eyes closed resting state instructions and screen
    if eyesClosedPreRestScreenEnabled:
        args = []
        messageScreen('eyesClosedScreen', args, eventsOutlet, win)
        drawEyesClosedScreen(win, eventsOutlet = eventsOutlet)
        pg.event.clear()

# =========================================================================================================================

    # == Guide trials ==
    if guideTrialsEnabled:

        # show guide screen text
        args = [startingTargets, startingTargets + startingDistractors]
        messageScreen('guideStartScreen', args, eventsOutlet, win)
        pg.event.clear()

        # start guide trials
        trials(gametype = 'guide', startingLevel = startingLevel, subjectNumber = subjectNumber, name = name, win = win, eventsOutlet = eventsOutlet, clock = clock)
        pg.event.clear()


    # == Practice trials ==
    if practiceTrialsEnabled:

        # show practice screen text
        args = []
        messageScreen('practiceStartScreen', args, eventsOutlet, win)
        pg.event.clear()

        # start practice trials
        trials(gametype = 'practice', startingLevel = startingLevel, subjectNumber = subjectNumber, name = name, win = win, eventsOutlet = eventsOutlet, clock = clock)
        pg.event.clear()


    # == Real trials ==

    # show real trials text
    args = []
    messageScreen('realTrialsStartScreen', args, eventsOutlet, win)
    pg.event.clear()

    # quick square and tag to indicate start of real trials
    blankSquareScreen('startOfRealTrials', eventsOutlet, win)
    pg.event.clear()

    # begin real trials
    game = trials(gametype = 'real', startingLevel = startingLevel, subjectNumber = subjectNumber, name = name, win = win, eventsOutlet = eventsOutlet, clock = clock)
    pg.event.clear()

    # draw a square and send a tag to indicate end of real trials
    blankSquareScreen('endOfRealTrials', eventsOutlet, win)
    pg.event.clear()


# =========================================================================================================================

    # == Post-trials resting state screens ==

    # show users the eyes open resting state instructions and screen
    if eyesOpenPostRestScreenEnabled:
        args = []
        messageScreen('eyesOpenScreen', args, eventsOutlet, win)
        drawEyesOpenScreen(win, eventsOutlet = eventsOutlet)
        pg.event.clear()

    # show users the eyes closed resting state instructions and screen
    if eyesClosedPostRestScreenEnabled:
        args = []
        messageScreen('eyesClosedScreen', args, eventsOutlet, win)
        drawEyesClosedScreen(win, eventsOutlet = eventsOutlet)
    
    # draw end of experiment screen
    blankSquareScreen('endOfExperiment', eventsOutlet, win)

# =========================================================================================================================

    if scoreEnabled:

        # display user's score
        args = [game['score']]
        messageScreen('finalScoreScreen', args, eventsOutlet, win)

        #  == High scores ==
        # (assuming this functionality is activated)
        score = game['score']
        if highscoresEnabled:

            # retrieve highscore data and see if user made the top 5
            highscores = getHighScoreData()
            rank = checkIfHighScore(game['score'], highscores)

            # if the user made the highscore list, then inform them and update the highscores list
            if rank != -1:
                args = [rank]
                messageScreen('newHighscoreScreen', args, eventsOutlet, win)
                highscores = addHighScore(score)
        
            # display highscores
            args = [highscores]
            messageScreen('highscoresScreen', args, eventsOutlet, win)
            pg.event.clear()

# =========================================================================================================================
    
    # display exit message 
    args = []
    messageScreen('experimentFinishedScreen', args, eventsOutlet, win)

    # create summary csv for the user
    summaryData(subjectNumber, name, game['score'])


    return

if __name__ == "__main__":
    main()