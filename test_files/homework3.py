#################################### #
#                           ######  #
## Abel Oakley ##################  # 
#                           ####  # 
## 10653333 ###################  # 
#                           ####  # 
## Homework 3 ###################  # 
#                           ######  # 
###################################  #

import math

import numpy

# Functie om getallen te sorteren met behulp van een dictionary
def sort_by_digit(lijst):
    dictionary = dict() # Maakt een dictionary aan
    for i in range(0,10): # Loop tussen de getallen 0 en 9
        listx=[] # Lijst aanmaken die voor elke i reset
        for j in lijst:
            if  j % 10 == i: 
                listx.append(j) # De gevonden item uit de lijst toevoegen

        dictionary[i] = listx # De dictionary gelijkstellen aan list x        
    return dictionary

lijst = [45, 90, 30, 33, 34, 64, 34, 28, 72, 20] # Lijst met getallen  
  
# Functie die een chart aanmaakt voor een gegeven lijst
def chart(dictionary):
    for i in dictionary.keys(): 
        num = len(dictionary[i]) # num staat gelijk aan het de lengte van de lijst op i
        print i, num * '#'# Geeft een chart weer met alle keys tussen 0 en 9

# Test programma voor de chart functie
def test_chart():
    print chart(sort_by_digit(lijst))

      
# Functie om 'ball collisions' te bepalen   
def ball_collisions(x1,x2,y1,y2,r1,r2):
    ball1 = x1, y1, r1 # Tuple aanmaken voor de eerste bal
    ball2 = x2, y2, r2 # Tuple aanmaken voor de tweede bal
    x = ball1[0] - ball2[0] # Delta x tussen de ballen bepalen
    y = ball1[1] - ball2[1] # Delta y tussen de ballen bepalen
    r = ball1[2] + ball2[2] # De twee stralen bij elkaar optellen
    z = math.sqrt(x**2 + y**2) # Pythagoras voor de lengte tussen de ballen
    
    # Kijken of de straal groter is dan de lengte tussen de ballen
    if r > z:
        return "The Balls collide"
    else:
        return "The Balls don't collide"

# Test programma voor de functie ball_collissions
def test_ball_collisions():
     print "The balls should collide:", ball_collisions(0,0,1,2,2,2)
     print "The balls shouldn't collide:", ball_collisions(3,7,4,5,1,2)
     print "The balls should collide:", ball_collisions(7,5,2,4,5,5)
     
# Functie van het berekenen van de stappen van een bal
def ball_step(ball, dt,t):
    # Tuple toewijzen aan variabelen die wel mutable zijn
    x, y, vx, vy = ball
    # Verloop van x,y over dt bepalen
    x += vx * dt
    y += vy * dt
    if x > 10 or x < 0: # Als x boven 10 of onder 0 komt, inverteerd vx en x
        vx *= - 1
        x = - x 
    if y > 10 or y < 0: # Als y boven 10 of onder 0 komt, inverteerd vy en y
        vy *= - 1
        y = - y
    # Tuple aannmaken voor de nieuwe positie van de bal
    ball2 = x, y, vx, vy
    return ball2

# Test programma voor ball_step
def move_ball():
    print ball_step((2, 3, 1, -2), 5, 1)

        
test_chart()
test_ball_collisions()   
move_ball()