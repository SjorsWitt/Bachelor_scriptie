'''
	
	doos.py
	Continuous Physics Simulation
	
	Particle-particle collisions partially implemented
	but crashes the simulation, so commented out (ln 82)
	
	(c) 2014 - Pablo Kebees (10907858)
	http://blobtech.nl
	
'''
from __future__ import division;
import matplotlib.pyplot as plot
import matplotlib.animation as animation
import math, time, operator, random;

pCount = 20;
container = 2, 1;
velocity = 0.5;
colorLight = 0.7;
FPS = 60;
size = 6;

# random.seed( raw_input( 'Enter seed: ' ) );

class vector:
	def __init__( self, magnitude, angle, polar = False ):
		if polar:
			self.x = math.cos( angle ) * magnitude;
			self.y = math.sin( angle ) * magnitude;
		else:
			self.x = magnitude;
			self.y = angle;
	
	def translate( self, vec ):
		self.x += vec.x;
		self.y += vec.y;
		return self;
	
	def scale( self, mag ):
		self.x *= mag;
		self.y *= mag;
		return self;
	
	def dot( self, vec ):
		self.x *= vec.x;
		self.y *= vec.y;
		return self;
	
	def toTuple( self ):
		return ( self.x, self.y );	
	
	def toStr( self ):
		return str( round( self.x, 4 ) ) + ';' + str( round( self.y, 4 ) );
	
	def copy( self ):
		return vector( self.x, self.y );
	
class particleInstance:
	counter = 0;
	
	def __init__( self, pos, vel, r ):
		self.pos = pos;
		self.vel = vel;
		self.r = r;
		
		self.id = chr( self.counter + 65 );
		particleInstance.counter += 1;
	
	def step( self, time ):
		self.pos.translate( self.vel.copy().scale( time ) );
		
	def debug( self ):
		return '%s pos: %s, vel: %s' % ( self.id, self.pos.toStr(), self.vel.toStr() );
	
def findEvent( particle ):
	global system, queue, container;
	
	### particle collisions
	
	# for target in system:
		# dx = particle.pos.x - target.pos.x;
		# dy = particle.pos.y - target.pos.y;
		# R = particle.r + target.r;
		
		# if dx ** 2 + dy ** 2 <= R ** 2:
			# continue;
		
		# dvx = particle.vel.x - target.vel.x;
		# dvy = particle.vel.y - target.vel.y;
		
		# a = dvx ** 2 + dvy ** 2;
		# b = 2 * ( dy * dvy + dx * dvx );
		# c = dx ** 2 + dy ** 2 - R ** 2;
		# d = b ** 2 - 4 * a * c;
		# if d < 0:
			# continue;
		
		# t = ( -b + d ** 0.5 ) / 2 / a;
		# if t < 0:
			# continue;
		
		# addEvent( t, [ particle, target ], [ vector( -1, -1 ), vector( -1, -1 ) ] );
	
	### boundary collisions
	# sweet one-liners
	timex = ( container[ 0 ] * ( particle.vel.x > 0 ) - particle.pos.x ) / particle.vel.x - particle.r / abs( particle.vel.x );
	timey = ( container[ 1 ] * ( particle.vel.y > 0 ) - particle.pos.y ) / particle.vel.y - particle.r / abs( particle.vel.y );
	addEvent( min( timex, timey ), [ particle ], [ vector( -1, 1 ) if timex < timey else vector( 1, -1 ) ] );
	
	queue.sort( key = lambda i: i[ 'time' ] );

def addEvent( time, particles, vectors ):
	global queue;
	
	particles = set( particles );
	
	for item in queue:
		if particles.intersection( item[ 'targets' ] ):
			if time > item[ 'time' ]:
				item[ 'targets' ].update( particles );
				item[ 'scalars' ] += [ None ] * ( len( item[ 'targets' ] ) - len( item[ 'scalars' ] ) );
				break;
			else:
				particles.update( item[ 'targets' ] );
				vectors += [ None ] * ( len( particles ) - len( vectors ) );
	else:
		queue.append( { 'time': time, 'targets': particles, 'scalars': vectors } );
	
def debug():
	global system, pCount;
	print( '\n'.join( [ particle.debug() for particle in system ] ) );

def init():
	global circles;
	
	for circle in circles:
		circle.center = ( -1000, -1000 );
	
	return circles;

def step( frame ):
	global last, queue, system, line, rec, circles, last;
	
	now = time.time();
	dTime = now - last;
	last = now;
	
	while dTime > 0:	
		next = min( dTime, queue[ 0 ][ 'time' ] );
		dTime -= next;
		
		for particle in system:
			particle.step( next );
		
		for item in queue: # reduce event times
			item[ 'time' ] -= next;
		
		# if ready for next event
		if queue[ 0 ][ 'time' ] <= 1e-15: # stupid floats
			for i, particle in enumerate( queue[ 0 ][ 'targets' ] ):
				if queue[ 0 ][ 'scalars' ][ i ] != None:
					particle.vel.dot( queue[ 0 ][ 'scalars' ][ i ] );
			targets = queue[ 0 ][ 'targets' ]; # remember involved particles
			queue.pop( 0 ); # remove event
			
			for target in targets: # find new events for the particles
				findEvent( target );
	
	for i in xrange( len( circles ) ):
		circles[ i ].center = system[ i ].pos.toTuple();
		circles[ i ].set_radius( system[ i ].r );
	
	return circles;

last = time.time();
figure = plot.figure( figsize = ( container[ 0 ] * size, container[ 1 ] * size ) );
ax = plot.axes( xlim = ( 0, container[ 0 ] ), ylim = ( 0, container[ 1 ] ) );

circles = []
for i in xrange( pCount ):
	circle = plot.Circle( ( 0, 0 ), fc = [ random.random() * colorLight for i in xrange( 3 ) ], ec = 'none' );
	circles.append( circle );
	ax.add_patch( circle );

system = [ particleInstance( vector( 0.25, 0.75 ), vector( velocity, 2 * math.pi * random.random(), True ), min( container ) / 100 * ( random.random() * 2 + 1 ) ) for i in xrange( pCount ) ];
queue = []; 

# Fill the queue for the first time
for particle in system:
	findEvent( particle );

anim = animation.FuncAnimation( figure, step, init_func = init, interval = 1000 / FPS, blit = True );
plot.show();