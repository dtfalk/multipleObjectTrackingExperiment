from math import floor
from .constants import startingDistractors, startingTargets, success, failure, distractorsOverflow, speedOverflow
from .classes import Ball, getValidPositions

# initializes a game dictionary
def initializeGame(level, gametype):
    game = {
        "level": level,
        "distractors": startingDistractors,
        "speed" : 1,
        "targets": startingTargets,
        "score": 0,
        "consecutive": 0,
        "highestLevel": 1,
        "gametype": gametype
    }
    
    return getAttributes(game)

# Function for updating a game based on the level
def updateGame(game, numberOfSelectedTargets):
    
    # if the user correctly identified all targets then they progress
    if numberOfSelectedTargets == game["targets"]:
        game["level"] += success
        game["consecutive"] += 1
        game["score"] = updateScore(game)

        # update highscore if necessary
        if game['level'] > game['highestLevel']:
            game['highestLevel'] = game['level']

    # otherwise, they failed and we decrement the level
    else:
        game["level"] += failure
        game["consecutive"] = floor(game["consecutive"] / 2)

        # level 1 is the lowest level
        if game["level"] < 1:
            game["level"] = 1

    # get the values for targets, distractors, and speed
    game = getAttributes(game)

    # get the targets and distractors
    targets, distractors = generateBalls(game)

    return game, targets, distractors

# Function to create our targets and distractors for a game
def generateBalls(game):
    
    # create the targets
    targets = []
    numberOfTargets = game["targets"]
    for i in range(numberOfTargets):
        targets.append(Ball(game))

    # create the distractors
    distractors = []
    numberOfDistractors = game["distractors"] 
    for i in range(numberOfDistractors):
        distractors.append(Ball(game))

    # give each ball a valid position
    getValidPositions(targets, distractors)

    return targets, distractors

# Function to update the score given current score and consecutive correct trials
# TODO: make a score function that actually makes sense and has had some thought put into it
def updateScore(game):
    return game["score"] + game["consecutive"] + floor(game["level"] // 2)

# generates the num targets, num distractors and speed based on a game
def getAttributes(game):

    # iterate over the attributes to get the number of targets and number of distractors
    # what we are doing here is kind of cheeky... keep modulo arithmetic in mind...
    # TODO: explain this better 

    # targets have no limit but start at "startingTargets"
    game["targets"] = ((game["level"] - 1) // (distractorsOverflow * speedOverflow)) + startingTargets 

    # speed will be either 1, 2, or 3
    game["speed"] = (((game["level"] - 1)  // distractorsOverflow) % speedOverflow) + 1

    # distractors will be targets + 0, targets + 1, or targets + 2
    game["distractors"] = game["targets"] + ((game["level"] - 1) % 3)

    return game