from pylsl import StreamInfo, StreamInlet, StreamOutlet, resolve_stream
import numpy as np
from .generalFunctions import initializeInlet
from .dictionaries import tagToEventIdNumberDictionary, eventIdNumberToTagDictionary

num_samples = 0 # change to however many samples we want

din_off_value = 65535 # din value when the light sensor is off

# sets up our prediction outlet and EEG/DIN and events inlets
def setupStreams():

    # set up our outlet (will ultimately return either a 0 or a 1 to MOT Task computer)
    outletInfo = StreamInfo('predictionStream', 'predictions', 1, 0, 'string')
    predictionOutlet = StreamOutlet(outletInfo) 

    # get our eeg stream
    eegInlet, _, _ = initializeInlet(streamType = 'eeg')

    # get our events stream
    eventsInlet, subjectNumber, _ = initializeInlet(streamType = 'Events')
    
    return predictionOutlet, eegInlet, eventsInlet, subjectNumber


# pull data from when we find the flash tag to roughly before flash ends
def pullData(event_inlet, eeg_inlet):
    
    # Store the level
    while True:
        tag, = event_inlet.pull_sample()

        # Extract the level of the trial
        if tagToEventIdNumberDictionary[tag[0]] < 100:
            return tag[0]
    
    # wait until we find the highlight start tag to speed up later searches
    while True:
        tag, = event_inlet.pull_sample()

        # break once we find the beginning of the highlight phase
        if tag[0] == 'highlightStart':
            break
    
    # collect data for fixed number of samples
    length = 0
    prev_din_value = din_off_value 
    din_found = False
    eeg_data = np.array([])
    while True:
        # Separate into eeg and din samples
        samples_old, = eeg_inlet.pull_chunk()
        samples = np.array(samples_old)
        eeg_samples = samples[:, :-1]
        din_samples = samples[:, -1]

        # find our flash din and then start collecting data until
        # a predetermined number of samples is collected
        for din_sample, eeg_sample in zip(din_samples, eeg_samples):

            # don't start storing eeg data until we find the associated DIN
            # rests on the assumption that tags come before DINs
            # But all testing thus far shows this assumption holds
            cur_din_value = din_sample

            # Find first instance in the change of din values
            if not din_found:
                if prev_din_value == din_off_value and cur_din_value != din_off_value:
                    din_found = True
                if not din_found:
                    prev_din_value = cur_din_value
                    continue

            # keep adding eeg data until we hit the desired length then break
            # out of this for-loop
            # use a length variable as an int bc i think that will be quicker
            # than calculating the list length each time
            eeg_data.append(eeg_sample)
            length += 1

        # once we hit the desired length then break
        # out of this while-loop
        if length == num_samples:
            break
    
    return eeg_data, level

            
# waits to find the start of the real trials before we begin recording
def findStart(eventsInlet):
    while True:
        tag, _ = eventsInlet.pull_sample()
        if tagToEventIdNumberDictionary[tag[0]] == 'startOfRealTrials':
            return

# make a prediction and return either 0 or 1
def predict(eegData):

    # insert your prediction code below
    prediction = 0
    return prediction

# get the result of the trial
def getResult(eventsInlet):
    while True:
        event, = eventsInlet.pull_sample()
        tag = event[0]
    
        if tag[1] == tag[2]: # handles correct trials (this is goofy)
            return '1'
        else: # handles incorrect trials (0 for incorrect)
            return '0'

# performs the mid-trial clustering
def cluster(overallArray):
    # your clustering code here
    cluster = 0
    return cluster

if __name__ == '__main__':
    eegArray = np.array([], dtype = 'float64')
    resultArray = np.array([], dtype = 'int8')
    levelTrialArray = np.array([], dtype = 'object')

    # setup our inlets (EEG/DIN and Events) and our prediction outlets
    predictionOutlet, eegInlet, eventsInlet, subjectNumber = setupStreams()

    # wait to find the start of real trials
    findStart(eventsInlet)

    # repeat this process of finding the relevant data, trimming that data,
    # and then predicting based on that data
    trial = 1
    while True:
        # collect data
        eeg_data, level = pullData(eventsInlet, eegInlet)

        # make prediction
        prediction = predict(eeg_data)

        # push to MOT task
        predictionOutlet.push_sample([str(prediction)])
        
        # grab the result of the trial
        result = getResult(eventsInlet)

        # append the data, the trial, the level to their respective arrays
        np.append(eegArray, eeg_data)
        np.append(resultArray, result)
        np.append(levelTrialArray, (trial, level))

        # cluster based on the existing data that we have
        clustering = cluster(np.array(eegArray, resultArray, levelTrialArray))

        # each iteration of this loop represents one trial, so increment the trial variable
        # at the end of the loop
        trial += 1