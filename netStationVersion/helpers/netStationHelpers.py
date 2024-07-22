from egi_pynetstation import NetStation


# ====================================================================================

# == Outlet Helper Functions ==

# Prepares the outlet that will be connected to for offline and realtime analyses
def initializeEventsOutlet():

    # IP address of NetStation - CHANGE THIS TO MATCH THE IP ADDRESS OF YOUR NETSTATION
    IP_ns = '10.10.10.42' #needs to be specified for the computer

    # IP address of amplifier (if using 300
    # series, this is the same as the IP address of
    # NetStation. If using newer series, the amplifier
    # has its own IP address)
    IP_amp = '10.10.10.51'

    #Port configured for ECI in NetStation - CHANGE THIS IF NEEDED
    port_ns = 55513

    eventsOutlet = NetStation.NetStation(IP_ns, port_ns)
    eventsOutlet.connect(ntp_ip = IP_amp)
    eventsOutlet.begin_rec()
    preSendTags(eventsOutlet) # send tags so that they will always be ordered properly
    eventsOutlet.send_event(event_type = 'STRT', start = 0.0)

    return eventsOutlet

# Sends a tag from an outlet
def sendTag(tag, outlet):
    outlet.send_event(event_type = tag)

# ====================================================================================

def preSendTags(eventsOutlet):

    # Level Tags
    for i in range(1, 100):
        
        if len(str(i)) == 1: # handles 1 digit numbers
            tag = 'FXX' + str(i)
        else: # handles 2 digit numbers
            tag = 'FX' + str(i)

        eventsOutlet.send_event(event_type = tag)
    
    # Performance Tags
    for totalTargets in range(1, 8):
        for targetsSelected in range(totalTargets + 1):
            for numberOfDistractors in range(totalTargets + 3):
                eventsOutlet.send_event(event_type = f'P{targetsSelected}{totalTargets}{numberOfDistractors}')
    
    # Constant Tags
    eventsOutlet.send_event(event_type = 'OPN0') # eyes open start
    eventsOutlet.send_event(event_type = 'OPN1') # eyes open end
    eventsOutlet.send_event(event_type = 'CLS0') # eyes closed start 
    eventsOutlet.send_event(event_type = 'CLS1') # eyes closed end
    eventsOutlet.send_event(event_type = 'TRL0') # start of real trials
    eventsOutlet.send_event(event_type = 'HGLT') # highlight balls phase start
    eventsOutlet.send_event(event_type = 'MVMT') # movement phase start
    eventsOutlet.send_event(event_type = 'SLCT') # selection phase start
    eventsOutlet.send_event(event_type = 'CLCK') # ball clicked
    eventsOutlet.send_event(event_type = 'UCLK') # ball unclicked
    eventsOutlet.send_event(event_type = 'SBMT') # selection submitted
    eventsOutlet.send_event(event_type = 'TMUP') # timeup
    eventsOutlet.send_event(event_type = 'BRK0') # break start
    eventsOutlet.send_event(event_type = 'BRK1') # break end
    eventsOutlet.send_event(event_type = 'TRL1') # end of real trials
    eventsOutlet.send_event(event_type = 'QUIT') # end of experiment

     




