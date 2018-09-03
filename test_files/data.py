# -*- coding: utf-8 -*-
# Joris Wang
# 5679699
# datum, versie
import matplotlib.pyplot as plt
min_temps = []
max_temps = []
freezing_periods = []

def read_file(filename, outputlist):
    """Leest een file en bewaart de data en temperatuur in een lijst as tuples."""
    temps = open(filename)

    for i in range(21): # Om de header over te slaan.
        temps.next()
    
    for line in temps:
        staid, souid, date, tn, q_tn = line.split(",")
        # Datum en temperatuur bewaard als tuple, zodat deze functie voor elke file afzonderlijk zou werken.
        outputlist.append((int(date), float(tn)/10))
    temps.close()

def lowest_temp():
    """Returnt de laagste temperatuur en bijbehorend datum."""
    min_temp = 100
    coldest_day = 0
    for i in range(len(min_temps)):
        # [0] = datum, [1] = temperatuur
        if min_temps[i][1] <= min_temp and min_temps[i][0] < 20000000:
            min_temp = min_temps[i][1]
            coldest_day = str(min_temps[i][0])
    return 'lowest temperature:', min_temp, 'year:', coldest_day[:4], 'month:', coldest_day[4:6], 'day:', coldest_day[6:8]

def highest_temp():
    """Returnt de hoogste temperatuur en bijbehorend datum."""
    max_temp = -100
    hottest_day = 0
    for i in range(len(max_temps)):
        # [0] = datum, [1] = temperatuur
        if max_temps[i][1] >= max_temp and max_temps[i][0] < 20000000:
            max_temp = max_temps[i][1]
            hottest_day = str(max_temps[i][0])
    return 'highest temperature:', max_temp, hottest_day[:4], 'month:', hottest_day[4:6], 'day:', hottest_day[6:8]

def coldest_period():
    """Maakt een lijst van de duur van alle vriesperiodes."""
    period_length = 0
    melting_day = 0
    del freezing_periods[:]
    for i in range(len(max_temps)):
        if max_temps[i][1] < 0:
            period_length += 1
            melting_day = 0
        elif melting_day < 1:
            # [i-1], omdat de periode pas een index later wordt bewaard.
            freezing_periods.append((max_temps[i-1][0], period_length))
            melting_day += 1
            period_length = 0

def coldest_period2():
    """Maakt een lijst met de duur van alle vriesperiodes en data met één uitzonderingsdag."""
    period_length = 0
    melting_day = 0
    grace_day = 0
    del freezing_periods[:]
    for i in range(len(max_temps)):
        if max_temps[i][1] < 0:
            period_length += 1
            melting_day = 0
        elif period_length > 0 and grace_day < 1:
            period_length += 1
            grace_day += 1
        elif melting_day < 1:
            freezing_periods.append((max_temps[i-1][0], period_length))
            melting_day += 1
            grace_day = 0
            period_length = 0

def longest_period(inputfunction):
    """"Roept coldest_period of coldest_period2 aan en haalt uit de gecreëerde lijst de langste vriesperiode."""
    period = 0
    inputfunction
    for i in range(len(freezing_periods)):
        # = 0 = datum, [1] = temperatuur
        if freezing_periods[i][1] > period:
            period = freezing_periods[i][1]
            date = str(freezing_periods[i][0])
    return 'longest period:', period, 'year:', date[:4], 'month:', date[4:6], 'day:', date[6:8]

def birthday_list():
    """Returnt een lijst met de maximale temperatuur op elke 13 december tot het jaar 2000."""
    birth_temps = []
    for i in range(len(max_temps)):
        # [0] = datum, [1] = temperatuur
        if max_temps[i][0] % 10000 == 1213 and max_temps[i][0] < 20000000:
            birth_temps.append(max_temps[i][1])
    return birth_temps

def plot_birthday(inputlist): 
    """Roept birthday_list aan om een histrogram te plotten.""" 
    plt.hist(inputlist, bins = 16)
    plt.title("Temperatures on Martijns' birthday ;-)")
    plt.xlabel('Temperature in Celcius')
    plt.ylabel('Frequency')
    plt.show()
        
read_file('TN_STAID000162.txt', min_temps)
read_file('TX_STAID000162.txt', max_temps)

print '1a'

print lowest_temp()
print highest_temp()

print '1b'
print longest_period(coldest_period())

print '1b hacker edition'
print longest_period(coldest_period2())

plot_birthday(birthday_list())



