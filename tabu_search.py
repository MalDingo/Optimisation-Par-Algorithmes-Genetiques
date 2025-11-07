"""Recherche Tabou pour le problème du voyageur de commerce"""

import random
from collections import deque


def calculer_distance_totale(solution, matrice_distances):

    distance = 0
    for i in range(len(solution) - 1):
        distance += matrice_distances[solution[i]][solution[i + 1]]

    distance += matrice_distances[solution[-1]][solution[0]]
    return distance


def generer_voisins(solution):

    voisins = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins


def tabu_search(matrice_distances, nombre_iterations, taille_tabu):



    nb_villes = len(matrice_distances)
    solution_actuelle = list(range(nb_villes))
    random.shuffle(solution_actuelle)


    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)


    tabu_list = deque(maxlen=taille_tabu)


    for iteration in range(nombre_iterations):

        voisins = generer_voisins(solution_actuelle)


        voisins = [v for v in voisins if v not in tabu_list]


        if not voisins:
            break

        # Choisir le MEILLEUR voisin
        solution_actuelle = min(voisins,
                                key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)


        tabu_list.append(solution_actuelle)


        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance


# EXEMPLE de matrice

matrice_distance = [
    [0, 16, 11, 6, 8, 9, 12, 15, 14, 10],
    [16, 0, 8, 10, 13, 9, 7, 12, 14, 6],
    [11, 8, 0, 7, 9, 12, 14, 10, 11, 8],
    [6, 10, 7, 0, 9, 11, 8, 14, 10, 12],
    [8, 13, 9, 9, 0, 14, 10, 11, 12, 7],
    [9, 9, 12, 11, 14, 0, 10, 13, 9, 8],
    [12, 7, 14, 8, 10, 10, 0, 9, 11, 13],
    [15, 12, 10, 14, 11, 13, 9, 0, 10, 12],
    [14, 14, 11, 10, 12, 9, 11, 10, 0, 8],
    [10, 6, 8, 12, 7, 8, 13, 12, 8, 0]
]


nombre_iterations = 1000
taille_tabu = 50

meilleure_solution, meilleure_distance = tabu_search(
    matrice_distance,
    nombre_iterations,
    taille_tabu
)

print("Meilleure solution trouvée (Tabu Search):", meilleure_solution)
print("Distance minimale:", meilleure_distance)