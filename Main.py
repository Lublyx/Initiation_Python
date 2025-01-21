import random
import os
# os.system('cls' if os.name == 'nt' else 'clear')

Inventaire = {}
Stats_Joueur = {}



Biome = {
    'Forêt' : [{
        'Mob' : [],
        'Loot' : [],
        'Ressources' : []
    }],
    'Ville' : [{
        'Mob' : [],
        'Loot' : [],
        'Ressources' : []
    }],
    'Desert' : [{
        'Mob' : [],
        'Loot' : [],
        'Ressources' : []
    }],
    'Marécage' : [{
        'Mob' : [],
        'Loot' : [],
        'Ressources' : []
    }]
}

