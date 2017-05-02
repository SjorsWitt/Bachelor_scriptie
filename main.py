import feedback
import parameters
from redbaron import RedBaron

# returns list of NameNodes
def getAllVariableNames(red, recursive = True):
    allVariableNames = []

    allVariableNames.extend(getNamesFromAssignments(red, recursive))
    allVariableNames.extend(getNamesFromParameters(red, recursive))
    allVariableNames.extend(getNamesFromIterators(red, recursive))

    return allVariableNames

# returns set of strings
def getAllVariableNamesSet(red, recursive = True):
    allVariableNames = []
    for nameNode in getAllVariableNames(red, recursive):
        allVariableNames.append(nameNode.value)

    return set(allVariableNames)

def getNamesFromAssignments(red, recursive = True):
    assignments = []

    for assignment in red.find_all("assignment", recursive = recursive):
        assignments.extend(assignment.target.find_all("name"))

    return assignments

def getNamesFromParameters(red, recursive = True):
    parameters = []

    for definition in red.find_all("def", recursive = recursive):
        for argument in definition.arguments:
            parameters.append(argument.target)

    return parameters

def getNamesFromIterators(red, recursive = True):
    iterators = []

    for loop in red.find_all("for", recursive = recursive):
        iterators.extend(loop.iterator.find_all("name"))

    return iterators

def calculateAverageNameLength(red):
    names = getAllVariableNamesSet(red)
    lengthTotal = 0.0
    namesAmount = len(names)
    
    for name in names:
        lengthTotal += len(name)

    return lengthTotal/namesAmount

def tooShortAverageLength(red):
    if calculateAverageNameLength(red) < parameters.minAverageNameLength:
        return True

def tooLongAverageLength(red):
    if calculateAverageNameLength(red) > parameters.maxAverageNameLength:
        return True

# does not check iterators
def numberOfSingleLetterNames(red):
    numberOfSingleLetterNames = 0

    variableNames = []
    variableNames.extend(getNamesFromAssignments(red))
    variableNames.extend(getNamesFromParameters(red))

    for name in variableNames:
        if len(name.value) == 1:
            numberOfSingleLetterNames += 1

    return numberOfSingleLetterNames

def singleLetterNamePresent(red):
    if numberOfSingleLetterNames(red) > 0:
        return True

def numberOfTooLongNames(red):
    numberOfTooLongNames = 0

    for name in getAllVariableNames(red):
        if len(name.value) > parameters.maxNameLength:
            numberOfTooLongNames += 1

    return numberOfTooLongNames

def TooLongNamePresent(red):
    if numberOfTooLongNames(red) > 0:
        return True

with open("test_files/test_program.py", "r") as source_code:
    red = RedBaron(source_code.read())

AllVariableNames = getAllVariableNames(red)
print AllVariableNames

if tooShortAverageLength(red):
    print feedback.tooShortAverageLength

if tooLongAverageLength(red):
    print feedback.tooLongAverageLength

if singleLetterNamePresent(red):
    print feedback.singleLetter

if TooLongNamePresent(red):
    print feedback.tooLong

print list(getAllVariableNamesSet(red))
print calculateAverageNameLength(red)