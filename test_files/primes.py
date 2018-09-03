'''
	
	primes.py
	Prime calculator
	
	(c) 2014 - Pablo Kebees
	http://blobtech.nl
	
'''

from time import clock;
clock()

columns = False;
limit = 1000;

limitLen = len( str( limit ) );
primeCount = 0;
primeStr = '';
adjCand = 2; # starter of candidate list adjacent non-primes
adjCount = 1; # candidate count adjacent non-primes
adjBest = 2; # starter of best list adjacent non-primes
adjLong = 1; # best count adjacent non-primes

if columns == False: # fit maximum columns in 80 width terminal
	columns = int( 78 / ( limitLen + 2 ) );
	
def addPrime( i ):
	global primeCount, primeStr, columns;
	
	primeCount += 1;
	s = str( i );
	primeStr += ' ' * ( limitLen - len( s ) + 2 ) + s;
	if primeCount % columns == 0:
		primeStr += '\n';
	
addPrime( 2 );
i = 3;
while True:
	
	n = 3;
	while n ** 2 <= i:
		if i % n == 0:
			if i == adjCand + adjCount + 1: # remember, we skip evens
				adjCount += 2;
				if adjCount > adjLong:
					adjLong = adjCount;
					adjBest = adjCand;
			else:
				adjCand = i;
				adjCount = 1;
			
			break;
		
		n += 1;
		
	else:
		addPrime( i );
		if primeCount == limit:
			break;
	
	i += 2;

if primeCount % columns != 0: # if 0, str already ends with newline
	primeStr += '\n';
	
print( primeStr );
print( 'Most consecutive non-primes: ' + ', '.join( [ str( i ) for i in range( adjBest, adjBest + adjLong ) ] ) );
print( 'Execution time: ' + str( clock() ) + ' seconds' );