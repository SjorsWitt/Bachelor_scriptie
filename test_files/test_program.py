a, b = 1, 2
c = a + b
d = 0
myList = range(10)
emptyList = []
thisVariableNameIsWayTooLong = True

def doSomething(param1, param2):
	param1 += c
	return param1 + param2

something = doSomething(a, c)

for item in myList:
	d += item