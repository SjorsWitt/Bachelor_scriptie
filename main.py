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

    allVariableNameNodes.sort(key=lambda x: getLineNumber(x)) # sort on line number
    return allVariableNameNodes

def getAllNameOccurrences(red, nameNode):
    allOccurrences = []

    for occurrence in red.find_all("name", value = nameNode.value):
        allOccurrences.append(occurrence)

    return allOccurrences

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
        if len(nameNode.value) < parameters.MIN_AVERAGE_NAME_LENGTH:
            belowAverageNames.append(nameNode)

    return belowAverageNames

def getAboveGoalAverageNames(nameNodes):
    aboveAverageNames = []

    for nameNode in nameNodes:
        if len(nameNode.value) > parameters.MAX_AVERAGE_NAME_LENGTH:
            aboveAverageNames.append(nameNode)

    return aboveAverageNames

def getGoalAverageNames(nameNodes):
    goodAverageNames = []

    for nameNode in nameNodes:
        if len(nameNode.value) > parameters.MIN_AVERAGE_NAME_LENGTH and len(nameNode.value) < parameters.MAX_AVERAGE_NAME_LENGTH:
            goodAverageNames.append(nameNode)

    return goodAverageNames

# excludes iterators
def getSingleLetterNames(nameNodes):
    singleLetterNames = []

    nameNodesNoIterators = [nameNode for nameNode in nameNodes if not isIterator(nameNode)]

    for nameNode in nameNodesNoIterators:
        if len(nameNode.value) == 1:
            singleLetterNames.append(nameNode)

    return singleLetterNames

def singleLetterNamePresent(nameNodes):
    if len(getSingleLetterNames(nameNodes)) > 0:
        return True
    return False

def getTooLongNames(nameNodes):
    tooLongNames = []

    for nameNode in nameNodes:
        if len(nameNode.value) > parameters.MAX_NAME_LENGTH:
            tooLongNames.append(nameNode)

    return tooLongNames

def tooLongNamePresent(nameNodes):
    if len(getTooLongNames(nameNodes)) > 0:
        return True
    return False

def getLineNumber(nameNode):
    return nameNode.absolute_bounding_box.top_left.line

# returns variable usage range in line number difference
def getLineRange(nameNodes):
    firstOccurrenceLine = getLineNumber(nameNodes[0])
    lastOccurrenceLine = getLineNumber(nameNodes[-1])
    return lastOccurrenceLine - firstOccurrenceLine

# returns number of indentation tabs
# def getIndentation(nameNode):
#     indentation = len(nameNode.indentation.expandtabs(parameters.TAB_WIDTH))

#     # count function definition (with parameters)/for loop as same 'indentation scope'
#     if isParameter(nameNode) or isIterator(nameNode):
#         indentation += parameters.TAB_WIDTH

#     return indentation/parameters.TAB_WIDTH

# # returns variable usage range in difference in indentation
# def getUsageIndentationRange(nameNodes):
#     iterNameNodes = iter(nameNodes)
#     indentation = getIndentation(next(iterNameNodes))
#     minIndentation = maxIndentation = indentation

#     for nameNode in iterNameNodes:
#         indentation = getIndentation(nameNode)

#         if indentation < minIndentation:
#             minIndentation = indentation

#         if indentation > maxIndentation:
#             maxIndentation = indentation

#     return maxIndentation - minIndentation

# def getScope(nameNode):
#     parent = nameNode.parent_find("def")

#     if parent == None:
#         scope = {}
#         scope["NameNode"] = nameNode
#         scope["Type"] = "Global"
#     else:
#         scope = {}
#         scope["NameNode"] = nameNode
#         scope["Type"] = "Local"
#         boundingBox = parent.absolute_bounding_box
#         scope["Box"] = (boundingBox.top_left.line, boundingBox.bottom_right.line)
#         scope["Size"] = boundingBox.bottom_right.line - boundingBox.top_left.line

#     return scope

# returns all scopes of given NameNodes
def getScopes(nameNodes):
    scopes = {}
    scopes["Global"] = []
    scopes["Local"] = []

    for nameNode in nameNodes:
        parent = nameNode.parent_find("def")

        if parent == None:
            scopes["Global"].append(nameNode)

        else:
            boundingBox = parent.absolute_bounding_box

            if any(scope["Box"] == (boundingBox.top_left.line, boundingBox.bottom_right.line) for scope in scopes["Local"]):
                scope["Variables"].append(nameNode)

            else:
                scope = {}
                scope["Box"] = (boundingBox.top_left.line, boundingBox.bottom_right.line)
                scope["Size"] = boundingBox.bottom_right.line - boundingBox.top_left.line
                scope["Variables"] = [nameNode]
                scopes["Local"].append(scope)
            
    for scope in scopes["Local"]:
        scope["Line range"] = getLineRange(scope["Variables"])

    return scopes


with open("test_files/homework3.py", "r") as source_code:
    red = RedBaron(source_code.read())

allVariableNames = getAllVariableNames(red)

# for nameNode in allVariableNames:
#     allOccurrences = getAllNameOccurrences(red, nameNode)
#     print "Range in lines: " + str(getLineRange(allOccurrences))
#     print "Range in indentation: " + str(getUsageIndentationRange(allOccurrences))
#     for occurrence in allOccurrences:
#         print occurrence.value, getLineNumber(occurrence), getIndentation(occurrence)
#     print "--------------------------------------"


# if tooShortAverageLength(allVariableNames):
#     print feedback.tooShortAverageLength

# if tooLongAverageLength(allVariableNames):
#     print feedback.tooLongAverageLength

# if singleLetterNamePresent(allVariableNames):
#     print feedback.singleLetter
#     for nameNode in getSingleLetterNames(allVariableNames):
#         print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + "."
#     print

# if tooLongNamePresent(allVariableNames):
#     print feedback.tooLong
#     for nameNode in getTooLongNames(allVariableNames):
#         print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + "."
#     print


# for nameNode in getBelowGoalAverageNames(allVariableNames):
#     print getScopes(getAllNameOccurrences(red, nameNode))

print allVariableNames
print "Average variable name length:", calculateAverageNameLength(allVariableNames)
print "Shorter than 10:", getBelowGoalAverageNames(allVariableNames)
print "From 10 to 16:", getGoalAverageNames(allVariableNames)
print "Longer than 16:", getAboveGoalAverageNames(allVariableNames)
print "Single-letter names:", getSingleLetterNames(allVariableNames)
print "Longer than 25:", getTooLongNames(allVariableNames)