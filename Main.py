from random import*
import os
import threading
import time

# git path : c/Users/lucas/OneDrive/Documents/IPI/Initiation_python/Initiation_Python
# os.system('cls' if os.name == 'nt' else 'clear')

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
    "Equipement" : [None, None, None], #### Equipement : (Epée, Armure, Bouclier) (équiper sur le personnage)
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
    "Spectre Sifflant" : ["Moyen", 20, 25, 30],
    "Vampire de Sang Noir" : ["Moyen", 10, 17, 35],
    "Basilic Hypnotique" : ["Moyen", 7, 15, 40],
    "Faucheuse Spectrale" : ["Moyen", 18, 22, 30],
    "Serpent des Flammes" : ["Moyen", 15, 17, 30],
    "Kraken d’Obsidienne" : ["Moyen+", 20, 30, 30],
    "Minotaure Écarlate" : ["Moyen+", 18, 25, 35],
    "Hydre des Abysses" : ["Moyen+", 20, 24, 40],
    "Chaman Sauvage" : ["Dure", 25, 28, 45],
    "Golem d’Ébène" : ["Dure", 23, 26, 50],
    "Salamandre Incandescente" : ["Dure", 20, 30, 40],
    "Wyverne de Givre" : ["Dure", 19, 26, 40],
    "Harpie Chantante" : ["Extreme", 25, 35, 55],
    "Gardien de Cristal" : ["Extreme", 30, 40, 60],
    "Démon Arcanique": ["Extreme", 40, 55, 70]}

Armor = { #### Value matching : (Protection, Drop rate)
    "Armure Commune" : [0.20, 0.25],
    "Armure Rare" : [0.30, 0.20],
    "Armure Epic" : [0.50, 0.15],
    "Armure Legendaire" : [0.70, 0.10],
    "Bouclier Runique" : [0.30, 0.20],
}

Weapons = { #### Value matching : (Dommage, attack speed, Rarity, Drop rate)
    "Lame du Vent" : [5, 1, "Commun"],
    "Arc Éthéré" : [2, 1.5, "Commun"],
    "Anneau des Âmes" : [7, 1.5, "Rare"],
    "Bâton de Lumière" : [10, 1, "Rare"],
    "Amulette de l'Ombre" : [4, 3, "Epic"],
    "Dague Sanguinaire" : [20, 1, "Epic"],
    "Flèche Explosive" : [14, 1.3, "Epic"],
    "Grimoire Perdu" : [30, 0.5, "Legendaire"],
    "Heaume de Fer Noir" : [25, 1, "Legendaire"],
    "Étoile Polaire" : [22, 1.2, "Legendaire"],
    "Épée Sifflante" : [40, 1, "Mythique"],
}

Bioms = {  ## 4 bioms, and the mob/ loot/ ressources/ difficulty we can find in each maps
    'Forêt' : {
        'Mob' : ["Goule des Brumes", "Ombre Rampante", "Troll des Cavernes", "Lycan Sombre", "Cyclope Rugissant"],
        'Loot' : ["Lame du Vent", "Arc Éthéré", "Anneau des Âmes", "Armure Commune", "Potion de soin"],
        'Ressources' : ["Poudre d'Étoiles", "Cristal Lunaire", "Éclat de Roche Magmatique"],
        'Difficulter' : 1
    },
    'Ville' : {
        'Mob' : ["Spectre Sifflant", "Vampire de Sang Noir", "Basilic Hypnotique", "Faucheuse Spectrale", "Serpent des Flammes"],
        'Loot' : ["Bâton de Lumière", "Amulette de l'Ombre", "Bouclier Runique", "Armure Rare", "Potion d'invisibilité"],
        'Ressources' : ["Sève de l’Arbre Ancien", "Épine du Chaos", "Écaille de Dragon Ancien"],
        'Difficulter' : 2
    },
    'Desert' : {
        'Mob' : ["Kraken d’Obsidienne", "Minotaure Écarlate", "Hydre des Abysses", "Chaman Sauvage", "Golem d’Ébène"],
        'Loot' : ["Dague Sanguinaire", "Flèche Explosive", "Grimoire Perdu", "Armure Epic", "Potion de dommge"],
        'Ressources' : ["Minerai de Mythal", "Plume de Phénix", "Fleur d’Ombrelune"],
        'Difficulter' : 3
    },
    'Marécage' : {
        'Mob' : ["Salamandre Incandescente", "Wyverne de Givre", "Harpie Chantante", "Gardien de Cristal", "Démon Arcanique"],
        'Loot' : ["Épée Sifflante", "Heaume de Fer Noir", "Étoile Polaire", "Armure Legendaire", "Totem de resurection"],
        'Ressources' : ["Pierre de Sang", "Ambre Vivante", "Cendre d’Asharan"],
        'Difficulter' : 4
    }
}

#################################    map definition        ################################################

### 10 x 10 map
map_forest = []

#################################    Variable definition        ################################################

loop = False
player_X = 4
player_Y = 9
last_location = [",",","]
last_D = "D"

#################################    fonctions definition        ################################################

### Display map in terminal
def Display_map (map_dis):
    for i in map_dis :
        lign = ''
        for y in i:
            if y == ',' or y == "'" : 
                lign += f"{green} {y} {default}"
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
        
        map[posY][posX], posA[0] = posA[0], map[posY-1][posX]
        posA[1] = posA[0]
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
    Dis_inv = []
    Dis_equip = Inventory["Equipement"]
    Dis_item = Inventory["Items"]
    print ("Pour équiper une armure ou une arme, saisissez le 'N°' de l'objet")
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
 
    choix = input("-->")
    if choix != "":
        try:
            verif = False
            if Dis_item[int(choix)-1] in Weapons:
                Inventory["Equipement"][0] = Dis_item[int(choix)-1]
                Player_stat["Multiplicateur de dégat"] = Player_stat["Base_domage"] + Weapons[Dis_item[int(choix)-1]][0]
                verif = True
                print ("Equiper !!")
            elif Dis_item[int(choix)-1] in Armor:
                Inventory["Equipement"][1] = Dis_item[int(choix)-1]
                Player_stat["Reduction de dégat"] = Armor[Dis_item[int(choix)-1]][0]
                verif = True
                print ("Equiper !!")
            elif verif == False:
                print("Vous ne pouvez pas équipez cet objet")
            time.sleep(1)
        except:
            print ("Saisie invalide")

    os.system('cls' if os.name == 'nt' else 'clear')
    Display_map (map_forest) ## Refresh map

def map_generation (x, y): ## Random map generation
    map_tmp = []
    for i in range (10):
        map2_tmp = []
        for z in range (10):
            if z == x and i == y:
                map2_tmp.append("@")
            else :
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

## interaction between player en universe 
def interaction (posA) :
    if posA[0] == "/":
        count = 0
        if Player_stat["Biome actuel"] == "foret" :
            Random_Monster = randint(0, 4)
            for i in Monsters :
                if count == Random_Monster :
                    for elem in Bioms["Forêt"]["Mob"] :
                        if elem == i :
                            load_pv = Monsters[elem][3]
                            load_domage = randint(Monsters[elem][1], Monsters[elem][2])
                            print (elem,"vous attaque!!\n\n",elem,":\n________________________\n  HP :", load_pv,"   Dégat :", load_domage,"\n\n\nVous :\n________________________\n HP :", Player_stat["PV"], "   Dégat de base :", Player_stat["Multiplicateur de dégat"])
                            print ("\nAppuyer sur 'E' le plus de fois possible pour faire plus de dégâts. (les attaques s'enchaînent, il faut être réactif)")
                            start = input("Ready? (Y/N)\n-->")
                            start_loop = False 
                            while start_loop == False :
                                if start.upper() == "Y" :
                                    while load_pv > 0 and Player_stat["PV"] > 0:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        print ("\n\n",elem,":\n________________________\n  HP :", load_pv,"   Dégat :", load_domage,"\n\n\nVous :\n________________________\n HP :", Player_stat["PV"], "   Dégat de base :", Player_stat["Multiplicateur de dégat"])
                                        
                                        t = threading.Timer(5, lambda: print("\nAppuiez sur 'enter' pour valider"))
                                        t.start()
                                        attack = input("Attaquez !!\n-->")
                                        t.cancel()
                                        load_pv -= (len(attack)/20)*Player_stat["Multiplicateur de dégat"]
                                        if load_pv > (len(attack)/20)*Player_stat["Multiplicateur de dégat"] :
                                            Player_stat["PV"] -= load_domage - (load_domage * Player_stat["Reduction de dégat"])
                                            print ("Dégat donner :", (len(attack)/20)*Player_stat["Multiplicateur de dégat"],"Dégat reçu :", load_domage - (load_domage * Player_stat["Reduction de dégat"]))
                                        else:
                                            print ("Dégat donner :", (len(attack)/20)*Player_stat["Multiplicateur de dégat"])
                                        time.sleep(5)

                                    
                                    if Player_stat["PV"] > 0:
                                        print ("Monstre vaincu !!\nBien jouer\n\n",elem,":\n________________________\n  HP :", 0,"   Dégât :", load_domage,"\n\n\nVous :\n________________________\n HP :", Player_stat["PV"], "   Dégât de base :", Player_stat["Multiplicateur de dégat"])
                                        time.sleep(5)
                                        loot()
                                    else:
                                        print ("Woimp.. Woimp.. Woimp.. !!\nTout ne s'est pas passé comme prévu\n\n",elem,":\n________________________\n  HP :", 0,"   Dégât :", load_domage,"\n\n\nVous :\n________________________\n HP :", 0, "   Dégât de base :", Player_stat["Multiplicateur de dégat"])
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
def loot():
    if Player_stat["Biome actuel"] == "foret" :
        equip = randint(0,4)
        item = randint (0,2)
        Inventory["Items"].append(Bioms["Forêt"]["Loot"][equip])
        Inventory["Items"].append(Bioms["Forêt"]["Ressources"][item])
        os.system('cls' if os.name == 'nt' else 'clear')
        print ("vous avez trouver :",Bioms["Forêt"]["Loot"][equip],"et",Bioms["Forêt"]["Ressources"][item])

## Display the player stat
def Display_stat ():
    for i in Player_stat:
        if i != "Inventaire" :
            print (i,":", Player_stat[i])

## Check if the player win
def win_check ():
    check = True
    for i in map_forest:
        for y in i:
            if y == '/':
                check = False
    return check


#################################    Main Programme        ################################################

print(f"""
{red}________________________________________________________________________________________________________________________________________{default}

Salutation jeune aventurier, avant de commencer je t'invite à lire le README qui peut être utile, de plus la touche 'help' est disponible.

        Votre mission, si vous l'acceptez, sera de vaincre tous les monstres et de rétablir le pays dans cette plaisante forêt !

{red}________________________________________________________________________________________________________________________________________{default}

""")

for i in range (3):
    time.sleep(1)
    print("croutch...")
time.sleep(1)
print("Tu arrives dans une forêt !")
time.sleep(2)


map_forest = map_generation(player_X, player_Y)

Display_map (map_forest)

while loop == False :
    choice = input("-->")
    if choice.upper() == "Z" or choice.upper() == "Q" or choice.upper() == "S" or choice.upper() == "D" : ## Test the input to moove in the map
        if choice.upper() == "Z": ## Moov forward
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
        if  result[0] == True:
            if result[2] == "Leave":
                if last_D == "F": map_forest, player_X, player_Y, last_location = Backward (map_forest, player_X, player_Y, last_location) 
                elif last_D == "B": map_forest, player_X, player_Y, last_location = Forward (map_forest, player_X, player_Y, last_location)
                elif last_D == "R" : map_forest, player_X, player_Y, last_location = Left (map_forest, player_X, player_Y, last_location)
                elif last_D == "L" : map_forest, player_X, player_Y, last_location = Right (map_forest, player_X, player_Y, last_location)
                last_location[0] = last_location[1] #refresh the last location item
            else:
                last_location = result[1]
            Display_map(map_forest)
            if win_check() == True :
                print("""
                  

                  Quelle puissance !! Vous avez réussi à vaincre tous les monstres !

                                Vous avez gagné, Bien joué !!!!
                  
                  """)
                loop = True
        elif result[0] == False :
            loop = True
            print ("""
                   
                   Vous avez été vaincu par un monstre maléfique !
                   
                                    Game Over !
                   """)


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



