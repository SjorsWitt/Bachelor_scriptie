# Luc Van Cleef
# goldbach.py
# 11-09-2014

print '************************************* Opgave 3 ************************************'
even_numbers = range(-2,1000,2)

possible_prime_numbers = range(2,1000) 
prime_numbers =[]           
prime = True

for number in possible_prime_numbers:
    n = int(number**0.5+1)               
    for possible_divisor in range(2,n):  
        if number%possible_divisor==0:   
            prime = False
            break
        else:
            prime = True
    if prime == True:
        prime_numbers.append(number) 
prime_numbers.reverse()                                             # draait de lijst van gevonden priemgetallen om zodat de eerste waarde het grootste priemgetal is


for number in even_numbers:
    for prime_number in prime_numbers:
        if number - prime_number > 1:                               # Probeert om het grootst mogelijke priemgetal van het nummer 'number' af te trekken
            print prime_number,'+',number-prime_number,'=',number   
            break
print '************************************* Opgave 4 ************************************'


getal_A = 0
getal_B = 0

for getal in range (220,1300):
    for deler_a in range(1,int(getal/2+1)):
        if getal%deler_a==0:                                       # controleert door welke delers het getal 'getal' te delen is
            getal_A = getal_A + deler_a                            # telt alle gevonden delers bij elkaar op en slaat deze waarde op in getal_A
        if deler_a==int(getal/2): 
            for deler_b in range(1,int(getal_A/2+1)):
                if getal_A%deler_b==0:                             # controleert door welke delers getal_A te delen is
                    getal_B = getal_B + deler_b                    # telt alle gevonden delers bij elkaar op en slaat deze waarde op in getal_B
            if getal_B == getal and getal != getal_A and getal_A > getal:    # controleert of de twee gevonden getallen, verschillende getallen zijn en of zij bevriende getallen zijn
                print getal,'en',getal_A,'zijn bevriende getallen'
                getal_A = 0          
                B = 0
            else:
                getal_A = 0
                getal_B = 0