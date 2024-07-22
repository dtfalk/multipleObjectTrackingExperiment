import os
import csv
import pandas as pd

# function to get save path for user
def getResultsPath(subjectNumber):

    # path for this file's directory
    curDir = os.path.dirname(__file__)

    # path for results directory, where we will store user info
    resultsDir = os.path.join(curDir, '..', 'results', 'subjectData')

    # create results directory if necessary
    os.makedirs(resultsDir, exist_ok = True)

    # create path to folder where we will write subject's data to 
    subjectResultsFolderPath = os.path.join(resultsDir, f'{subjectNumber}')

    # create folder to store trial by trial and aggregate data
    os.makedirs(subjectResultsFolderPath, exist_ok = True)

    # create path to file where we will write subject's data to 
    subjectResultsFilePath = os.path.join(subjectResultsFolderPath, 'TrialByTrialData.csv')

    return subjectResultsFilePath, subjectResultsFolderPath


# function to get existing high score information
def getHighScoreData():

    # path for this file's directory
    curDir = os.path.dirname(__file__)

    # path for results directory, where we will store user info
    resultsDir = os.path.join(curDir, '..', 'results')

    # path to highscore data
    highscoreDataPath = os.path.join(resultsDir, 'highscoreData.csv')
    os.makedirs(os.path.dirname(highscoreDataPath), exist_ok = True)

    # if the file doesn't exist, then create an empty file with a header and 5 entries of 0
    if not os.path.exists(highscoreDataPath):
        with open(highscoreDataPath, mode = 'w', newline = '') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(['highscores'])

            # write five lines of zeros
            for i in range(5):
                writer.writerow(['0'])

        return [0] * 5
    
    # otherwise, read the data from the file
    else:
        # we will assume that the high score data is sorted 
        with open(highscoreDataPath, mode = 'r', newline = '') as f:

            # create a csv reader and list the lines
            reader = csv.reader(f)
            lines = list(reader)

            # separate out headerm leaving just the data (only keep top 5 scores in file)
            # if fewer than five scores present, take the existing amount of scores
            highscoresStrings = lines[1:]
        
        # cast list of strings to list of integers
        highscores = [int(x[0]) for x in highscoresStrings]

        return highscores

# checks if the user's score makes the highscore list
def checkIfHighScore(score, highscores):

    # initialize their rank to -1. If not a highscore, then -1 will be returned
    rank = -1

    # assume highscores is sorted
    for i, highscore in enumerate(highscores):
        if score > highscore:
            rank = i + 1
            break

    return rank

# write to the high score data file
def addHighScore(score):

    # path for this file's directory
    curDir = os.path.dirname(__file__)

    # path for results directory, where we will store user info
    resultsDir = os.path.join(curDir, '..', 'results')

    # path to highscore data
    highscoreDataPath = os.path.join(resultsDir, 'highscoreData.csv')

    # we will assume that the high score data is sorted 
    with open(highscoreDataPath, mode = 'r', newline = '') as f:

        # create a csv reader and list the lines
        reader = csv.reader(f)
        lines = list(reader)

        # separate out header, leaving just the data (only keep top 5 scores in file).
        # If fewer than five scores present, take the existing amount of scores
        highscoresStrings = lines[1:]

    # cast the highscores from strings to integers and add new score
    highscores = [int(x[0]) for x in highscoresStrings]
    highscores.append(score)

    # sort in descending order and keep top 5
    highscores.sort(reverse = True)
    highscores = highscores[:5]

    # write the new high scores
    with open(highscoreDataPath, mode = 'w', newline = '') as f:

        # initialize a csv writer
        writer = csv.writer(f)

        # create and write the header
        header = ['high scores']
        writer.writerow(header)

        # write the highscores to the file
        for highscore in highscores:
            writer.writerow([str(highscore)])
    
    return highscores

# records the user's performance on a trial by writing a line to their TrialByTrial CSV file
def recordTrialData(trialsCount, subjectNumber, name, submissionTime, totalTimeElapsed, game, numberOfTargetsIdentified, dprime, timeup):
    
    # get the save paths
    subjectResultsFilePath, _ = getResultsPath(subjectNumber)

    # prepare the header
    header = ['Subject Number', 'Name', 'Trial Number', 'Level', 'Response Time',
            'Total Time Since Start of Real Trials', 'Number of Targets Identified', 'Number of Targets', 
            'Number of Distractors', 'D-Prime', 'Timeup']
    
    # prepare the data
    data = [str(subjectNumber), str(name), str(trialsCount), str(game['level']),
            str(submissionTime), str(totalTimeElapsed), str(numberOfTargetsIdentified),
            str(game['targets']), str(game['distractors']), str(dprime), str(timeup)]

    # if the file does not exist yet, then...
    if not os.path.exists(subjectResultsFilePath):

        # write header and data to file
        with open(subjectResultsFilePath, mode = 'w', newline = '') as f:

            # initialize a csv writer
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write the data
            writer.writerow(data)
    
    # if the file already exists, then...
    else:

        # write the data to the file
        with open(subjectResultsFilePath, mode = 'a', newline = '') as f:
            
            # initialize a csv writer
            writer = csv.writer(f)

            # write the data
            writer.writerow(data)
    
    return

# function to create a summary data file for each user
def summaryData(subjectNumber, name, score):

    # get path to trial by trial data
    subjectResultsFilePath, subjectResultsFolderPath = getResultsPath(subjectNumber)

    # get save path of the summary file
    summaryDataSavePath = os.path.join(subjectResultsFolderPath, 'summaryData.csv')

    # read the lines from the trial by trial data
    trialByTrialData = pd.read_csv(subjectResultsFilePath)

    # get the dprime data and find the mean/standard deviation
    dprimeData = trialByTrialData['D-Prime']
    dprimeMean = dprimeData.mean()
    dprimeSTD = dprimeData.std()

    # get the level data and find the highest level attained and the final level attained
    levelData = trialByTrialData['Level']
    highestLevel = levelData.max()
    finalLevel = levelData.iloc[-1]

    # prepare the header
    header = ['Subject Number', 'Name', 'D-Prime Mean', 'D-Prime Standard Deviation', 'Highest Level', 'Final Level', 'Score']

    # prepare the data
    data = [str(subjectNumber), str(name), str(dprimeMean), str(dprimeSTD), str(highestLevel), str(finalLevel), str(score)]

    # write the header and data to the summary file
    with open(summaryDataSavePath, mode = 'w', newline = '') as f:

        # initialize a csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(data)
    
    return
    

