import feedback
import parameters
from redbaron import RedBaron

# returns list of NameNodes
def getAllVariableNames(red):
    allVariableNames = []
    for nameNode in findVariableNamesFromCode(red):
        allVariableNames.append(nameNode.value)

    allVariableNameNodes = []
    for name in set(allVariableNames):
        allVariableNameNodes.append(red.find("name", value = name))

    allVariableNameNodes.sort(key=lambda x: getLineNumber(x)) # sort on line number
    return allVariableNameNodes

def getAllNameOccurrences(red, nameNode):
    allOccurrences = []

    for occurrence in red.find_all("name", value = nameNode.value):
        allOccurrences.append(occurrence)

    return allOccurrences

def findVariableNamesFromCode(red):
    allVariableNames = []

    allVariableNames.extend(getNamesFromAssignments(red))
    allVariableNames.extend(getNamesFromParameters(red))
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

def isIterator(nameNode):
    if nameNode.on_attribute == "iterator":
        return True
    return False

def isParameter(nameNode):
    if nameNode.parent.on_attribute == "arguments":
        return True
    return False

# ignores multiple usages of variables
def calculateAverageNameLength(nameNodes):
    lengthTotal = 0.0
    namesAmount = len(nameNodes)
    
    for nameNode in nameNodes:
        lengthTotal += len(nameNode.value)

    return lengthTotal/namesAmount

def tooShortAverageLength(nameNodes):
    if calculateAverageNameLength(nameNodes) < parameters.MIN_AVERAGE_NAME_LENGTH:
        return True
    return False

def tooLongAverageLength(nameNodes):
    if calculateAverageNameLength(nameNodes) > parameters.MAX_AVERAGE_NAME_LENGTH:
        return True
    return False

def getBelowGoalAverageNames(nameNodes):
    belowAverageNames = []

    for nameNode in nameNodes:
        if len(nameNode.value) > 1 and len(nameNode.value) < parameters.MIN_AVERAGE_NAME_LENGTH:
            belowAverageNames.append(nameNode)

    return belowAverageNames

def getAboveGoalAverageNames(nameNodes):
    aboveAverageNames = []

    for nameNode in nameNodes:
        if len(nameNode.value) > parameters.MAX_AVERAGE_NAME_LENGTH and len(nameNode.value) <= parameters.MAX_NAME_LENGTH:
            aboveAverageNames.append(nameNode)

    return aboveAverageNames

def getGoalAverageNames(nameNodes):
    goodAverageNames = []

    for nameNode in nameNodes:
        if len(nameNode.value) >= parameters.MIN_AVERAGE_NAME_LENGTH and len(nameNode.value) <= parameters.MAX_AVERAGE_NAME_LENGTH:
            goodAverageNames.append(nameNode)

    return goodAverageNames

# excludes iterators
def getSingleLetterNames(nameNodes, excludeIterators = True):
    singleLetterNames = []

    if excludeIterators:
        nameNodes = [nameNode for nameNode in nameNodes if not isIterator(nameNode)]

    for nameNode in nameNodes:
        if len(nameNode.value) == 1:
            singleLetterNames.append(nameNode)

    return singleLetterNames

def getTooLongNames(nameNodes):
    tooLongNames = []

    for nameNode in nameNodes:
        if len(nameNode.value) > parameters.MAX_NAME_LENGTH:
            tooLongNames.append(nameNode)

    return tooLongNames

def getLineNumber(nameNode):
    return nameNode.absolute_bounding_box.top_left.line

# returns variable usage range in line number difference
def getLineRange(nameNodes):
    lines = []
    for nameNode in nameNodes:
        lines.append(getLineNumber(nameNode))

    return max(lines) - min(lines)

# returns all scopes of given NameNodes
def getScopes(nameNodes):
    scopes = {}
    scopes["Global"] = {}
    scopes["Local"] = []

    for nameNode in nameNodes:
        parent = nameNode.parent_find("def")

        if parent == None:
            scopes["Global"].setdefault("Variables", []).append(nameNode)

        else:
            boundingBox = parent.absolute_bounding_box

            scopePresent, index = scopeIsPresent(scopes, boundingBox)
            if scopePresent:
                scopes["Local"][index]["Variables"].append(nameNode)

            else:
                scope = {}
                scope["Box"] = (boundingBox.top_left.line, boundingBox.bottom_right.line)
                scope["Scope range"] = boundingBox.bottom_right.line - boundingBox.top_left.line
                scope["Variables"] = [nameNode]
                scopes["Local"].append(scope)

    if scopes["Global"]:
        scopes["Global"]["Variable range"] = getLineRange(scopes["Global"]["Variables"])

    for scope in scopes["Local"]:
        scope["Variable range"] = getLineRange(scope["Variables"])

    return scopes

# scope is already present in scopes json object
def scopeIsPresent(scopes, boundingBox):
    for i, scope in enumerate(scopes["Local"]):
        if scope["Box"] == (boundingBox.top_left.line, boundingBox.bottom_right.line):
            return True, i
    return False, None


with open("test_files/test_program.py", "r") as source_code:
    red = RedBaron(source_code.read())

allVariableNames = getAllVariableNames(red)
singleLetterNames = getSingleLetterNames(allVariableNames, True)
belowAverageNames = getBelowGoalAverageNames(allVariableNames)
averageNames = getGoalAverageNames(allVariableNames)
aboveAverageNames = getAboveGoalAverageNames(allVariableNames)
tooLongNames = getTooLongNames(allVariableNames)

if singleLetterNames:
    print feedback.singleLetter, "\n"

if tooLongNames:
    print feedback.tooLong
    for nameNode in getTooLongNames(allVariableNames):
        print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + ".\n"

if tooShortAverageLength(allVariableNames):
    print feedback.tooShortAverageLength

if tooLongAverageLength(allVariableNames):
    print feedback.tooLongAverageLength

for nameNode in aboveAverageNames:
    allOccurrences = getAllNameOccurrences(red, nameNode)
    lineRange = getLineRange(allOccurrences)
    variablesAmount = len(allOccurrences)
    scopes = getScopes(allOccurrences)

    # if scopes["Global"] and not scopes["Local"] and variablesAmount < 4:
    #     print nameNode, "is a good name."

    if ((scopes["Global"] and scopes["Global"]["Variable range"] <= 6) or 
        (scopes["Local"] and all(localScope["Variable range"] for localScope in scopes["Local"]) <= 6)):
        print nameNode.value + " is bad."

# if singleLetterNamePresent(allVariableNames):
#     print feedback.singleLetter
#     for nameNode in getSingleLetterNames(allVariableNames):
#         print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + ".\n"


# allBelowAverageNames = []
# for nameNode in getBelowGoalAverageNames(allVariableNames):
#     print getScopes(getAllNameOccurrences(red, nameNode))