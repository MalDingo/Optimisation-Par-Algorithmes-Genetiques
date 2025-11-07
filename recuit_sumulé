import math
import random

def calcul_energie(etat, matrice_energie):
    energie_totale = 0
    for i in range(len(etat) - 1):
        energie_totale += matrice_energie[etat[i]][etat[i + 1]]
    # Retour à la ville de départ (boucle fermée)
    energie_totale += matrice_energie[etat[-1]][etat[0]]
    return energie_totale


def generer_voisin(etat):
    voisin = etat[:]
    i, j = random.sample(range(len(etat)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin


def Recuit_Simule(matrice_energie, temp_initiale=1000, refroid=0.95, iterations=1000):
    nb_villes = len(matrice_energie)
    etat_courant = list(range(nb_villes))
    random.shuffle(etat_courant)

    energie_courante = calcul_energie(etat_courant, matrice_energie)
    meilleur_etat = etat_courant[:]
    meilleure_energie = energie_courante

    temperature = temp_initiale

    for _ in range(iterations):
        nouvel_etat = generer_voisin(etat_courant)
        energie_nouvelle = calcul_energie(nouvel_etat, matrice_energie)
        delta = energie_nouvelle - energie_courante

        # Critère d’acceptation
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            etat_courant = nouvel_etat
            energie_courante = energie_nouvelle

        # Mise à jour du meilleur état trouvé
        if energie_courante < meilleure_energie:
            meilleur_etat = etat_courant[:]
            meilleure_energie = energie_courante

        # Refroidissement progressif
        temperature *= refroid

    return meilleur_etat, meilleure_energie


# ===============================
# 🔹 Exemple avec 10 villes
# ===============================
matrice_energies = [
    [0, 2, 9, 10, 7, 3, 6, 4, 8, 5],
    [2, 0, 8, 6, 5, 9, 7, 3, 4, 6],
    [9, 8, 0, 4, 2, 7, 5, 9, 6, 3],
    [10, 6, 4, 0, 8, 9, 3, 5, 7, 2],
    [7, 5, 2, 8, 0, 6, 9, 3, 4, 7],
    [3, 9, 7, 9, 6, 0, 5, 8, 4, 3],
    [6, 7, 5, 3, 9, 5, 0, 6, 2, 4],
    [4, 3, 9, 5, 3, 8, 6, 0, 5, 7],
    [8, 4, 6, 7, 4, 4, 2, 5, 0, 3],
    [5, 6, 3, 2, 7, 3, 4, 7, 3, 0],
]

meilleur_etat, meilleure_energie = Recuit_Simule(matrice_energies)
print("Chemin trouvé :", meilleur_etat)
print(" Énergie minimale atteinte :", meilleure_energie)
