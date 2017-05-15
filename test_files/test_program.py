a, b = 1, 2
c = a + b
d = 0
myList = range(10)
emptyList = []
thisNameIsGood = True

aboveAverageButNotTooLong = True
doAnotherThing(aboveAverageButNotTooLong)

thisVariableNameIsWayTooLong = True

def doSomething(param1, param2):
	param1 += c
	return param1 + param2

def doAnotherThing(param3):
	c += 5
	return param3 - c

def longNameInSmallScope(someList):
	anotherLongNamedList = []
	for thisNameIsLongForItsScope in someList:
		anotherLongNamedList.append(thisNameIsLongForItsScope)
	return anotherLongNamedList

something = doSomething(a, c)

for i in myList:
	d += i

aboveAverageButNotTooLong