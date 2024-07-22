from pylsl import StreamInfo, StreamInlet, StreamOutlet # lab streaming layer classes
from pylsl import resolve_stream # lab streaming layer functions
from pylsl import IRREGULAR_RATE # lab streaming layer constants and datatypes


# ====================================================================================

# == Outlet Helper Functions ==

# Prepares the outlet that will be connected to for offline and realtime analyses
def initializeEventsOutlet(subjectNumber):

    # prepare lab streaming layer functionality (give it a name, a type, a sampling rate (irregular), and a data type it sends (strings))
    info = StreamInfo(name = f'eventsStream_{subjectNumber}', type = 'Events', channel_count = 1, nominal_srate = IRREGULAR_RATE, channel_format = 'string', source_id = 'MOT_Experiment')
    
    # create the outlet through which we will send tags
    eventOutlet = StreamOutlet(info)

    return eventOutlet

# Sends a tag from an outlet
def sendTag(tag, outlet):
    outlet.push_sample([tag])

# ====================================================================================

# == Inlet Helper Functions ==

# Finds streams of a given type and sets up an LSL inlet for the stream
def initializeInlet(streamType):

    # look for/find the LSL stream of a given type
    print(f'\n\nLooking for {streamType} stream...\n\n')
    streams = resolve_stream('type', type)
    print(f'\n\nfound {streamType} stream named {streams[0].name()}\n\n')

    # initalize the LSL inlet ()
    inlet = StreamInlet(streams[0])

    return inlet


