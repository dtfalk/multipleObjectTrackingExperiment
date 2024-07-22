from pylsl import StreamOutlet, StreamInfo, local_clock
from time import sleep

def main(experimentDictionary):

    # initialize EEG outlet stream
    eegOutletInfo = StreamInfo(name = 'testEEGStream', type = 'eeg', channel_count = 129, channel_format = 'float32', nominal_srate = 1000, source_id = 'Mock_EEG_Outlet')
    
    # Add a description to the StreamInfo object
    desc = eegOutletInfo.desc()

    # Add channel information
    channels = desc.append_child("channels")
    for i in range(1, 129):  # Adding 128 EEG channels, you can customize this based on your channel setup
        ch = channels.append_child("channel")
        ch.append_child_value("label", f"EEG_{i}")
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "eeg")
    eegOutlet = StreamOutlet(eegOutletInfo)

    numberOfSamples = 1000
    numberOfChannels = 129

    # push 1000 samples a second 
    sampleNumber = 1
    while experimentDictionary['dataCollectionRunning']:
        try:
            startTime = local_clock()

            testData = ([sampleNumber] * numberOfChannels) * numberOfSamples
            #testData = np.full(shape = (numberOfSamples,numberOfChannels), fill_value = sampleNumber)
            #testData[:, -1] = np.random.randint(2, size=numberOfSamples) + DIN_OFF_VALUE
            eegOutlet.push_chunk(testData)
            sampleNumber += 1

            sleepTime = 1 - (local_clock() - startTime)
            if sleepTime > 0:
                sleep(sleepTime)
        except:
            break
        
if __name__ == '__main__':
    main()