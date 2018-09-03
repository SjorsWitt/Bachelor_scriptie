import matplotlib.pyplot as plt

def parseFile( str ):
	return [ [ int( i ) for i in line.split( ',' ) ] for line in open( str, 'r' ).readlines()[ 21: ] ];

minFile = 'TN_STAID000162.txt';
highFile = 'TX_STAID000162.txt';

minData = parseFile( minFile );
longest = 0;
current = 0;
longDate = 0;
end = False;
low = minData[ 0 ][ 3 ];
last = 1;
for entry in minData:
	if entry[ 3 ] < low:
		low = entry[ 3 ];
	
	if entry[ 3 ] < 0:
		if last > 0:
			current = 1;
		else:
			current += 1;
	else:
		if last < 0:
			if longest < current:
				longest = current;
				longDate = entry[ 2 ];
	
	last = entry[ 3 ];

histValues = [];
highData = parseFile( highFile );
high = minData[ 0 ][ 3 ];
for entry in highData:
	if entry[ 3 ] > high:
		high = entry[ 3 ];
	if entry[ 2 ] < 2e7 and str( entry[ 2 ] )[ 4: ] == '1213':
		histValues.append( entry[ 3 ] / 10.0 );

longDate = str( longDate );
print( 'Hoogste temperatuur: %.1f' % ( high / 10.0 ) );
print( 'Laagste temperatuur: %.1f' % ( low / 10.0 ) );
print( 'Langste periode aaneensluitend gevroren is %d dagen vanaf %s-%s-%s' % ( longest, longDate[ :4 ], longDate[ 4:6 ], longDate[ -2: ] ) );

plt.hist( histValues );
plt.xlabel( 'Temperature ($\degree$C)' );
plt.ylabel( 'Days (count)' );
plt.show();