import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import time
import numpy as np

# ===============================
#  🔹 Fonctions utilitaires
# ===============================
def distance(v1, v2):
    return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)

def generer_matrice(villes):
    n = len(villes)
    matrice = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrice[i][j] = distance(villes[i], villes[j])
    return matrice

def calcul_energie(etat, matrice_energie):
    energie = 0
    for i in range(len(etat) - 1):
        energie += matrice_energie[etat[i]][etat[i+1]]
    energie += matrice_energie[etat[-1]][etat[0]]
    return energie

def generer_voisin(etat):
    voisin = etat[:]
    i, j = random.sample(range(len(etat)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

# ===============================
#  🔥 Recuit simulé
# ===============================
def recuit_simule(matrice, temp_initiale=1000, refroid=0.98, iterations=500):
    etat = list(range(len(matrice)))
    random.shuffle(etat)
    energie = calcul_energie(etat, matrice)
    meilleur, best_energie = etat[:], energie
    temp = temp_initiale

    for _ in range(iterations):
        voisin = generer_voisin(etat)
        energie_voisin = calcul_energie(voisin, matrice)
        delta = energie_voisin - energie
        if delta < 0 or random.random() < math.exp(-delta / temp):
            etat, energie = voisin, energie_voisin
        if energie < best_energie:
            meilleur, best_energie = etat[:], energie
        temp *= refroid
    return meilleur, best_energie

# ===============================
#  🚫 Recherche Tabou
# ===============================
def tabu_search(matrice, iterations=200, tabu_size=15):
    n = len(matrice)
    current = random.sample(range(n), n)
    best = current[:]
    best_cost = calcul_energie(current, matrice)
    tabu_list = []

    for _ in range(iterations):
        voisins = [generer_voisin(current) for _ in range(30)]
        candidats = [(v, calcul_energie(v, matrice)) for v in voisins if v not in tabu_list]
        if not candidats:
            continue
        candidats.sort(key=lambda x: x[1])
        meilleur_voisin, cout = candidats[0]

        if cout < best_cost:
            best, best_cost = meilleur_voisin[:], cout

        tabu_list.append(meilleur_voisin)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        current = meilleur_voisin[:]
    return best, best_cost

# ===============================
#  🧬 Algorithme Génétique (amélioré)
# ===============================
def selection_roulette(population, fitness):
    total_fit = sum(fitness)
    pick = random.uniform(0, total_fit)
    current = 0
    for i, f in enumerate(fitness):
        current += f
        if current > pick:
            return population[i]

def selection_rang(population, fitness):
    sorted_pop = [x for _, x in sorted(zip(fitness, population))]
    rank_probs = np.linspace(0, 1, len(population))
    pick = random.random()
    idx = int(pick * (len(population) - 1))
    return sorted_pop[idx]

def selection_elitiste(population, fitness):
    idx = np.argmax(fitness)
    return population[idx][:]

def crossover_1_point(p1, p2):
    point = random.randint(1, len(p1)-2)
    enfant = p1[:point] + [x for x in p2 if x not in p1[:point]]
    return enfant

def crossover_2_points(p1, p2):
    p1_idx, p2_idx = sorted(random.sample(range(len(p1)), 2))
    enfant = p1[:p1_idx] + [x for x in p2 if x not in p1[:p1_idx] and x not in p1[p2_idx:]] + p1[p2_idx:]
    return enfant

def mutation(etat, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(etat)), 2)
        etat[i], etat[j] = etat[j], etat[i]
    return etat

def algo_genetique(matrice, population_size=50, generations=100, mutation_rate=0.1,
                   selection_method="Roulette", crossover_method="1 point"):
    n = len(matrice)
    population = [random.sample(range(n), n) for _ in range(population_size)]

    for _ in range(generations):
        fitness = [1 / calcul_energie(ind, matrice) for ind in population]
        new_pop = []

        for _ in range(population_size):
            # Sélection
            if selection_method == "Roulette":
                p1 = selection_roulette(population, fitness)
                p2 = selection_roulette(population, fitness)
            elif selection_method == "Rang":
                p1 = selection_rang(population, fitness)
                p2 = selection_rang(population, fitness)
            else:
                p1 = selection_elitiste(population, fitness)
                p2 = selection_elitiste(population, fitness)

            # Croisement
            if crossover_method == "1 point":
                enfant = crossover_1_point(p1, p2)
            else:
                enfant = crossover_2_points(p1, p2)

            # Mutation
            enfant = mutation(enfant, mutation_rate)
            new_pop.append(enfant)

        population = new_pop

    best = min(population, key=lambda x: calcul_energie(x, matrice))
    return best, calcul_energie(best, matrice)

# ===============================
#  🎨 Visualisation
# ===============================
def plot_villes(villes, chemin):
    fig, ax = plt.subplots()
    x = [villes[i][0] for i in chemin]
    y = [villes[i][1] for i in chemin]
    ax.plot(x, y, 'bo-', linewidth=2)

    for i, (xv, yv) in enumerate(villes):
        ax.text(xv + 0.2, yv + 0.2, f"Ville {i}", fontsize=9, color="red")

    ax.scatter(villes[chemin[0]][0], villes[chemin[0]][1], color='green', s=100, label='Départ')
    ax.scatter(villes[chemin[-1]][0], villes[chemin[-1]][1], color='orange', s=100, label='Arrivée')

    ax.legend()
    ax.set_title("Visualisation du chemin optimal (trajet non cyclique)")
    ax.grid(True)
    return fig

# ===============================
#  🌍 Interface Streamlit
# ===============================
st.title("🌐 Optimisation combinatoire - Visualisation des algorithmes")
st.markdown("""
Choisissez un **algorithme d’optimisation** et observez comment il trouve le chemin optimal entre plusieurs villes.
""")

algo = st.selectbox("Choisissez un algorithme :", ["Recuit simulé", "Recherche Tabou", "Algorithme Génétique"])
nb_villes = st.slider("Nombre de villes :", 4, 15, 8)

# Génération des coordonnées
villes = [(random.uniform(0, 20), random.uniform(0, 20)) for _ in range(nb_villes)]
matrice = generer_matrice(villes)

st.write("### 🧮 Matrice des distances (arrondie)")
st.dataframe([[round(x, 2) for x in row] for row in matrice])

if algo == "Algorithme Génétique":
    col1, col2 = st.columns(2)
    with col1:
        selection_method = st.selectbox("Méthode de sélection :", ["Roulette", "Rang", "Élitiste"])
    with col2:
        crossover_method = st.selectbox("Type de croisement :", ["1 point", "2 points"])
else:
    selection_method = crossover_method = None

if st.button("🚀 Lancer l’algorithme"):
    start_time = time.time()

    if algo == "Recuit simulé":
        chemin, cout = recuit_simule(matrice)
    elif algo == "Recherche Tabou":
        chemin, cout = tabu_search(matrice)
    else:
        chemin, cout = algo_genetique(matrice, selection_method=selection_method, crossover_method=crossover_method)

    end_time = time.time()
    execution_time = end_time - start_time

    st.success(f"✅ Chemin trouvé : {chemin}")
    st.info(f"⏱ Temps d'exécution : {execution_time:.4f} secondes")

    fig = plot_villes(villes, chemin)
    st.pyplot(fig)
