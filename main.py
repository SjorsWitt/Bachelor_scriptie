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

def getScopeSize(scope):
    return scope["Box"][1] - scope["Box"][0]

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

# get all data required for above average name lengths
def getAboveAverageData(red, nameNodes):

    biggestGlobalCluster = []
    biggestLocalCluster = []

    for nameNode in nameNodes:
        allOccurrences = getAllNameOccurrences(red, nameNode)
        scopes = getScopes(allOccurrences, parameters.CLUSTER_DISTANCE)

        if scopes["Global"]:
            biggestCluster = max(scopes["Global"]["Clusters"], key=len)

            if len(biggestCluster) > len(biggestGlobalCluster):
                biggestGlobalCluster = biggestCluster
            elif len(biggestCluster) == len(biggestGlobalCluster) and \
                            len(biggestCluster[0].value) > len(biggestGlobalCluster[0].value):
                biggestGlobalCluster = biggestCluster

        if scopes["Local"]:
            biggestClusters = []
            for localScope in scopes["Local"]:
                biggestClusters.append(max(localScope["Clusters"], key=len))

            biggestCluster = max(biggestClusters, key=len)

            if len(biggestCluster) > len(biggestLocalCluster):
                biggestLocalCluster = biggestCluster
            elif len(biggestCluster) == len(biggestLocalCluster) and \
                            len(biggestCluster[0].value) > len(biggestLocalCluster[0].value):
                biggestLocalCluster = biggestCluster

    return biggestGlobalCluster, biggestLocalCluster

# get all data required for below average name lengths
def getBelowAverageData(red, nameNodes):

    # smallest cluster of (biggest clusters per variable)
    smallestBigGlobalCluster = None
    smallestBigLocalCluster = None

    # first appearance of same variable as in smallestBigLocalCluster
    firstLocalAppearance = None

    clusters = []
    for nameNode in nameNodes:
        allOccurrences = getAllNameOccurrences(red, nameNode)
        scopes = getScopes(allOccurrences, parameters.CLUSTER_DISTANCE)

        if scopes["Global"]:
            clusters.append(scopes["Global"]["Clusters"]) # collecting all local and global clusters

            biggestCluster = max(scopes["Global"]["Clusters"], key=len)

            if smallestBigGlobalCluster == None:
                smallestBigGlobalCluster = biggestCluster
            if len(biggestCluster) < len(smallestBigGlobalCluster):
                smallestBigGlobalCluster = biggestCluster
            elif len(biggestCluster) == len(smallestBigGlobalCluster) and \
                            len(biggestCluster[0].value) < len(smallestBigGlobalCluster[0].value):
                smallestBigGlobalCluster = biggestCluster

        if scopes["Local"]:
            biggestClusters = []
            firstAppearances = []
            for localScope in scopes["Local"]:
                clusters.append(localScope["Clusters"]) # collecting all local and global clusters
                biggestClusters.append(max(localScope["Clusters"], key=len))
                firstAppearances.append(localScope["Variables"][0])

            smallestBigCluster = min(biggestClusters, key=len)
            firstAppearance = firstAppearances[biggestClusters.index(smallestBigCluster)]

            if smallestBigLocalCluster == None:
                smallestBigLocalCluster = smallestBigCluster
                firstLocalAppearance = firstAppearance
            elif len(smallestBigCluster) < len(smallestBigLocalCluster):
                smallestBigLocalCluster = smallestBigCluster
                firstLocalAppearance = firstAppearance

            elif len(smallestBigCluster) == len(smallestBigLocalCluster):
                if isWord(smallestBigLocalCluster[0].value) and not isWord(smallestBigCluster[0].value):
                    smallestBigLocalCluster = smallestBigCluster
                    firstLocalAppearance = firstAppearance
                elif (isWord(smallestBigLocalCluster[0].value) or not isWord(smallestBigCluster[0].value)) and \
                                len(smallestBigCluster[0].value) < len(smallestBigLocalCluster[0].value):
                    smallestBigLocalCluster = smallestBigCluster
                    firstLocalAppearance = firstAppearance

    biggestLineRange = {}
    biggestLineRange["Line Range"] = 0
    biggestLineRange["Variable"] = None
    for cluster in clusters:
        distance = getBiggestDistance(cluster)
        if distance > biggestLineRange["Line Range"]:
            biggestLineRange["Line Range"] = distance
            biggestLineRange["Variable"] = cluster[0][0]

    return smallestBigGlobalCluster, smallestBigLocalCluster, firstLocalAppearance, biggestLineRange

def isWord(string):
    nlDict = enchant.Dict("nl_NL")
    engDict = enchant.Dict("en_US")
    return (nlDict.check(string) or engDict.check(string))

def getBiggestDistance(cluster):
    biggestDistance = 0

    for nameNode, nextNameNode in zip(cluster, cluster[1:]):
        distance = getLineNumber(nextNameNode[0]) - getLineNumber(nameNode[-1])
        if distance > biggestDistance:
            biggestDistance = distance

    return biggestDistance


if __name__ == "__main__":
    fileName = raw_input("Give file name: ")

    with open("test_files/" + fileName + ".py", "r") as source_code:
        print "Loading..."
        red = redbaron.RedBaron(source_code.read())

    allVariables = getAllVariables(red)
    singleLetterNames = getSingleLetterNames(allVariables, parameters.EXCLUDE_ITERATORS)
    belowAverageNames = getBelowGoalAverageNames(allVariables, parameters.EXCLUDE_SINGLE_LETTER, parameters.EXCLUDE_ITERATORS)
    # averageNames = getGoalAverageNames(allVariables)
    aboveAverageNames = getAboveGoalAverageNames(allVariables)
    tooLongNames = getTooLongNames(allVariables)

    if allVariables:
        averageNameLength = calculateAverageNameLength(allVariables)

    biggestGlobalCluster, biggestLocalCluster = getAboveAverageData(red, aboveAverageNames)
    smallestBigGlobalCluster, smallestBigLocalCluster, firstLocalAppearance, biggestLineRange = getBelowAverageData(red, belowAverageNames)

    if singleLetterNames:
        print "\n", feedback.SINGLE_LETTER
        for nameNode in singleLetterNames:
            print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + "."

    if tooLongNames:
        print "\n", feedback.TOO_LONG
        for nameNode in tooLongNames:
            print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + "."

    if allVariables and averageNameLength < parameters.MIN_AVERAGE_NAME_LENGTH:
        print "\n", feedback.TOO_SHORT_AVERAGE

    if allVariables and averageNameLength > parameters.MAX_AVERAGE_NAME_LENGTH:
        print "\n", feedback.TOO_LONG_AVERAGE


    if smallestBigGlobalCluster and len(smallestBigGlobalCluster) < parameters.GLOBAL_BIG_CLUSTER:
        print "\n" + feedback.GLOBAL_TOO_SHORT_SMALL_CLUSTER
        print feedback.EXAMPLE_TOO_SHORT
        print "\t- '" + smallestBigGlobalCluster[0].value + "', first appearance in line " + \
              str(getLineNumber(smallestBigGlobalCluster[0]))

    if smallestBigLocalCluster and len(smallestBigLocalCluster) < parameters.LOCAL_BIG_CLUSTER:
        print "\n" + feedback.LOCAL_TOO_SHORT_SMALL_CLUSTER
        print feedback.EXAMPLE_TOO_SHORT
        print "\t- '" + firstLocalAppearance.value + "', first appearance in line " + \
              str(getLineNumber(firstLocalAppearance))

    if biggestLineRange["Line Range"] > 10:
        print "\n" + feedback.TOO_SHORT_BIG_LINE_RANGE
        print feedback.EXAMPLE_TOO_SHORT
        print "\t- '" + biggestLineRange["Variable"].value + "', first appearance in line " + \
              str(getLineNumber(biggestLineRange["Variable"]))


    if len(biggestGlobalCluster) >= parameters.GLOBAL_BIG_CLUSTER:
        print "\n" + feedback.GLOBAL_TOO_LONG_BIG_CLUSTER
        print feedback.EXAMPLE_TOO_LONG
        print "\t- '" + biggestGlobalCluster[0].value + "' is used too much in lines " + \
              str(getLineNumber(biggestGlobalCluster[0])) + "-" + str(getLineNumber(biggestGlobalCluster[-1]))

    if len(biggestLocalCluster) >= parameters.LOCAL_BIG_CLUSTER:
        print "\n" + feedback.LOCAL_TOO_LONG_BIG_CLUSTER
        print feedback.EXAMPLE_TOO_LONG
        print "\t- '" + biggestLocalCluster[0].value + "' is used too much in lines " + \
              str(getLineNumber(biggestLocalCluster[0])) + "-" + str(getLineNumber(biggestLocalCluster[-1]))