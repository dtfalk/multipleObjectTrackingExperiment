import os
import csv
import time
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

    # count variable to keep track of each tag's number
    tagToNumberList = [('DIN1', 1)]
    eventsOutlet.send_event('DIN1')
    time.sleep(200)
    count = 2

    # Level Tags
    for i in range(2, 100):
        
        if len(str(i)) == 1: # handles 1 digit numbers
            tag = 'FXX' + str(i)
        else: # handles 2 digit numbers
            tag = 'FX' + str(i)

        eventsOutlet.send_event(event_type = tag)
        tagToNumberList.append((tag, count))
        count += 1
        time.sleep(200)
    
    # Trial Tags
    for i in range(1, 201):
        
        if len(str(i)) == 1:
            tag = f'LLL{i}'
        elif len(str(i)) == 2:
            tag = f'LL{i}'
        else:
            tag = f'L{i}'
            
        eventsOutlet.send_event(event_type = tag)
        tagToNumberList.append((tag, count))
        count += 1
        time.sleep(200)

    
    # Performance Tags
    for totalTargets in range(1, 8):
        for targetsSelected in range(totalTargets + 1):
            for numberOfDistractors in range(totalTargets + 3):
                eventsOutlet.send_event(event_type = f'P{targetsSelected}{totalTargets}{numberOfDistractors}')
                tagToNumberList.append((f'P{targetsSelected}{totalTargets}{numberOfDistractors}', count))
                count += 1
                time.sleep(200)

    
    # Constant Tags
    eventsOutlet.send_event(event_type = 'OPN0') # eyes open start
    tagToNumberList.append(('OPN0', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'OPN1') # eyes open end
    tagToNumberList.append(('OPN1', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'CLS0') # eyes closed start 
    tagToNumberList.append(('CLS0', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'CLS1') # eyes closed end
    tagToNumberList.append(('CLS1', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'TRL0') # start of real trials
    tagToNumberList.append(('TRL0', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'HGLT') # highlight balls phase start
    tagToNumberList.append(('HGLT', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'MVMT') # movement phase start
    tagToNumberList.append(('MVMT', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'SLCT') # selection phase start
    tagToNumberList.append(('SLCT', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'CLCK') # ball clicked
    tagToNumberList.append(('CLCK', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'UCLK') # ball unclicked
    tagToNumberList.append(('UCLK', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'SBMT') # selection submitted
    tagToNumberList.append(('SBMT', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'TMUP') # timeup
    tagToNumberList.append(('TMUP', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'BRK0') # break start
    tagToNumberList.append(('BRK0', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'BRK1') # break end
    tagToNumberList.append(('BRK1', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'TRL1') # end of real trials
    tagToNumberList.append(('TRL1', count))
    count += 1
    time.sleep(200)


    eventsOutlet.send_event(event_type = 'QUIT') # end of experiment
    tagToNumberList.append(('QUIT', count))
    count += 1
    time.sleep(200)


    with open(os.path.join(os.path.dirname(__file__), '..', 'numbersToTags.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        header = ['Number', 'Tag']
        writer.writerow(header)
        
        for tag, number in tagToNumberList:
            writer.writerow([tag, str(number)])


     




