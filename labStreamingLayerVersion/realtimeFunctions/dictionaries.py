# file containing dictionaries to translate between tags and event ID numbers

# == Dictionaries for translating between tags and event IDs ==
#DIN_ON_VALUE = 65534 IDK what this value is
DIN_OFF_VALUE = 65535

# Given a dictionary, swaps keys for values and values for keys
# (assumes that the given dictionary constitutes an injection)
def reverseADictionary(dictionary):
    reverseDictionary = {}
    for key, value in dictionary.items():
        reverseDictionary[value] = key
    return reverseDictionary

# Translates each level tag to an event ID number
# 'level 15' ----> 15
def levelTags(tagToEventIdNumberDictionary):
    for i in range(1, 100):
        tagToEventIdNumberDictionary[f'level {i}'] = i
    
    return tagToEventIdNumberDictionary

# Translates a user's performance on a trial to a number
def performanceTags(tagToEventIdNumberDictionary):

    for totalTargets in range(1, 15):
        for selectedTargets in range(totalTargets + 1):
            for numberOfDistractors in range(totalTargets + 3):
                tagToEventIdNumberDictionary[f'{selectedTargets} out of {totalTargets} targets identified with {numberOfDistractors} distractors'] = int(f'9{selectedTargets}{totalTargets}{numberOfDistractors}')


# initalize the dictionary with the bulk of the event tags/event ID numbers
tagToEventIdNumberDictionary = {
    'eyesOpenStart': 101,
    'eyesOpenEnd': 102,
    'eyesClosedStart': 103,
    'eyesClosedEnd': 104,
    'startOfRealTrials': 105,
    'fixationStart': 106,
    'highlightStart': 107,
    'movementStart': 108,
    'selectionStart': 109,
    'ballSelected': 110,
    'ballUnselected': 111,
    'selectionSubmitted': 112,
    'timeup': 113,
    'breakStart': 114,
    'breakEnd': 115,
    'endOfRealTrials': 116,
    'endOfExperiment': -1
}

# add in the level tags
tagToEventIdNumberDictionary = levelTags(tagToEventIdNumberDictionary)
performanceTags(tagToEventIdNumberDictionary)

eventIdNumberToTagDictionary = reverseADictionary(tagToEventIdNumberDictionary)