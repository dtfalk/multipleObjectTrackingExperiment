from scipy.special import comb
from scipy.stats import norm

# Function for calculating expected balls correct on a trial if user were guessing
def expected_value(game):

    # get the number of targets and total number of balls
    numberOfTargets = game["targets"]
    numberOfDistractors = game["distractors"]
    totalBalls = numberOfTargets + numberOfDistractors

    # begin calculating expected value as sum of value_of_outcome_i * probability_of_outcome_i
    expectedValue = 0

    # iterate over each possible outcome
    for i in range(numberOfTargets + 1):

        # numerator is number of ways of choosing i balls correctly from the total number of targets
        # times the ways of choosing (number of targets - i) number of distractors from the number of distractors
        numerator = comb(numberOfTargets, i) * comb(numberOfDistractors, numberOfTargets - i)

        # denominator is the total number of ways of choosing number of targets number of balls from total number of balls
        denominator = comb(totalBalls, numberOfTargets)

        # we multiply i (number of balls correct i.e. the value of this outcome) by the probability of this outcome (num / denom)
        # and add this to the expected value
        expectedValue += i * (numerator / denominator)

    return expectedValue

# Calculates d-prime value
# Note: misses will always equal false alarms. This means that one miss implies exactly one false alarm
# As a result, every hit implies exactly negative one false alarms. They have a perfectly inverse linear relationship.
# The z-score calculation is a linear transformation. Linear transformations preserver linear relationships.
# As a result, the z-score for hitrate will have a definable linear relationship with the z-score of false alarm rate.
# Since d-prime is just z-score of hitrate minus z-score of false alarm rate, there is a way to write the dprime score
# as a function of JUST hitrate or a function of JUST false alarm rate. 
# As a result, this d-prime calculation is (can be written as) a function of JUST ONE VARIABLE. 
# That is not typical of a dprime rate. Not really how dprime should be used iirc.
def dPrime(numberOfSelectedTargets, game):

    # get the number of targets and total number of balls
    numberOfTargets = game["targets"]
    numberOfDistractors = game["distractors"]

    # Hits := number of correctly identified targets
    hits = numberOfSelectedTargets
    hitRate = hits / numberOfTargets

    # Misses := number of targets that were not identified
    misses = numberOfTargets - numberOfSelectedTargets

    # False Alarms := number of distractors that were selected as targets
    falseAlarms = numberOfTargets - numberOfSelectedTargets
    falseAlarmRate = falseAlarms / numberOfDistractors

    # Correct Rejections := number of distractors that were correctly identified as NOT targets
    correctRejections = numberOfDistractors - falseAlarms

    # values for fixing extreme d primes
    halfHit = 0.5 / (hits + misses)
    halfFalseAlarm = 0.5 / (misses + correctRejections)

    if hitRate == 1:
        hitRate = 1 - halfHit
    if hitRate == 0:
        hitRate = halfHit

    # fix extreme fa rate
    if falseAlarmRate == 1:
        falseAlarmRate = 1 - halfFalseAlarm
    if falseAlarmRate == 0:
        falseAlarmRate = halfFalseAlarm

    # calculate z values
    hitRateZScore = norm.ppf(hitRate)
    falseAlarmRateZScore = norm.ppf(falseAlarmRate)

    # calculate d prime
    dPrime = hitRateZScore - falseAlarmRateZScore
    
    return dPrime