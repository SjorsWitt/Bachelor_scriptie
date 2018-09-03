# Name: Kevin Haver
# Section: D
# Date: 15 oktober 2014
# hacker.py

# Opdracht 1.b hacker edition

def langst_gevroren_hacker(filename):
    '''
    Bepaalt de langste periode dat het gevroren heeft.
    '''
    input_filehandle = open(filename, 'r')
    for i in range (21):        # Eerste 21 regels overslaan (dat is tekst):
       line = input_filehandle.next()
    
    dagen_gevroren = 0
    max_dagen_gevroren = 0
    dag_boven_nul = 0
    
    for line in input_filehandle:
        elementen = line.split()
        element1 = elementen[1]
        element2 = elementen[2]
        jaar = int(element1[-9:-5])
        maand = element1[-5:-3]
        dag = element1[-3:-1]
        
        max_temp = float(element2[:-1])/10
        if max_temp < 0:
            dagen_gevroren += 1
            if dagen_gevroren > max_dagen_gevroren:
                max_dagen_gevroren = dagen_gevroren
                eindigt = dag, maand, jaar
        if max_temp >= 0:
            if dag_boven_nul == 0:      # Het aantal dagen boven 0 mag maximaal                   
                dagen_gevroren += 1     # 1 zijn, anders begint de teller
                dag_boven_nul = 1       # weer opnieuw
            elif dag_boven_nul == 1:
                dagen_gevroren = 0
                dag_boven_nul = 0
                
    input_filehandle.close()

    
    print "\nLangste periode dat het heeft gevroren met maximaal 1 dag boven",\
          "\nnul duurde ", max_dagen_gevroren, "dagen en eindigde op",\
          zeller(eindigt[0], eindigt[1], eindigt[2]), eindigt[0], "-", \
          eindigt[1], "-", eindigt[2]
    return " "

def zeller(dag, maand, jaar):
    '''
    Berekent op welke dag van de week een datum valt
    '''
    jaar_str = str(jaar) # Eerst van jaar een string maken, zodat het 
    A = int(maand)-2     # opgesplitst kan worden
    B = int(dag)
    C = int(jaar_str[2:4]) # Jaar
    D = int(jaar_str[0:2])  # Eeuw
    if A <= 0:
        A += 12
        C -= 1

    W = (13*A - 1) / 5
    X = C / 4
    Y = D / 4
    Z = W + X + Y + B + C - 2*D
    R = Z % 7

    if R == 0:
        return 'zondag'
    if R == 1:
        return 'maandag'
    if R == 2:
        return 'dinsdag'
    if R == 3:
        return 'woensdag'
    if R == 4:
        return 'donderdag'
    if R == 5:
        return 'vrijdag'
    if R == 6:
        return 'zaterdag'

# ---------- Main ------------

print "hacker:"
print langst_gevroren_hacker('TX_STAID000162.txt')
