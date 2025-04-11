from random import*
import os
import threading
import time

################################       Color definition            #######################################

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[95m"
gray = "\033[61m"
default = "\033[0m"  # Reset style

#################################    Dictionary definition        ###############################################

Inventory = {
    "Equipement" : [None, None, None], #### Equipement : (sword, armor, shield) (equiped on)
    "Items" : []
}

Player_stat = {
    "PV" : 100,
    "Base_domage" : 10,
    "Multiplicateur de dégat" : 10,
    "Inventaire" : Inventory,
    "Reduction de dégat" : 0,
    "Biome actuel": "foret"
}

Monsters = {  #### Value matching : (Difficuly, min dommage, max dommage, health)
    "Goule des Brumes" : ["Facile", 6, 12, 20],
    "Ombre Rampante" : ["Facile", 3, 9, 25],
    "Troll des Cavernes" : ["Facile", 2, 5, 30],
    "Lycan Sombre" : ["Facile", 10, 15, 15],
    "Cyclope Rugissant" : ["Moyen", 13, 17, 25],
    }

Armor = { #### Value matching : (Protection, Drop rate)
    "Armure Commune" : [0.20, 0.25],
}

Weapons = { #### Value matching : (Dommage, attack speed, Rarity, Drop rate)
    "Lame du Vent" : [5, 1, "Commun"],
    "Arc Éthéré" : [2, 1.5, "Commun"],
    "Anneau des Âmes" : [7, 1.5, "Rare"],
}

Bioms = {  ## 4 bioms, and the mob/ loot/ ressources/ difficulty we can find in each maps
    'Forêt' : {
        'Mob' : ["Goule des Brumes", "Ombre Rampante", "Troll des Cavernes", "Lycan Sombre", "Cyclope Rugissant"],
        'Loot' : ["Lame du Vent", "Arc Éthéré", "Anneau des Âmes", "Armure Commune", "Potion de soin"],
        'Ressources' : ["Poudre d'Étoiles", "Cristal Lunaire", "Éclat de Roche Magmatique"],
        'Difficulter' : 1
    },
}

#################################    map definition        ################################################

### 10 x 10 map
map_forest = []

#################################    Variable definition        ################################################

loop = False #main program loop

#curent possition on the player in the map
player_X = 4
player_Y = 9

#2 previous position of the player (usefull to come back)
last_location = [",",","]

#previous direction of the deplacment (usefull to come back)
last_D = "D"

#################################    fonctions definition        ################################################

### Display map in terminal
def Display_map (map_dis):
    for i in map_dis :
        lign = ''
        for y in i:
            if y == ',' or y == "'" : 
                lign += f"{green} {y} {default}" # Apply some color to the elements of the map
            elif y == 'X' : 
                lign += f"{gray} {y} {default}"
            elif y == '/' : 
                lign += f"{purple} {y} {default}"
            elif y == '@': 
                lign += f"{red} {y} {default}"
        print (lign)

### Moove in the map (forward)
def Forward (map, posX, posY, posA):
    os.system('cls' if os.name == 'nt' else 'clear')
    if map[posY-1][posX] != "X":
        map[posY][posX], posA[0] = posA[0], map[posY-1][posX] #move the player in the array
        posA[1] = posA[0] #refresh the 2 last deplacment
        map[posY-1][posX] = "@"
        posY -= 1
    return (map, posX, posY, posA)

### Moove in the map (Left)
def Left (map, posX, posY, posA):
    os.system('cls' if os.name == 'nt' else 'clear')
    if map[posY][posX-1] != "X":
        map[posY][posX], posA[0] = posA[0], map[posY][posX-1]
        posA[1] = posA[0]
        map[posY][posX-1] = "@"
        posX -= 1
    return (map, posX, posY, posA)

### Moove in the map (Backward)
def Backward (map, posX, posY, posA):
    os.system('cls' if os.name == 'nt' else 'clear')
    if map[posY+1][posX] != "X":
        map[posY][posX], posA[0] = posA[0], map[posY+1][posX]
        posA[1] = posA[0]
        map[posY+1][posX] = "@"
        posY +=1
    return (map, posX, posY, posA)

### Moove in the map (Right)
def Right (map, posX, posY, posA):
    os.system('cls' if os.name == 'nt' else 'clear')
    if map[posY][posX+1] != "X":
        map[posY][posX], posA[0] = posA[0], map[posY][posX+1]
        posA[1] = posA[0]
        map[posY][posX+1] = "@"
        posX += 1
    return (map, posX, posY, posA)

### Display the player inventory and equip equipments
def Display_inventory ():
    #display the inventory of the player
    Dis_inv = []
    Dis_equip = Inventory["Equipement"]
    Dis_item = Inventory["Items"]
    print ("Pour équiper une armure ou une arme, saisissez le 'N°' de l'objet\nSinon, pressez entrer pour quitter\n")
    for elem in Inventory :
        Dis_inv.append(elem)
    print ("Equipement équiper :")
    if Dis_equip[0] == None :
        print ("Arme : Aucune")
    else :
        print (f"Arme : {Dis_equip[0]}")
    if Dis_equip[1] == None :
        print ("Armure : Aucune")
    else :
        print (f"Arme : {Dis_equip[1]}")
    if Dis_equip[2] == None :
        print ("Bouclier : Aucun")
    else :
        print (f"Arme : {Dis_equip[2]}")
    print("Items :")
    if Dis_item == [] :
        print ("Inventaire Vide")
    else :
        for i in range (len(Dis_item)):
            print (f"{i+1} - {Dis_item[i]}")
 
    #Equip some stuff
    choix = input("-->")
    if choix != "":
        try:
            verif = False
            if Dis_item[int(choix)-1] in Weapons: #Verify that the selected item is a weapon
                Inventory["Equipement"][0] = Dis_item[int(choix)-1]
                Player_stat["Multiplicateur de dégat"] = Player_stat["Base_domage"] + Weapons[Dis_item[int(choix)-1]][0]
                verif = True
                print ("Equiper !!")
            elif Dis_item[int(choix)-1] in Armor: #Verify that the selected item is an armor
                Inventory["Equipement"][1] = Dis_item[int(choix)-1]
                Player_stat["Reduction de dégat"] = Armor[Dis_item[int(choix)-1]][0]
                verif = True
                print ("Equiper !!")
            elif verif == False:
                print("Vous ne pouvez pas équipez cet objet")
            time.sleep(1)
        except:
            print ("Saisie invalide")

    os.system('cls' if os.name == 'nt' else 'clear') #clear the shell
    Display_map (map_forest) ## Refresh map

def map_generation (x, y): ## Random map generation
    map_tmp = []
    for i in range (10):
        map2_tmp = []
        for z in range (10):
            if z == x and i == y:
                map2_tmp.append("@")
            else : #the different item in the map generate randomly
                seed = randint(1, 7)
                if seed == 2 or seed == 4 or seed == 6 :
                    map2_tmp.append(",")
                elif seed == 1 or seed == 5 :
                    map2_tmp.append("'")
                elif seed == 3 :
                    map2_tmp.append("X")
                elif seed == 7 :
                    map2_tmp.append("/")
        map_tmp.append(map2_tmp)
    return (map_tmp)

## interaction between player and event
def interaction (posA) :
    if posA[0] == "/": #Verify that the player is in a event
        count = 0
        if Player_stat["Biome actuel"] == "foret" : # verify he is in the correct biom
            Random_Monster = randint(0, 4) # chose a random monster to fight
            for i in Monsters :
                if count == Random_Monster :
                    for elem in Bioms["Forêt"]["Mob"] :
                        if elem == i :
                            load_pv = Monsters[elem][3]
                            load_domage = randint(Monsters[elem][1], Monsters[elem][2])
                            print (elem,"vous attaque!!\n\n",elem,":\n________________________\n  HP :", load_pv,"   Dégat :", load_domage,"\n\n\nVous :\n________________________\n HP :", Player_stat["PV"], "   Dégat de base :", Player_stat["Multiplicateur de dégat"]) #Display information
                            print ("\nAppuyer sur 'E' le plus de fois possible pour faire plus de dégâts. (les attaques s'enchaînent, il faut être réactif)")
                            start_loop = False 
                            while start_loop == False :
                                start = input("Ready? (Y/N)\n-->")
                                if start.upper() == "Y" :
                                    while load_pv > 0 and Player_stat["PV"] > 0: 
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        print ("\n\n",elem,":\n________________________\n  HP :", load_pv,"   Dégat :", load_domage,"\n\n\nVous :\n________________________\n HP :", Player_stat["PV"], "   Dégat de base :", Player_stat["Multiplicateur de dégat"])#Display information
                                        #allow 5s to the player to press the attack button as much as he can
                                        t = threading.Timer(5, lambda: print("\nAppuiez sur 'enter' pour valider"))
                                        t.start()
                                        attack = input("Attaquez !!\n-->")
                                        t.cancel()
                                        if load_pv > ((len(attack)/20)*Player_stat["Multiplicateur de dégat"]) :
                                            Player_stat["PV"] -= round(load_domage - (load_domage * Player_stat["Reduction de dégat"]), 2)
                                            print ("Dégat donner :", round(((len(attack)/20)*Player_stat["Multiplicateur de dégat"]), 2),"Dégat reçu :", round(load_domage - (load_domage * Player_stat["Reduction de dégat"]), 2))
                                        else:
                                            print ("Dégat donner :", round(((len(attack)/20)*Player_stat["Multiplicateur de dégat"]), 2))
                                        load_pv -= (len(attack)/20)*Player_stat["Multiplicateur de dégat"]
                                        time.sleep(5)

                                    
                                    if Player_stat["PV"] > 0: #win the fight
                                        print ("Monstre vaincu !!\nBien jouer\n\n",elem,":\n________________________\n  HP :", 0,"   Dégât :", load_domage,"\n\n\nVous :\n________________________\n HP :", Player_stat["PV"], "   Dégât de base :", Player_stat["Multiplicateur de dégat"])#Display information
                                        time.sleep(5)
                                        loot()
                                    else: #loose the fight
                                        print ("Woimp.. Woimp.. Woimp.. !!\nTout ne s'est pas passé comme prévu\n\n",elem,":\n________________________\n  HP :", 0,"   Dégât :", load_domage,"\n\n\nVous :\n________________________\n HP :", 0, "   Dégât de base :", Player_stat["Multiplicateur de dégat"])#Display information
                                        start_loop = True
                                        return (False, posA)
                                    time.sleep(5)
                                    posA[0] = "'"
                                    return (True, posA, " ")

                                elif start.upper() == "N" : # To return at the last location
                                    start_loop = True
                                    return (True, posA, "Leave")
                                    

                                else :
                                    print ("erreur de saisie")
                count += 1 

## give the loot to the player
def loot(): # give some random loot to the player
    if Player_stat["Biome actuel"] == "foret" :
        equip = randint(0,4)
        item = randint (0,2)
        Inventory["Items"].append(Bioms["Forêt"]["Loot"][equip])
        Inventory["Items"].append(Bioms["Forêt"]["Ressources"][item])
        os.system('cls' if os.name == 'nt' else 'clear')
        print ("vous avez trouver :",Bioms["Forêt"]["Loot"][equip],"et",Bioms["Forêt"]["Ressources"][item])

## Display the player stat
def Display_stat (): #Display the player stat
    for i in Player_stat:
        if i != "Inventaire" :
            print (i,":", Player_stat[i])

## Check if the player win
def win_check (): # If the player beat all the monster, the game stop and he win
    check = True
    for i in map_forest:
        for y in i:
            if y == '/': # if there still 1 "/" son he don't win yet
                check = False
    return check


#################################    Main Programme        ################################################
# Starting display
print(f"""
{red}________________________________________________________________________________________________________________________________________{default}

Salutation jeune aventurier, avant de commencer je t'invite à lire le README qui peut être utile, de plus la touche 'help' est disponible.

        Votre mission, si vous l'acceptez, sera de vaincre tous les monstres et de rétablir le pays dans cette plaisante forêt !
    Pour rencontrer des monstres, il faut se déplacer sur les "/" et appuyer sur E pour interagir. Les "X" représentent de vulgaires cailloux.
        

{red}________________________________________________________________________________________________________________________________________{default}

""")

for i in range (3):
    time.sleep(1)
    print("croutch...")
time.sleep(1)
print("Tu arrives dans une forêt !")
time.sleep(2)


map_forest = map_generation(player_X, player_Y) # generation of the map

Display_map (map_forest) # display the map

while loop == False :
    choice = input("-->")
    if choice.upper() == "Z" or choice.upper() == "Q" or choice.upper() == "S" or choice.upper() == "D" : ## Test the input to moove in the map
        if choice.upper() == "Z": ## Moove forward
            if player_Y-1 != -1:
                map_forest, player_X, player_Y, last_location = Forward (map_forest, player_X, player_Y, last_location) 
                last_D="F"
            else :
                print ("Un mur géant !!!!, tu ne peux pas le traverser")

        elif choice.upper() == "Q": ## Moove left
            if player_X-1 != -1:     
                map_forest, player_X, player_Y, last_location = Left (map_forest, player_X, player_Y, last_location)
                last_D="L"
            else :
                print ("Un mur géant !!!!, tu ne peux pas le traverser")

        elif choice.upper() == "S": ## moove backward
            if player_Y+1 != 10:
                map_forest, player_X, player_Y, last_location = Backward (map_forest, player_X, player_Y, last_location)
                last_D="B"
            else :
                print ("Un mur géant !!!!, tu ne peux pas le traverser")

        elif choice.upper() == "D": ## moove right
            if player_X+1 != 10:
                map_forest, player_X, player_Y, last_location = Right (map_forest, player_X, player_Y, last_location)
                last_D="R"
            else :
                print ("Un mur géant !!!!, tu ne peux pas le traverser")
        Display_map (map_forest) ## Refresh map after mooving
        

    elif choice.upper() == "E" : ## start combat with an random monster
        result = interaction(last_location)
        try:
            if  result[0] == True:
                if result[2] == "Leave": # if the player leave a fight he is put at his previous location (before enter in the event)
                    if last_D == "F": map_forest, player_X, player_Y, last_location = Backward (map_forest, player_X, player_Y, last_location) 
                    elif last_D == "B": map_forest, player_X, player_Y, last_location = Forward (map_forest, player_X, player_Y, last_location)
                    elif last_D == "R" : map_forest, player_X, player_Y, last_location = Left (map_forest, player_X, player_Y, last_location)
                    elif last_D == "L" : map_forest, player_X, player_Y, last_location = Right (map_forest, player_X, player_Y, last_location)
                    last_location[0] = last_location[1] #refresh the last location item
                else:
                    last_location = result[1]
                Display_map(map_forest)
                if win_check() == True : #Win display
                    print("""
                    

                    Quelle puissance !! Vous avez réussi à vaincre tous les monstres !

                                    Vous avez gagné, Bien joué !!!!
                    
                    """)
                    loop = True
            elif result[0] == False : #Loose diplay
                loop = True
                print ("""
                    
                    Vous avez été vaincu par un monstre maléfique !
                    
                                        Game Over !
                    """)
        except:
            print("\nIl n'y à rien à faire ici...\n")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
            Display_map(map_forest)

    elif choice.upper() == "A": ## Display the player statistic
        Display_stat()

    elif choice.upper() == "I" :
        Display_inventory() ## Display the player inventory

    elif choice.upper() == "R":
        os.system('cls' if os.name == 'nt' else 'clear')
        Display_map (map_forest) ## Refresh map

    elif choice.upper() == "HELP" : ## Display some usefull information about the game mechanics
        print ("Pour ce déplacer :\n- Avancer : z\n- Gauche : q\n- Reculer : s\n- Droite : d\nPour intéragire : E\nPour voir l'inventaire : i\nPour actualiser la map : r\nPour afficher les statistiques du joueur : a\nPour quitter : esc")

    elif choice.upper() == "ESC": ## Can leave the game
        loop = True
    
    else :
        print ("Saisie invalide")




###### 262 lign of code / 300 #######

