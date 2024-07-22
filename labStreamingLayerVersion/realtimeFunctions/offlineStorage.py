# File to save eeg data as an xdf file for offline analyses
import os
import mne
import numpy as np
from threading import Thread
from .generalFunctions import *
from pylsl import local_clock
from .dictionaries import *

# Create save folder if necessary and return file path
def getPaths(subjectNumber):

    # file paths for storing event data
    curDir = os.path.dirname(__file__)

    # folder where we save data to (may need to revise?)
    saveFolder = os.path.join(curDir, '..', 'results', 'subjectData', subjectNumber)

    # path to temp folder where we temporarily store data
    tempFolderPath = os.path.join(saveFolder, 'tempData')
    os.makedirs(tempFolderPath, exist_ok = True)

    # path to the save file
    savefilePath = os.path.join(saveFolder, f'{subjectNumber}_raw.fif')

    return savefilePath, tempFolderPath


# prompts the user to enter the subject number
def getSubjectNumber():

    # set of digits for valid chars in subject number
    digits = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

    while True:
        subjectNumber = input('\nEnter Subject Number: ').strip()
        if subjectNumber and all(char in digits for char in subjectNumber):
            return subjectNumber
        else:
            print('Invalid Subject Number. Please enter digits only.')


# extract info from the eeg inlet and creates an MNE info object for EEG and DIN channels
def getInfo(eegInlet):

    # get LSL eeg inlet info
    streamInfo = eegInlet.info()

    # number of channels (subtract one because last channel is the DIN)
    numberOfChannels = streamInfo.channel_count() - 1
    
    # sampling rate of eeg data outlet
    samplingRate = streamInfo.nominal_srate()

    # extract channels (need to get rid of DIN channel)
    channels = streamInfo.desc().child('channels').child('channel')

    # get channel names
    channelNames = []
    for _ in range(numberOfChannels):
        channelNames.append(channels.child_value('label'))
        channels = channels.next_sibling()
    
    # create MNE info object for eeg data, DIN data
    eegInfo = mne.create_info(ch_names = channelNames, sfreq = samplingRate, ch_types = 'eeg')
    dinInfo = mne.create_info(ch_names = ['DIN'], sfreq = samplingRate, ch_types = ['stim'])

    return eegInfo, dinInfo


# collects the eeg data and the events data and eeg data to temporary numpy files
# which we will later use to make one big fif file 
def collectEEGData(eegInlet, tempFolderPath, crossThreadReferenceDictionary):
    
    # initial temporary file name
    minute = 1
    tempFilename = os.path.join(tempFolderPath, f'minute_{minute}.npy')

    # want to find the timestamp of the first sample so we can subtract off for events
    firstSampleFound = False

    # data collection loop
    startTime = local_clock()
    dinData = [] # empty list to store din data (din data is stored as 129th entry in eeg data)
    tempEEGData = [] # empty list for temporary eeg data

    # collect an extra 5 seconds of eeg data after event collection is finished
    garbageTimeRemaining = 5
    garbageTimeBegun = False

    while crossThreadReferenceDictionary['eventCollectionRunning'] or garbageTimeRemaining > 0:
        
        try:
            
            # pull eeg chunk
            correction = eegInlet.time_correction()
            samples, uncorrectedTimestamps = eegInlet.pull_chunk()
            
            # if our chunk is non-empty
            if samples:

                # correct the timestamps
                timestamps = np.array(uncorrectedTimestamps) + correction

                # only collect eeg samples once event stream has been found
                if timestamps[0] < crossThreadReferenceDictionary['eventsStreamStartTime']:
                    continue

                # collect the timestamp of the first sample
                if not firstSampleFound:
                    crossThreadReferenceDictionary['firstSampleTimestamp'] = timestamps[0]
                    firstSampleFound = True

                # Seperate EEG and DIN data
                eegSamples = [sample[:-1] for sample in samples] # All but the last entry are EEG data
                dinSamples = [sample[-1] for sample in samples]  # The last entry is DIN data

                # extend the EEG data and DIN data with our new samples
                tempEEGData.extend(eegSamples.copy())
                dinData.extend(dinSamples.copy())

            
            # write a new temp file for each minute
            if (local_clock() - startTime) >= 60:

                # save the current temp array
                np.save(tempFilename, np.array(tempEEGData, dtype = np.float32))

                # update the file name
                minute += 1
                tempFilename = os.path.join(tempFolderPath, f'minute_{minute}.npy')

                # reset the start time
                startTime = local_clock()

                # empty the temp eeg data
                tempEEGData = []
            
            if not crossThreadReferenceDictionary['eventCollectionRunning']:
                if garbageTimeBegun:
                    garbageTimeRemaining = 5 - (local_clock() - garbageTimeStart)
                else:
                    startTime = local_clock()
                    garbageTimeBegun = True
                    garbageTimeStart = local_clock()

        except Exception as error:
            print(f'Error in EEG data collection loop: \n{error}')
            crossThreadReferenceDictionary['eventCollectionRunning'] = False
    
    print(f'garbage time elapsed: {local_clock() - garbageTimeStart}')
    
    # save the remaining data
    np.save(tempFilename, np.array(tempEEGData, dtype = np.float32))
    
    # save DIN data
    np.save(os.path.join(tempFolderPath, 'dinData.npy'), np.array(dinData, dtype = np.float32))

    # add dinData to cross thread reference dictionary (adding to dict is like having a return value)
    crossThreadReferenceDictionary['dinData'] = np.array(dinData, dtype = np.float32)

    return


# collects the events data and the events data and eeg data to temporary numpy files
# which we will later use to make one big fif file 
def collectEventsData(eventsInlet, crossThreadReferenceDictionary, tempFolderPath, samplingRate):

    # data collection loop
    eventsData = []
    while crossThreadReferenceDictionary['eventCollectionRunning']:

        try:

            # pull event sample
            correction = eventsInlet.time_correction()
            events, timestamp = eventsInlet.pull_sample()
            tag = events[0]
            timestamp += correction
        
            # append event to events list
            sampleIndex = round((timestamp - crossThreadReferenceDictionary['firstSampleTimestamp']) * samplingRate)
            eventsData.append((int(sampleIndex), int(0), int(tagToEventIdNumberDictionary[tag])))
            
            # print tag and event ID number
            print(f'Event: {tag}\nID Number: {tagToEventIdNumberDictionary[tag]}\nTimestamp: {timestamp - crossThreadReferenceDictionary['firstSampleTimestamp']}\nSample Index: {sampleIndex}\n\n')

            # once we get the end of the experiment, kill this thread and update the 
            # cross-thread reference dictionary to indicate to the eeg collection thread
            # that it should stop collecting data
            if tagToEventIdNumberDictionary[tag] == tagToEventIdNumberDictionary['endOfExperiment']:
                crossThreadReferenceDictionary['eventCollectionRunning'] = False

        except Exception as error:
            print(f'Error in event data collection loop: \n{error}')
            crossThreadReferenceDictionary['eventCollectionRunning'] = False
    
    # cast events data to a numpy array and then correct the timestamps
    eventsData = np.array(eventsData)

    np.save(os.path.join(tempFolderPath, 'eventsData.npy'), eventsData)
    crossThreadReferenceDictionary['eventsData'] = eventsData

    return


# takes the events data, the DIN data, and the temp files with EEG data and creates
# a fif file with all of the data for use in later MNE processing
def createFifFile(eventsData, dinData, tempFolderPath, savefilePath, eegInfo, dinInfo):
    
    # create a numpy object with all of the EEG data
    arrays = []
    for minute in range(1, len(os.listdir(tempFolderPath)) - 1): # subtract one bc we have din data and event data files

        # name of file
        tempFilePath = os.path.join(tempFolderPath, f'minute_{minute}.npy')

        # load temp file and append to overall data list ('arrays')
        curArray = np.load(tempFilePath)
        arrays.append(curArray)
    
    # since the data was saved in the form (n_samples, n_channels),
    # we transpose the data to get (n_channels, n_samples)
    eegData = np.concatenate(arrays)
    eegData = eegData.T

    # creates an MNE array with eeg data and info about the eeg machine
    rawObject = mne.io.RawArray(data = eegData, info = eegInfo)
    dinData = dinData.reshape(-1, 1).T
    dinRawObject = mne.io.RawArray(data = dinData, info = dinInfo)

    # append DIN data and Events data to the raw object with EEG data
    rawObject.add_channels([dinRawObject], force_update_info = True)
    rawObject.set_annotations(mne.annotations_from_events(events = eventsData, sfreq = eegInfo['sfreq'], event_desc = eventIdNumberToTagDictionary))

    # save the object
    rawObject.save(savefilePath, overwrite = True)

    return



def main():

    # initialize an inlet for the eeg data stream and extract sampling rate
    eegInlet, _, _ = initializeInlet(streamType = 'eeg')

    # initialize an inlet for the events stream
    eventsInlet, subjectNumber, eventsStreamStartTime = initializeInlet(streamType = 'Events')


    eegInfo, dinInfo = getInfo(eegInlet)
    
    # get the path to where we will save the event data
    savefilePath, tempFolderPath = getPaths(subjectNumber)

    # get sampling rate
    samplingRate = eegInfo['sfreq']

    # create a dictionary to store a boolean variable ('eventCollectionRunning').
    # For some reason (i don't know the reason), dictionaries are updated across
    # child threads. When the variable is flipped to False, the eeg collection stream
    # will know to stop collecting data. Similary, we use eventStreamStartTime to weed out
    # chunks received before the event stream was found. This dictionary will also contain the dinData 
    # and events data from these child processes. 
    crossThreadReferenceDictionary = {'eventCollectionRunning': True, 'eventsStreamStartTime': eventsStreamStartTime}


    # define a thread to collect data from the eeg streams and write to .npy files in temp folder (also collects DIN data)
    eegCollectionThread = Thread(target = collectEEGData, args = (eegInlet, tempFolderPath, crossThreadReferenceDictionary))

    # define a thread to collect event data
    eventsCollectionThread = Thread(target = collectEventsData, args = (eventsInlet, crossThreadReferenceDictionary, tempFolderPath, samplingRate))
    
    # start the data collection threads
    eegCollectionThread.start()
    eventsCollectionThread.start()

    # wait for all data to be collected before creating final file
    eventsCollectionThread.join()
    eegCollectionThread.join()

    # recover events data and DIN data
    eventsData = crossThreadReferenceDictionary['eventsData']
    dinData = crossThreadReferenceDictionary['dinData']

    # create a fif file with all of the data for mne processing
    createFifFile(eventsData, dinData, tempFolderPath, savefilePath, eegInfo, dinInfo)


if __name__ == '__main__':
    main()

