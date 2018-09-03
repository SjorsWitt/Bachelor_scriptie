import math

'''
Maakt een woordenboek door het eerste digit uit de lijst als key te maken.
'''
list = [45, 90, 30, 33, 34, 64, 34, 28, 72, 20]
def sort_by_digit(n):
    d = dict()
    for i in n:
        
        sec_digit = i % 10 # rest getal vinden
        if sec_digit not in d:
            d[sec_digit] = [i]
        else:
            d[sec_digit].append(i)
    return d

# opgave 3.3
# bepaling of twee ballen botsen door de afstand te vergelijken met de som
# van radius
def ball_collide(a, b):
    x1 = a[0]
    x2 = b[0]
    y1 = a[1]
    y2 = b[1]
    
    afstand = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2)
    som_radius = a[2] + b[2]
    if afstand <= som_radius:
        return "They are colliding"
    else:
        return "They are not colliding"   
    
bal_A = (2, 3, 1)
bal_B = (8, 5, 3)
print ball_collide(bal_A, bal_B)

# opgave 3.4
# kijkt wanneer de snelheden moet worden omgedraaid, dus bij de randen
# van de doos
def ball_step(a, b):
    start_x = a[0]
    start_y = a[1]
    vx = a[2]
    vy = a[3]

    new_x = (vx * b) + start_x
    new_y = (vy * b) + start_y

    x_min = 0
    x_max = 10
    y_min = 0
    y_max = 10

    if new_x >= x_max:
        vx = -vx
    if new_x <= x_min:
        vx = -vx
    if new_y >= y_max:
        vy = -vy
    if new_y <= y_min:
        vy = -vy

    return (new_x, new_y, vx, vy)

print "Ball's new position:", ball_step((5, 5, 2, 1), 0.01)
