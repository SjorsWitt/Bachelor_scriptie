import feedback
import parameters
from redbaron import RedBaron

# returns list of NameNodes
def getAllVariableNames(red, includeIterators = True):
    allVariableNames = []
    for nameNode in findVariableNamesFromCode(red, includeIterators):
        allVariableNames.append(nameNode.value)

    allVariableNameNodes = []
    for name in set(allVariableNames):
        allVariableNameNodes.append(red.find("name", value = name))

    return allVariableNameNodes

def findVariableNamesFromCode(red, includeIterators = True):
    allVariableNames = []

    allVariableNames.extend(getNamesFromAssignments(red))
    allVariableNames.extend(getNamesFromParameters(red))
    if includeIterators:
        allVariableNames.extend(getNamesFromIterators(red))

    return allVariableNames

def getNamesFromAssignments(red):
    assignments = []

    for assignment in red.find_all("assignment"):
        assignments.extend(assignment.target.find_all("name"))

    return assignments

def getNamesFromParameters(red):
    parameters = []

    for definition in red.find_all("def"):
        for argument in definition.arguments:
            parameters.append(argument.target)

    return parameters

def getNamesFromIterators(red):
    iterators = []

    for loop in red.find_all("for"):
        iterators.extend(loop.iterator.find_all("name"))

    return iterators

def isIterator(red, nameNode):
    if nameNode.on_attribute == "iterator":
        return True
    return False

def isParameter(red, nameNode):
    if nameNode.parent.on_attribute == "arguments":
        return True
    return False

# ignores multiple usages of variables
def calculateAverageNameLength(red):
    nameNodes = getAllVariableNames(red)
    lengthTotal = 0.0
    namesAmount = len(nameNodes)
    
    for nameNode in nameNodes:
        lengthTotal += len(nameNode.value)

    return lengthTotal/namesAmount

def tooShortAverageLength(red):
    if calculateAverageNameLength(red) < parameters.minAverageNameLength:
        return True
    return False

def tooLongAverageLength(red):
    if calculateAverageNameLength(red) > parameters.maxAverageNameLength:
        return True
    return False

# does not check iterators
def getSingleLetterNames(red):
    singleLetterNames = []

    for nameNode in getAllVariableNames(red, False):
        if len(nameNode.value) == 1:
            singleLetterNames.append(nameNode)

    return singleLetterNames

def singleLetterNamePresent(red):
    if len(getSingleLetterNames(red)) > 0:
        return True
    return False

def getTooLongNames(red):
    tooLongNames = []

    for nameNode in getAllVariableNames(red):
        if len(nameNode.value) > parameters.maxNameLength:
            tooLongNames.append(nameNode)

    return tooLongNames

def TooLongNamePresent(red):
    if len(getTooLongNames(red)) > 0:
        return True
    return False

def getAllNameOccurrences(red, nameNode):
    allOccurrences = []

    for occurrence in red.find_all("name", value = nameNode.value):
        allOccurrences.append(occurrence)

    return allOccurrences

def getLineNumber(red, nameNode):
    return nameNode.absolute_bounding_box.top_left.line

with open("test_files/test_program.py", "r") as source_code:
    red = RedBaron(source_code.read())

# if tooShortAverageLength(red):
#     print feedback.tooShortAverageLength

# if tooLongAverageLength(red):
#     print feedback.tooLongAverageLength

# if singleLetterNamePresent(red):
#     print feedback.singleLetter

# if TooLongNamePresent(red):
#     print feedback.tooLong

for nameNode in getAllVariableNames(red):
    print nameNode, "\t", isIterator(red, nameNode)
    # for occurrence in getAllNameOccurrences(red, nameNode):
    #     print occurrence.value, getLineNumber(red, occurrence)
    # print "--------------------------------------"