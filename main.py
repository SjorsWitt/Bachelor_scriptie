from redbaron import RedBaron

def getAllVariableNames(red, recursive = True):
    variableNames = []

    variableNames.extend(getNamesFromAssignments(red, recursive))
    variableNames.extend(getNamesFromParameters(red, recursive))
    variableNames.extend(getNamesFromIterators(red, recursive))

    return variableNames

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

def calculateAverage(red):
    names = getAllVariableNames(red)
    lengthTotal = 0.0
    namesAmount = len(names)
    
    for name in names:
        lengthTotal += len(name.value)

    return lengthTotal/namesAmount

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

# names longer than 25 characters
def numberOfTooLongNames(red):
    numberOfTooLongNames = 0

    for name in getAllVariableNames(red):
        if len(name.value) > 25:
            numberOfTooLongNames += 1

    return numberOfTooLongNames

def TooLongNamePresent(red):
    if numberOfTooLongNames(red) > 0:
        return True

with open("random_program.py", "r") as source_code:
    red = RedBaron(source_code.read())

AllVariableNames = getAllVariableNames(red)
print AllVariableNames
print calculateAverage(red)

if singleLetterNamePresent(red):
    print "Variable names should not consist of a single letter, unless it is a for loop iterator."

if TooLongNamePresent(red):
    print "Variable names of more than 25 characters should be avoided."