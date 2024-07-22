import os
import csv


# creates an aggregate trial by trial file in the results folder
def createAggregateFile(filename):
    
    # path where we load files from (results/subjectData)
    curDir = os.path.dirname(__file__)
    loadPath = os.path.join(curDir, '..', 'results', 'subjectData')

    # store all of the subject folders in the directory as a list
    subjectDataFolders = [fileOrFolder for fileOrFolder in os.listdir(loadPath) if os.path.isdir(os.path.join(loadPath, fileOrFolder))]

    # collect the data from each TrialByTrialData file
    aggregateData = []
    for subjectDataFolder in subjectDataFolders:

        # path to TrialByTrialData csv file (potentially) in each subject folder
        filePath = os.path.join(loadPath, subjectDataFolder, filename)

        try:
            with open(filePath, mode = 'r', newline = '') as f:

                try:
                    # initialize a csv reader
                    reader = csv.reader(f)

                    # store the data as a list (exclude the header)
                    lines = list(reader)[1:]
                    
                    # add this file's lines to the aggregate data list
                    aggregateData.extend(lines)

                # handle empty files
                except:
                    pass

        # handle empty folders
        except:
            pass

    
    # save path for the aggregate data (results folder)
    aggregateDataSavePath = os.path.join(curDir, '..', 'results', filename)

    # prepare the header
    if filename == 'TrialByTrialData.csv':
        header = ['Subject Number', 'Name', 'Trial Number', 'Level', 'Response Time',
                'Total Time Since Start of Real Trials', 'Number of Targets Identified', 'Number of Targets', 
                'Number of Distractors', 'D-Prime', 'Timeup']
    else:
        header = ['Subject Number', 'Name', 'D-Prime Mean', 'D-Prime Standard Deviation', 'Highest Level', 'Final Level', 'Score']

    # write the data to a csv in results
    with open(aggregateDataSavePath, mode = 'w', newline = '') as f:

        # initialize a csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write data
        for line in aggregateData:
            writer.writerow(line)
    
    return

def main():

    # create aggregate data file for trial by trial data
    createAggregateFile('TrialByTrialData.csv')

    # create aggregate data file for 
    createAggregateFile('summaryData.csv')


if __name__ == '__main__':
    main()
