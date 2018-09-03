import feedback
import parameters
import redbaron
import enchant

# returns list of NameNodes
def getAllVariables(red):
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
        if isinstance(assignment.target, redbaron.nodes.NameNode):
            assignments.append(assignment.target)

        elif isinstance(assignment.target, redbaron.nodes.TupleNode):
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

def getBelowGoalAverageNames(nameNodes, excludeSingleLetterNames = False, excludeIterators = False):
    belowAverageNames = []

    if excludeIterators:
        nameNodes = [nameNode for nameNode in nameNodes if not isIterator(nameNode)]

    for nameNode in nameNodes:
        if excludeSingleLetterNames:
            if len(nameNode.value) > 1 and len(nameNode.value) < parameters.MIN_AVERAGE_NAME_LENGTH:
                belowAverageNames.append(nameNode)
        else:
            if len(nameNode.value) < parameters.MIN_AVERAGE_NAME_LENGTH:
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

def getSingleLetterVariables(nameNodes):
    singleLetterVariables = []

    for nameNode in nameNodes:
        allOccurrences = getAllNameOccurrences(red, nameNode)
        scopes = getScopes(allOccurrences, parameters.CLUSTER_DISTANCE)

        if scopes["Global"]:
            singleLetterVariables.append(scopes["Global"]["Variables"][0])

        if scopes["Local"]:
            for localScope in scopes["Local"]:
                singleLetterVariables.append(localScope["Variables"][0])

    singleLetterVariables.sort(key=lambda variable: getLineNumber(variable))
    return singleLetterVariables

# returns names that are too long in every scenario (longer than parameters.MAX_NAME_LENGTH)
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
def getScopes(nameNodes, maxDif):
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
                scope["Variables"] = [nameNode]
                scopes["Local"].append(scope)

    if scopes["Global"]:
        # scopes["Global"]["Variables range"] = getLineRange(scopes["Global"]["Variables"])
        # scopes["Global"]["Variables amount"] = len(scopes["Global"]["Variables"])
        scopes["Global"]["Clusters"] = list(grouper(scopes["Global"]["Variables"], maxDif))

    for scope in scopes["Local"]:
        # scope["Variables range"] = getLineRange(scope["Variables"])
        # scope["Variables amount"] = len(scope["Variables"])
        scope["Clusters"] = list(grouper(scope["Variables"], maxDif))

    return scopes

# scope is already present in scopes json object
def scopeIsPresent(scopes, boundingBox):
    for i, scope in enumerate(scopes["Local"]):
        if scope["Box"] == (boundingBox.top_left.line, boundingBox.bottom_right.line):
            return True, i
    return False, None

# groups NameNodes into clusters seperated at least maxDif lines
def grouper(nameNodes, maxDif):
    prevLineNumber = None
    group = []
    for nameNode in nameNodes:
        lineNumber = getLineNumber(nameNode)

        if not prevLineNumber or lineNumber - prevLineNumber <= maxDif:
            group.append(nameNode)
        else:
            yield group
            group = [nameNode]
        prevLineNumber = lineNumber
    if group:
        yield group

def getTooShortVariables(red, nameNodes):
    tooShortVariables = {}
    allClusters = []

    for nameNode in nameNodes:
        allOccurrences = getAllNameOccurrences(red, nameNode)
        scopes = getScopes(allOccurrences, parameters.CLUSTER_DISTANCE)

        if scopes["Global"]:
            allClusters.append(scopes["Global"]["Clusters"])  # collecting all local and global clusters

            biggestClusterLength = len(max(scopes["Global"]["Clusters"], key=len))
            if biggestClusterLength < parameters.GLOBAL_BIG_CLUSTER:
                clusterLengths = tooShortVariables.setdefault(feedback.GLOBAL_TOO_SHORT_CLUSTER, [])
                clusterLengths.append((scopes["Global"]["Variables"][0], biggestClusterLength))

        if scopes["Local"]:
            for localScope in scopes["Local"]:
                allClusters.append(localScope["Clusters"])  # collecting all local and global clusters

                biggestClusterLength = len(max(localScope["Clusters"], key=len))
                if biggestClusterLength < parameters.LOCAL_BIG_CLUSTER:
                    clusterLengths = tooShortVariables.setdefault(feedback.LOCAL_TOO_SHORT_CLUSTER, [])
                    clusterLengths.append((localScope["Variables"][0], biggestClusterLength))

    for clusters in allClusters:
        distance = getBiggestDistance(clusters)
        if distance > parameters.BIG_DISTANCE:
            tooShortVariables.setdefault(feedback.TOO_SHORT_LINE_RANGE, []).append((clusters[0][0], distance))

    return tooShortVariables

def getTooLongVariables(red, nameNodes):
    tooLongVariables = {}

    for nameNode in nameNodes:
        allOccurrences = getAllNameOccurrences(red, nameNode)
        scopes = getScopes(allOccurrences, parameters.CLUSTER_DISTANCE)

        if scopes["Global"]:
            biggestCluster = max(scopes["Global"]["Clusters"], key=len)
            clusterLength = len(biggestCluster)

            if clusterLength >= parameters.GLOBAL_BIG_CLUSTER:
                clusters = tooLongVariables.setdefault(feedback.GLOBAL_TOO_LONG_CLUSTER, [])
                clusters.append((biggestCluster, clusterLength))

        if scopes["Local"]:
            for localScope in scopes["Local"]:
                biggestCluster = max(localScope["Clusters"], key=len)
                clusterLength = len(biggestCluster)

                if clusterLength >= parameters.LOCAL_BIG_CLUSTER:
                    clusters = tooLongVariables.setdefault(feedback.LOCAL_TOO_LONG_CLUSTER, [])
                    clusters.append((biggestCluster, clusterLength))

    return tooLongVariables

# check if string is word; exclude single letter strings (except x and y) as they are considered dictionary words
def isWord(string):
    global nlDict
    global engDict

    if string == "x" or string == "y":
        return True
    elif len(string) == 1:
        return False
    else:
        return (nlDict.check(string) or engDict.check(string))

# finds biggest distance between clusters
def getBiggestDistance(clusters):
    biggestDistance = 0

    for nameNode, nextNameNode in zip(clusters, clusters[1:]):
        distance = getLineNumber(nextNameNode[0]) - getLineNumber(nameNode[-1])
        if distance > biggestDistance:
            biggestDistance = distance

    return biggestDistance

# returns best matching variable for short names
def findBestShortVariable(variables, checkForMin):

    # filter out all dictionary words only if non-dictionary word is present
    if any(not isWord(variable[0].value) for variable in variables):
        variables = [variable for variable in variables if not isWord(variable[0].value)]

    if checkForMin:
        # only leaving in all variables where biggest cluster is the smallest of all variables
        minLength = min(variables, key=lambda variable: variable[1])[1]
        variables = [variable for variable in variables if variable[1] == minLength]
    else:
        # only leaving in all variables with biggest line range in between clusters
        maxLength = max(variables, key=lambda variable: variable[1])[1]
        variables = [variable for variable in variables if variable[1] == maxLength]

    # find variable with shortest name
    return min(variables, key=lambda variable: len(variable[0].value))

def findBestLongVariable(variables):
    # only leaving in all variables with biggest line range in between clusters
    maxClusterLength = max(variables, key=lambda variable: variable[1])[1]
    variables = [variable for variable in variables if variable[1] == maxClusterLength]

    # find variable(s) with longest name
    maxNameVariable = max(variables, key=lambda variable: len(variable[0][0].value))
    maxNameLength = len(maxNameVariable[0][0].value)
    variables = [variable for variable in variables if len(variable[0][0].value) == maxNameLength]

    # return variable where cluster has smallest line range
    return min(variables, key=lambda variable: getLineNumber(variable[0][-1]) - getLineNumber(variable[0][0]))

if __name__ == "__main__":
    nlDict = enchant.Dict("nl_NL")
    engDict = enchant.Dict("en_US")

    fileName = raw_input("Give file name: ")

    with open("evaluation/" + fileName + ".py", "r") as source_code:
        print "Loading..."
        red = redbaron.RedBaron(source_code.read())

    allVariables = getAllVariables(red)
    singleLetterNames = getSingleLetterNames(allVariables, parameters.EXCLUDE_ITERATORS_SL)
    belowAverageNames = getBelowGoalAverageNames(allVariables, parameters.EXCLUDE_SINGLE_LETTER, parameters.EXCLUDE_ITERATORS_BA)
    aboveAverageNames = getAboveGoalAverageNames(allVariables)
    tooLongNames = getTooLongNames(allVariables)

    if allVariables:
        averageNameLength = calculateAverageNameLength(allVariables)

    tooShortVariables = getTooShortVariables(red, belowAverageNames)
    toolongVariables = getTooLongVariables(red, aboveAverageNames)
    singleLetterVariables = getSingleLetterVariables(singleLetterNames)

    if allVariables and averageNameLength < parameters.MIN_AVERAGE_NAME_LENGTH:
        print "\n" + feedback.TOO_SHORT_AVERAGE

    if allVariables and averageNameLength > parameters.MAX_AVERAGE_NAME_LENGTH:
        print "\n" + feedback.TOO_LONG_AVERAGE

    # if names in two different languages are found (exclude single letters and words existing in both languages)
    if any(len(variable.value) != 1 and not (nlDict.check(variable.value) and engDict.check(variable.value)) and \
                        nlDict.check(variable.value) for variable in allVariables) and \
            any(len(variable.value) != 1 and not (nlDict.check(variable.value) and engDict.check(variable.value)) and \
                        engDict.check(variable.value) for variable in allVariables):
        print "\n" + feedback.SAME_LANGUAGE

    if singleLetterVariables:
        print "\n" + feedback.SINGLE_LETTER
        for nameNode in singleLetterVariables:
            print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + "."

    if tooLongNames:
        print "\n" + feedback.TOO_LONG
        for nameNode in tooLongNames:
            print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + "."


    # if tooShortVariables.has_key(feedback.GLOBAL_TOO_SHORT_CLUSTER):
    #     bestVariable = findBestShortVariable(tooShortVariables[feedback.GLOBAL_TOO_SHORT_CLUSTER], True)
    #
    #     print "\n" + feedback.GLOBAL_TOO_SHORT_CLUSTER
    #     print feedback.EXAMPLE_GLOBAL_SHORT_CLUSTER
    #     print "\t- '" + bestVariable[0].value + "', first appearance in line " + \
    #           str(getLineNumber(bestVariable[0]))
    #
    # if tooShortVariables.has_key(feedback.LOCAL_TOO_SHORT_CLUSTER):
    #     bestVariable = findBestShortVariable(tooShortVariables[feedback.LOCAL_TOO_SHORT_CLUSTER], True)
    #
    #     print "\n" + feedback.LOCAL_TOO_SHORT_CLUSTER
    #     print feedback.EXAMPLE_LOCAL_SHORT_CLUSTER
    #     print "\t- '" + bestVariable[0].value + "', first appearance in line " + \
    #           str(getLineNumber(bestVariable[0]))
    #
    # if tooShortVariables.has_key(feedback.TOO_SHORT_LINE_RANGE):
    #     bestVariable = findBestShortVariable(tooShortVariables[feedback.TOO_SHORT_LINE_RANGE], False)
    #
    #     print "\n" + feedback.TOO_SHORT_LINE_RANGE
    #     print feedback.EXAMPLE_SHORT_LINE_RANGE
    #     print "\t- '" + bestVariable[0].value + "', first appearance in line " + \
    #           str(getLineNumber(bestVariable[0]))
    #
    #
    # if toolongVariables.has_key(feedback.GLOBAL_TOO_LONG_CLUSTER):
    #     bestVariable = findBestLongVariable(toolongVariables[feedback.GLOBAL_TOO_LONG_CLUSTER])
    #
    #     print "\n" + feedback.GLOBAL_TOO_LONG_CLUSTER
    #     print feedback.EXAMPLE_GLOBAL_LONG_CLUSTER
    #     print "\t- '" + bestVariable[0][0].value + "' is used frequently in lines " + \
    #           str(getLineNumber(bestVariable[0][0])) + "-" + str(getLineNumber(bestVariable[0][-1]))
    #
    # if toolongVariables.has_key(feedback.LOCAL_TOO_LONG_CLUSTER):
    #     bestVariable = findBestLongVariable(toolongVariables[feedback.LOCAL_TOO_LONG_CLUSTER])
    #
    #     print "\n" + feedback.LOCAL_TOO_LONG_CLUSTER
    #     print feedback.EXAMPLE_LOCAL_LONG_CLUSTER
    #     print "\t- '" + bestVariable[0][0].value + "' is used frequently in lines " + \
    #           str(getLineNumber(bestVariable[0][0])) + "-" + str(getLineNumber(bestVariable[0][-1]))

    for key in tooShortVariables:
        print "\n" + key
        for variable in tooShortVariables[key]:
            print str(getLineNumber(variable[0])) + " - " + variable[0].value

    for key in toolongVariables:
        print "\n" + key
        for variable in toolongVariables[key]:
            print str(getLineNumber(variable[0][0])) + " - " + variable[0][0].value