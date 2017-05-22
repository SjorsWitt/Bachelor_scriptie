import feedback
import parameters
import redbaron

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

def tooShortAverageLength(nameNodes):
    if calculateAverageNameLength(nameNodes) < parameters.MIN_AVERAGE_NAME_LENGTH:
        return True
    return False

def tooLongAverageLength(nameNodes):
    if calculateAverageNameLength(nameNodes) > parameters.MAX_AVERAGE_NAME_LENGTH:
        return True
    return False

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

def getAboveAverageData(red, nameNodes):
    biggestGlobalCluster = []
    biggestLocalCluster = []
    biggestScope = None

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

            scope = max(scopes["Local"], key=getScopeSize)
            if biggestScope == None:
                biggestScope = scope
            elif getScopeSize(scope) > getScopeSize(biggestScope):
                biggestScope = scope
            elif getScopeSize(scope) == getScopeSize(biggestScope) and \
                            len(scope["Variables"][0].value) > len(biggestScope["Variables"][0].value):
                biggestScope = scope

    return biggestGlobalCluster, biggestLocalCluster, biggestScope

if __name__ == "__main__":

    with open("test_files/test_program.py", "r") as source_code:
        red = redbaron.RedBaron(source_code.read())

    allVariableNames = getAllVariableNames(red)
    singleLetterNames = getSingleLetterNames(allVariableNames, True)
    belowAverageNames = getBelowGoalAverageNames(allVariableNames, False, False)
    # averageNames = getGoalAverageNames(allVariableNames)
    aboveAverageNames = getAboveGoalAverageNames(allVariableNames)
    tooLongNames = getTooLongNames(allVariableNames)

    biggestGlobalCluster, biggestLocalCluster, biggestScope = getAboveAverageData(red, aboveAverageNames)

    if singleLetterNames:
        print "\n", feedback.SINGLE_LETTER
        for nameNode in singleLetterNames:
            print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + "."

    if tooLongNames:
        print "\n", feedback.TOO_LONG
        for nameNode in tooLongNames:
            print "'" + nameNode.value + "', first appearance in line " + str(getLineNumber(nameNode)) + "."

    if tooShortAverageLength(allVariableNames):
        print "\n", feedback.TOO_SHORT_AVERAGE

    if tooLongAverageLength(allVariableNames):
        print "\n", feedback.TOO_LONG_AVERAGE

    if len(biggestGlobalCluster) >= 4:
        print "\n" + feedback.GLOBAL_BIG_CLUSTER
        print "Example of such a variable in your code:"
        print "\t- '" + biggestGlobalCluster[0].value + "' (Global variable) is used too much in lines " + \
              str(getLineNumber(biggestGlobalCluster[0])) + "-" + str(getLineNumber(biggestGlobalCluster[-1]))

    if len(biggestLocalCluster) >= 3:
        print "\n" + feedback.LOCAL_BIG_CLUSTER
        print "Example of such a variable in your code:"
        print "\t- '" + biggestLocalCluster[0].value + "' (Local variable) is used too much in lines " + \
              str(getLineNumber(biggestLocalCluster[0])) + "-" + str(getLineNumber(biggestLocalCluster[-1]))

    if getScopeSize(biggestScope) <= 8:
        print "\n" + feedback.SMALL_LOCAL_SCOPE
        print "Example of such a variable in your code:"
        print "\t- '" + biggestScope["Variables"][0].value + "' in the local scope ranging from " + \
              str(biggestScope["Box"])



    # badLongNames = []
    # for nameNode in aboveAverageNames:
    #     allOccurrences = getAllNameOccurrences(red, nameNode)
    #     scopes = getScopes(allOccurrences,parameters.CLUSTER_DISTANCE)
    #     totalFeedback = {}
    #
    #     if scopes["Global"]:
    #         for cluster in scopes["Global"]["Clusters"]:
    #             if (any(len(cluster) >= 4 for cluster in scopes["Global"]["Clusters"])):
    #                 totalFeedback["Global"] = feedback.GLOBAL_BIG_CLUSTER
    #
    #     if scopes["Local"]:
    #         for localScope in scopes["Local"]:
    #             localFeedback = {}
    #             if any(len(cluster) >= 3 for cluster in localScope["Clusters"]):
    #                 localFeedback.setdefault("Feedback", []).append(feedback.LOCAL_BIG_CLUSTER)
    #
    #             if getScopeSize(localScope) <= 8:
    #                 localFeedback.setdefault("Feedback", []).append(feedback.SMALL_LOCAL_SCOPE)
    #
    #             if localFeedback:
    #                 localFeedback["Box"] = localScope["Box"]
    #                 totalFeedback.setdefault("Local", []).append(localFeedback)
    #
    #     if totalFeedback:
    #         badLongNames.append((nameNode, totalFeedback))

    # print "\nBad long names:"
    # for name in badLongNames:
    #     firstLine = "\t- '" + name[0].value
    #     secondLine = "\t Reason:"
    #     if "Global" in name[1]:
    #         firstLine += ", first appearance in line " + str(getLineNumber(name[0])) + " (Global variable)"




    # badLongNames = []
    # for nameNode in aboveAverageNames:
    #     allOccurrences = getAllNameOccurrences(red, nameNode)
    #     scopes = getScopes(allOccurrences,parameters.CLUSTER_DISTANCE)
    #     done = False

    #     if scopes["Local"]:
    #         for localScope in scopes["Local"]:
    #             for cluster in localScope["Clusters"]:
    #                 if len(cluster) > parameters.LOCAL_DISTINCTION:
    #                     badLongNames.append(nameNode)
    #                     done = True
    #                     break
    #             if done:
    #                 break

    #     if not done and scopes["Global"]:
    #         for cluster in scopes["Global"]["Clusters"]:
    #             if len(cluster) > parameters.GLOBAL_DISTINCTION:
    #                 badLongNames.append(nameNode)
    #                 break


    # badShortNames = []
    # for nameNode in belowAverageNames:
    #     allOccurrences = getAllNameOccurrences(red, nameNode)
    #     scopes = getScopes(allOccurrences, parameters.CLUSTER_DISTANCE)
    #     nameIsBad = True

    #     if scopes["Global"]:
    #         for cluster in scopes["Global"]["Clusters"]:
    #             if len(cluster) > parameters.GLOBAL_DISTINCTION:
    #                 nameIsBad = False
    #                 break

    #     if nameIsBad and scopes["Local"]:
    #         for localScope in scopes["Local"]:
    #             for cluster in localScope["Clusters"]:
    #                 if len(cluster) > parameters.LOCAL_DISTINCTION:
    #                     nameIsBad = False
    #                     break
    #             if not nameIsBad:
    #                 break

    #     if nameIsBad:
    #         badShortNames.append(nameNode)


    # print "\nBad long names:"
    # for name in badLongNames:
    #     print "\t- ", name.value, "in line", getLineNumber(name)

    # print "\nBad short names:"
    # for name in badShortNames:
    #     print "\t- ", name.value, "in line", getLineNumber(name)