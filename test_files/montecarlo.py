#################################### #
#                           ######  #
## Abel Oakley ##################  # 
#                           ####  # 
## 10653333 ###################  # 
#                           ####  # 
## Monte Carlo ##################  # 
#                           ######  # 
###################################  #

import math

import numpy

import random

import matplotlib.pyplot as plt


# Functie: integraal van x^2
def x2(x):
    return x**x
    
# Functie: integraal van sin(x)
def sin(x):
    return math.sin(x)
    
#Functie: integraal van sin(x^2)
def sin2(x):
    return math.sin(x**2)

# Functie: Monte Carlo integraal
def integral_monteCarlo(a,b,f): 
    
    # De integraalregio definieren met een box door middel van xmin, xmax,
    # ymin en ymax te bepalen. 
    xmin = a
    xmax = b 
    ymin = f(a)
    ymax = f(a)
    for i in numpy.arange(a, b, 0.01):
        if f(i) > ymax:
            ymax = f(i)
        if f(i) < ymin:
            ymin = f(i)
            
    if ymin > 0:
        ymin = 0
        



    # Tellers aanmaken voor aantal random getallen dat binnen of buiten
    # de functie valt.                  
    fout = 0
    goed = 0
    t = 0
    
    # Loop die random getallen aanmaakt en kijkt of deze binnen of buiten 
    # de functie vallen. Hoe groter het getal hou nauwkeuriger de berekening. 
    while t <= 10000:
        randomx = random.random() * (xmax - xmin) + xmin
        randomy = random.random() * (ymax - ymin) + ymin
        if f(randomx) >= 0 and randomy > 0:
            if randomy < f(randomx):
                goed += 1.0
            if randomy > f(randomx):
                fout += 1.0
        if f(randomx) <= 0 and randomy < 0:
            if randomy > f(randomx):
                goed -= 1.0
            if randomy < f(randomx):
                fout += 1.0
        if f(randomx) < 0 and randomy > 0:
            fout += 1.0
        if f(randomx) > 0 and randomy < 0:
            fout += 1.0
        t += 1 
        
    # De integraal is de fractie punten die binnen de frafiek vallen keer
    # de oppervlakte van de totale box. 
    integraal = (((goed)/(goed + fout)) * (xmax - xmin) * (ymax - ymin))
    return integraal

def test_monteCarlo():        
    print "De primitieve is:", integral_monteCarlo(0, 1.0, x2)
    print "De primitieve is:", integral_monteCarlo (0.1, 2.0, sin) 
    print "De primitieve is:", integral_monteCarlo (0, math.pi, sin2) 
test_monteCarlo()

