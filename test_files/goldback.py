'''
	
	goldback.py
	Goldbach conjecture demonstration
		
	(c) 2014 - Pablo Kebees (10907858)
	http://blobtech.nl/
	
'''

limit = 100;
columns = False;

limitLen = len( str( limit ) );
if columns == False: # fit maximum columns in 80 width terminal
	columns = int( 80 / ( limitLen * 3 + 6 + 3 ) );

def not_prime( i ):
	n = 2;
	while n ** 2 <= i:
		if i % n == 0:
			return True;
		
		n += 1;
	
	return False;

def pad( i ):
	global limitLen;
	i = str( i );
	return ' ' * ( limitLen - len( i ) ) + i;
	
out = '';
count = 0;
for i in range( 4, limit + 1, 2 ):
	n = 2;	
	while not_prime( n ) or not_prime( i - n ):
		n += 1;
	
	out += pad( i ) + ' = ' + pad( n ) + ' + ' + pad( i - n );
	count += 1;
	
	if( count == columns ):
		out += '\n';
		count = 0;
	else:
		out +=  ' | ';

print( out );