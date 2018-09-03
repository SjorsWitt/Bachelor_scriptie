def langste_vries_periode_met_1_moment_dooi(opened_file):
    """
    @return: de langste periode  waarin de maximale temperatuur onder nul is gebleven,\
    maar het wel 1 dag heeft mogen dooien in De Bilt  
    @param: opened_file is het eerder geopende bestand waarvoor de functie wordt uitgevoerd   
    """
    # benodigde tellers
    vriesperiode = 0 
    dooiperiode = 0 
    langste_vriesperiode = 0
    
    # De eerste 21 regels moeten worden overgeslagen om bij de data in het bestand aan te komen
    for i in range(21):
       opened_file.next()
    
    for line in opened_file:
        # deelt de data op in strings, zodat temperatuur en datum als afzonderlijke elementen worden gezien 
        regel = line.split(",")
        
        #Zodra de maximum temperatuur onder 0 komt begint de teller en wordt deze opgeslagen\
        # wanneer deze langer is dan de eerder opgeslagen langste periode waarin het heeft gevroren
        if int(regel[3]) < 0: 
            vriesperiode += 1
            if vriesperiode > langste_vriesperiode: 
                langste_vriesperiode = vriesperiode
                datum = int(regel[2])
        else:
            # De temperatuur mag 1 dag boven 0 komen en de teller dooiperiode begint dan met tellen
            dooiperiode += 1
            vriesperiode += 1
            
            # zodra het langer dan 1 dag dooit/de temperatuur boven 0 komt, worden de dooiperiode\
            # en vriesperiode counter opnieuw op 0 gezet
            if dooiperiode > 1: 
                vriesperiode = 0
                dooiperiode = 0
            else:   
                # vriesperiode incl. met 1 dooidag worden opgeslagen als langste_vriesperiode\
                # en bijbehorende datum
                if vriesperiode > langste_vriesperiode:
                    langste_vriesperiode = vriesperiode
                    datum = int(regel[2])
   
    return langste_vriesperiode, datum

