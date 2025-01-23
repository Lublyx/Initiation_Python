from random import*
import os


# chemain git : c/Users/lucas/OneDrive/Documents/IPI/Initiation_python/Initiation_Python
# os.system('cls' if os.name == 'nt' else 'clear')


################################       Definition des couleurs            #######################################

rouge = "\033[31m"
vert = "\033[32m"
jaune = "\033[33m"
bleue = "\033[34m"
gris = "\033[61m"


default = "\033[0m"  # Réinitialise le style



#################################    Définition des dictionnaires        ################################################


Inventaire = {
    "Equipement" : [None, None, None], #### Equipement : (Epée, Armure, Bouclier) (équiper sur le personnage)
    "Items" : []
}

Stats_Joueur = {
    "PV" : 100,
    "Déga de base" : 10,
    "Inventaire" : Inventaire,
    "Reduction de déga" : 0,
}

Monstres = {  #### Cractéristique type : (Difficulter, min déga, min déga, vie)
    "Goule des Brumes" : ["Facile", 6, 12, 20],
    "Ombre Rampante" : ["Facile", 3, 9, 25],
    "Troll des Cavernes" : ["Facile", 2, 5, 30],
    "Lycan Sombre" : ["Facile", 10, 15, 15],
    "Cyclope Rugissant" : ["Moyen", 15, 20, 25],
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

Armure = { #### Cractéristique type : (Protection, Chance de drop)
    "Armure Commune" : [0.10, 0.25],
    "Armure Rare" : [0.25, 0.20],
    "Armure Epic" : [0.50, 0.15],
    "Armure Legendaire" : [0.70, 0.10],
    "Bouclier Runique" : [0.30, 0.20],
}

Armes = { #### Cractéristique type : (Déga, Vitesse attaque, Rareter, Chance de drop)
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

Biome = {
    'Forêt' : [{
        'Mob' : ["Goule des Brumes", "Ombre Rampante", "Troll des Cavernes", "Lycan Sombre", "Cyclope Rugissant"],
        'Loot' : ["Lame du Vent", "Arc Éthéré", "Anneau des Âmes", "Armure Commune", "Potion de soin"],
        'Ressources' : ["Poudre d'Étoiles", "Cristal Lunaire", "Éclat de Roche Magmatique"],
        'Difficulter' : 1
    }],
    'Ville' : [{
        'Mob' : ["Spectre Sifflant", "Vampire de Sang Noir", "Basilic Hypnotique", "Faucheuse Spectrale", "Serpent des Flammes"],
        'Loot' : ["Bâton de Lumière", "Amulette de l'Ombre", "Bouclier Runique", "Armure Rare", "Potion d'invisibilité"],
        'Ressources' : ["Sève de l’Arbre Ancien", "Épine du Chaos", "Écaille de Dragon Ancien"],
        'Difficulter' : 2
    }],
    'Desert' : [{
        'Mob' : ["Kraken d’Obsidienne", "Minotaure Écarlate", "Hydre des Abysses", "Chaman Sauvage", "Golem d’Ébène"],
        'Loot' : ["Dague Sanguinaire", "Flèche Explosive", "Grimoire Perdu", "Armure Epic", "Potion de dommge"],
        'Ressources' : ["Minerai de Mythal", "Plume de Phénix", "Fleur d’Ombrelune"],
        'Difficulter' : 3
    }],
    'Marécage' : [{
        'Mob' : ["Salamandre Incandescente", "Wyverne de Givre", "Harpie Chantante", "Gardien de Cristal", "Démon Arcanique"],
        'Loot' : ["Épée Sifflante", "Heaume de Fer Noir", "Étoile Polaire", "Armure Legendaire", "Totem de resurection"],
        'Ressources' : ["Pierre de Sang", "Ambre Vivante", "Cendre d’Asharan"],
        'Difficulter' : 4
    }]
}


#################################    Définition des map        ################################################

### map de 30 x 10
map_foret = []





#################################    Définition des Variables        ################################################

boucle = False
position_joueurX = 4
position_joueurY = 9
position_avant = ","







#################################    Définition des Fonctions        ################################################

### Afficher la map dans le terminale
def Afficher_map (map_aff):
    for i in map_aff :
        linge = ''
        for y in i:
            if y == ',' or y == "'" :
                linge += f"{vert} {y} {default}"
            elif y == 'X' or y == '/' :
                linge += f"{gris} {y} {default}"
            elif y == '@':
                linge += f"{rouge} {y} {default}"
        print (linge)

### Ce déplacer dans la map (Avancer)
def Avancer (map, posX, posY, posA):
    if map[posY-1][posX] != "X":
        map[posY][posX] = posA 
        posA =  map[posY-1][posX]
        map[posY-1][posX] = "@"
        posY -= 1
    return (map, posX, posY, posA)

### Ce déplacer dans la map (Gauche)
def Gauche (map, posX, posY, posA):
    if map[posY][posX-1] != "X":
        map[posY][posX] = posA 
        posA =  map[posY][posX-1]
        map[posY][posX-1] = "@"
        posX -= 1
    return (map, posX, posY, posA)

### Ce déplacer dans la map (Reculer)
def Reculer (map, posX, posY, posA):
    if map[posY+1][posX] != "X":
        map[posY][posX] = posA 
        posA =  map[posY+1][posX]
        map[posY+1][posX] = "@"
        posY +=1
    return (map, posX, posY, posA)

### Ce déplacer dans la map (Droite)
def Droite (map, posX, posY, posA):
    if map[posY][posX+1] != "X":
        map[posY][posX] = posA 
        posA =  map[posY][posX+1]
        map[posY][posX+1] = "@"
        posX += 1
    return (map, posX, posY, posA)

### Afficher l'inventaire du joueur
def Affichage_Inventaire ():
    Aff_inv = []
    Aff_equip = Inventaire["Equipement"]
    Aff_item = Inventaire["Items"]
    for elem in Inventaire :
        Aff_inv.append(elem)
    print ("Equipement équiper :")
    if Aff_equip[0] == None :
        print ("Arme : Aucune")
    else :
        print (f"Arme : {Aff_equip[0]}")
    if Aff_equip[1] == None :
        print ("Armure : Aucune")
    else :
        print (f"Arme : {Aff_equip[1]}")
    if Aff_equip[2] == None :
        print ("Bouclier : Aucun")
    else :
        print (f"Arme : {Aff_equip[2]}")
    print("Items :")
    if Aff_item == [] :
        print ("Inventaire Vide")
    else :
        for i in range (len(Aff_item)):
            print (f"{i+1} - {Aff_item[i]}")


def generer_map (x, y):
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


#################################    Programme Principale        ################################################

print ("Salutation jeune aventurier, avant de commencer je t'invite à lire le README qui peut être utile, deplus la touche 'help' est disponible.\ncroutch...crouch...crouch\nTu arrive dans une forêt\n\n\n")

map_foret = generer_map(position_joueurX, position_joueurY)

Afficher_map (map_foret)

while boucle == False :
    choix = input("-->")
    if choix.upper() == "Z" or choix.upper() == "Q" or choix.upper() == "S" or choix.upper() == "D" : ## Permet de ce déplacer dans la map
        if choix.upper() == "Z":
            if position_joueurY-1 != -1:
                tmp = Avancer (map_foret, position_joueurX, position_joueurY, position_avant)
                map_foret = tmp[0]
                position_joueurX = tmp[1]
                position_joueurY = tmp[2]
                position_avant = tmp[3]
            else :
                print ("Un mur géant !!!!, tu ne peut pas le traverser")

        elif choix.upper() == "Q":
            if position_joueurX-1 != -1:     
                tmp = Gauche (map_foret, position_joueurX, position_joueurY, position_avant)
                map_foret = tmp[0]
                position_joueurX = tmp[1]
                position_joueurY = tmp[2]
                position_avant = tmp[3]
            else :
                print ("Un mur géant !!!!, tu ne peut pas le traverser")

        elif choix.upper() == "S":
            if position_joueurY+1 != 10:
                tmp = Reculer (map_foret, position_joueurX, position_joueurY, position_avant)
                map_foret = tmp[0]
                position_joueurX = tmp[1]
                position_joueurY = tmp[2]
                position_avant = tmp[3]
            else :
                print ("Un mur géant !!!!, tu ne peut pas le traverser")

        elif choix.upper() == "D":
            if position_joueurX+1 != 10:
                tmp = Droite (map_foret, position_joueurX, position_joueurY, position_avant)
                map_foret = tmp[0]
                position_joueurX = tmp[1]
                position_joueurY = tmp[2]
                position_avant = tmp[3]
            else :
                print ("Un mur géant !!!!, tu ne peut pas le traverser")
        Afficher_map (map_foret) ## Actualisation de la map après déplacement


    elif choix.upper() == "E" :
        pass

    elif choix.upper() == "I" :
        Affichage_Inventaire() ## Afficher l'inventaire du joueur
        


    elif choix.upper() == "R":
        Afficher_map (map_foret) ## Actualisation de la map


    elif choix.upper() == "HELP" : ## Affiche des informations suplémentaire sur le jeux
        print ("Pour ce déplacer :\n- Avancer : z\n- Gauche : q\n- Reculer : s\n- Droite : d\nPour intéragire : E\nPour voir l'inventaire : i\nPour ouvrir les recettes de craft : c\nPour actualiser la map : r")


    elif choix.upper() == "ESC": ## Permet de quitter le jeu
        boucle = True
    
    else :
        print ("Saisie invalide")

