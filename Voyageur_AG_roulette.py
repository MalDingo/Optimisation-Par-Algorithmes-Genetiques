import random
import math

# ===============================
# 🔹 FONCTIONS DE BASE
# ===============================

def cout_trajet(trajet, distances):
    """Calcule le coût total d'un trajet (somme des distances entre villes)."""
    total = 0
    for i in range(len(trajet) - 1):
        total += distances[trajet[i]][trajet[i + 1]]
    total += distances[trajet[-1]][trajet[0]]  # retour au point de départ
    return total


def selection_par_roulette(pop, scores, nb_parents):
    """Sélectionne des parents proportionnellement à leur fitness (distance inverse)."""
    poids = [1 / (score + 1) for score in scores]
    return random.choices(pop, weights=poids, k=nb_parents)


# ===============================
# 🔹 MÉTHODES DE CROISEMENT
# ===============================

def crossover_un_point(p1, p2):
    n = len(p1)
    cut = random.randint(1, n - 2)
    enfant = p1[:cut]
    for v in p2:
        if v not in enfant:
            enfant.append(v)
    return enfant


def crossover_deux_points(p1, p2):
    n = len(p1)
    i, j = sorted(random.sample(range(1, n - 1), 2))
    enfant = [-1] * n
    enfant[i:j] = p1[i:j]
    index = j
    for v in p2[j:] + p2[:j]:
        if v not in enfant:
            enfant[index % n] = v
            index += 1
    return enfant


def crossover_mixte(p1, p2):
    """Croisement uniforme (aléatoire 50% de chaque parent)."""
    n = len(p1)
    enfant = []
    for i in range(n):
        if random.random() < 0.5 and p1[i] not in enfant:
            enfant.append(p1[i])
    for v in p2:
        if v not in enfant:
            enfant.append(v)
    return enfant


def appliquer_crossover(p1, p2, type_cx="simple"):
    if type_cx == "simple":
        return crossover_un_point(p1, p2)
    elif type_cx == "double":
        return crossover_deux_points(p1, p2)
    elif type_cx == "mixte":
        return crossover_mixte(p1, p2)
    return crossover_un_point(p1, p2)


# ===============================
# 🔹 MUTATION
# ===============================

def mutation(trajet, proba=0.1):
    """Échange deux villes avec une certaine probabilité."""
    if random.random() < proba:
        i, j = random.sample(range(len(trajet)), 2)
        trajet[i], trajet[j] = trajet[j], trajet[i]
    return trajet


# ===============================
# 🔹 ALGORITHME GÉNÉTIQUE
# ===============================

def algo_genetique(distances, taille=50, generations=100, mutation_taux=0.1, type_cx="simple"):
    nb_villes = len(distances)

    # 🔸 Initialisation population
    population = [random.sample(range(nb_villes), nb_villes) for _ in range(taille)]

    meilleur_chemin = None
    meilleur_score = float("inf")

    for g in range(generations):
        # 🔸 Évaluation
        scores = [cout_trajet(ind, distances) for ind in population]
        meilleur_gen = min(scores)
        if meilleur_gen < meilleur_score:
            meilleur_score = meilleur_gen
            meilleur_chemin = population[scores.index(meilleur_gen)][:]

        if g % 20 == 0:
            print(f"Génération {g:3d} → Meilleur coût : {meilleur_score:.2f}")

        # 🔸 Nouvelle population
        nouvelle_pop = []
        elite_idx = sorted(range(len(scores)), key=lambda x: scores[x])[:2]
        for idx in elite_idx:
            nouvelle_pop.append(population[idx][:])

        # 🔸 Sélection + croisement + mutation
        while len(nouvelle_pop) < taille:
            parents = selection_par_roulette(population, scores, 2)
            enfant = appliquer_crossover(parents[0], parents[1], type_cx)
            enfant = mutation(enfant, mutation_taux)
            nouvelle_pop.append(enfant)

        population = nouvelle_pop

    return meilleur_chemin, meilleur_score


# ===============================
# 🔹 TEST ET COMPARAISON
# ===============================

def test_algorithme():
    distances = [
        [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
        [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
        [2, 10, 0, 8, 4, 3, 3, 4, 2, 3],
        [7, 4, 1, 0, 8, 7, 5, 7, 5, 4],
        [15, 7, 4, 8, 0, 7, 3, 2, 2, 7],
        [2, 3, 3, 7, 7, 0, 4, 5, 4, 3],
        [5, 7, 3, 5, 3, 4, 0, 3, 3, 4],
        [7, 15, 4, 7, 2, 5, 3, 0, 2, 5],
        [6, 8, 2, 5, 2, 4, 3, 2, 0, 3],
        [5, 2, 3, 4, 7, 3, 4, 5, 3, 0]
    ]

    print("\n🚀 ALGORITHME GÉNÉTIQUE — TSP OPTIMISATION 🚀")
    for methode in ["simple", "double", "mixte"]:
        print(f"\nMéthode de croisement : {methode.upper()}")
        sol, cout = algo_genetique(distances, taille=50, generations=100, mutation_taux=0.1, type_cx=methode)
        print(f"Chemin optimal trouvé : {sol}")
        print(f"Distance totale : {cout}\n")


if __name__ == "__main__":
    test_algorithme()
