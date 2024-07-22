# run this file if you want to do offline data collection on the same computer you
# are running the experiment on. (Currently, this file includes a call to EEGTestOutlet)
# which is a mock EEG + DIN outlet device for testing purposes. If you are using
# the actual Netstation system, then comment out the lines relating to this.)
from threading import Thread
from main import main as startExperiment
from realtimeFunctions.offlineStorage import main as offlineStorage
from realtimeFunctions.EEGTestOutlet import main as testOutlet

def main():

    experimentDictionary = {'dataCollectionRunning': True}

    # create EEG mock outlet thread (comment out if using real EEG device)
    testOutletThread = Thread(target = testOutlet, args = [experimentDictionary]) 

    # create threads for offline storage and the experiment
    offlineStorageThread = Thread(target = offlineStorage, args = [])
    experimentThread = Thread(target = startExperiment, args = [])

    # start EEG mock outlet thread (comment out if using real EEG device)
    testOutletThread.start()

    # start offline storage and experiment threads
    offlineStorageThread.start()
    experimentThread.start()

    # wait for all threads to finish
    experimentThread.join()
    offlineStorageThread.join()
    experimentDictionary['dataCollectionRunning'] = False
    testOutletThread.join() # comment this line out if using real EEG device

if __name__ == '__main__':
    main()




