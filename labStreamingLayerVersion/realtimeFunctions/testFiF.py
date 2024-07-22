import os
import mne
from .dictionaries import *

def main():
    subjectNumber = input('Subject Number: ')
    curDir = os.path.dirname(__file__)
    resultsPath = os.path.join(curDir, '..', 'results', 'subjectData', subjectNumber, f'{subjectNumber}_raw.fif')

    raw = mne.io.read_raw_fif(resultsPath, preload = True)
    events = mne.events_from_annotations(raw, event_id = tagToEventIdNumberDictionary)
    print(events)


if __name__ == '__main__':
    main()