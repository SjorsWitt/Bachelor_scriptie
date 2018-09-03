# Luc Van Cleef
# homework3.py
# 30-sep-2014



import random as rnd
import math

def sort_by_digit(list_of_numbers):
    
    sorted_list = {}
    
    # doorloop alle nummers in de opgegeven lijst
    for number in list_of_numbers:
        for rest in range(10):
            
            # checkt wat de rest is bij een deling door 10 (dit is altijd de laatste decimaal), als er nog 
            # geen key is met deze waarde wordt deze aangemaakt en wordt de value als een lijst erin opgeslagen
            if number%10 == rest not in sorted_list:
                sorted_list[rest] = [number]
            
            elif number%10 == rest in sorted_list:
                sorted_list[rest].append(number)
    return sorted_list    
                


def chart(list_of_numbers):
    lijst = sort_by_digit(list_of_numbers)
    for i in lijst:
        print i, len(lijst[i])*'#'


def test_chart():
    input_1 = []
    input_2 = []
    input_3 = []
    
    # creert 3 lijsten van een random lengte met daarin random integers
    for i in range(rnd.randint(25,75)):
         input_1.append(rnd.randint(1,2000))   
    for i in range(rnd.randint(1,25)):
         input_2.append(rnd.randint(1,2000))     
    for i in range(rnd.randint(1,25)):
         input_3.append(rnd.randint(1,2000))     
    
    output_1 = chart(input_1)
    output_2 = chart(input_2)
    output_3 = chart(input_3)
    
    return output_1
    return output_2
    return output_3

test_chart()

print ''
print '***************************************** opgave 3.3 *************************'
print ''

def ball_colide(ball_1,ball_2):
    
    # berekent met behulp van de stelling van pythagoras de afstand tussen de de middelpunten van de cirkels
    distance = math.sqrt((ball_1[0]-ball_2[0])**2+(ball_1[1]-ball_2[1])**2)
    
    # kijkt of de afstand tussen de twee middelpunt groter is dan de som van beide radiussen, als dat het geval is raken de cirkels elkaar niet.
    # als dat wel het geval is raken de 2 elkaar dus wel.
    
    colide = distance - abs(ball_1[2]) - abs(ball_2[2])
    is_colide = True
    if colide > 0:
        is_colide = False
    else:
        is_colide == True
    return is_colide
    
print 'If ball 1 with a radius of 4 is at x = 2, y = 1 and ball 2 with a radius of 3 is at x = 1, y = 2. Collision is:',ball_colide((2,1,4),(1,2,3))
print 'If ball 1 with a radius of 5 is at x = 45, y = 68 and ball 2 with a radius of 6 is at x = 2, y = 3. Collision is:',ball_colide((45,68,5),(2,3,6))
print 'If ball 1 with a radius of 3 is at x = -4, y = -4 and ball 2 with a radius of 3 is at x = 0, y = 0. Collision is:',ball_colide((-4,-4,3),(0,0,3))

print ''
print '***************************************** opgave 3.4 *************************'
print ''

def ball_step(ball_parameters,dt):
    
    # genereert 4 variabelen uit de ingevoerde tuple
    x_position = ball_parameters[0]
    x_velocity = ball_parameters[2]
    y_position = ball_parameters[1]
    y_velocity = ball_parameters[3]
    
    # berekent de nieuwe coordinaat van het deeltje                        
    x_position_new = x_position + dt * x_velocity
    y_position_new = y_position + dt * y_velocity
    
    # zorgt ervoor dat als de nieuwe coordinaten van het deeltje buiten de muren ligt (x > 10 en y > 10) de snelheid wordt omgedraait en er berekent wordt hoe ver
    # het deeltje terug stuitert.
    if x_position_new >= 10:
        x_velocity = -x_velocity
        x_position_new = 10 - (x_position_new - 10)
    if y_position_new >= 10:
        y_velocity = -y_velocity 
        y_position_new = 10 - (y_position_new - 10)  
    
    # Hetzelfde als hierboven, maar dan voor waardes x < 0 en y < 0
    if x_position_new <= 0:
        x_velocity = -x_velocity
        x_position_new = -x_position_new
    if y_position_new <= 0:
        y_velocity = -y_velocity 
        y_position_new = -y_position_new
    
    # maakt een tuple aan met de nieuwe parameters
    ball_parameters_new = (x_position_new,y_position_new,x_velocity,y_velocity)
    return ball_parameters_new
    

def ball_move(ball_parameters,t,dt):
    
    # zorgt dat er een NameError gereturned wordt als de startcoordinaten buiten de toegestande waarde liggen
    if ball_parameters[0] < 0 or ball_parameters[0] >10 or ball_parameters[1] <0 or ball_parameters[1] > 10:
       raise NameError("Error: You've entered an invalid parameter")

    # maakt een nieuwe tuple aan met de ingevoerde parameters van de bal
    new_parameters = ball_parameters
    
    # loopt over de waardes in t heen en berekent voor elke stap de nieuwe coordinaten van de bal
    for delta_t in range(t):
        new_parameters = ball_step(new_parameters,dt)
    return new_parameters

print ball_move((2,3,1,-2),5,1)
print ball_move((5,8,1,-3),1008,1)
print ball_move((7,2,4,-4),5,3)
print ball_move((10,10,1,2),10,3)
print ball_move((4,-1,1,-2),5,1)
