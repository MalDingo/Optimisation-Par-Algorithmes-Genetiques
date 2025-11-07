import streamlit as st
import random
import math

# ----------------------------- Recuit simulé -----------------------------
def calcul_energie(etat, matrice_energie):
    energie_totale = 0
    for i in range(len(etat) - 1):
        energie_totale += matrice_energie[etat[i]][etat[i + 1]]
    energie_totale += matrice_energie[etat[-1]][etat[0]]
    return energie_totale

def generer_voisin(etat):
    voisin = etat[:]
    i, j = random.sample(range(len(etat)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

def recuit_simule(matrice_energie, temp_initiale=1000, refroid=0.95, iterations=1000):
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

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            etat_courant = nouvel_etat
            energie_courante = energie_nouvelle

        if energie_courante < meilleure_energie:
            meilleur_etat = etat_courant[:]
            meilleure_energie = energie_courante

        temperature *= refroid

    return meilleur_etat, meilleure_energie

# ----------------------------- Algorithme Génétique -----------------------------
def algo_genetique(matrice, population_size=50, generations=100, mutation_rate=0.1):
    def fitness(etat):
        return 1 / calcul_energie(etat, matrice)

    def crossover(parent1, parent2):
        point = random.randint(1, len(parent1)-2)
        child = parent1[:point] + [x for x in parent2 if x not in parent1[:point]]
        return child

    def mutate(etat):
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(etat)), 2)
            etat[i], etat[j] = etat[j], etat[i]
        return etat

    n = len(matrice)
    population = [random.sample(range(n), n) for _ in range(population_size)]

    for _ in range(generations):
        population = sorted(population, key=lambda x: calcul_energie(x, matrice))
        new_population = population[:10]
        while len(new_population) < population_size:
            p1, p2 = random.sample(population[:20], 2)
            child = mutate(crossover(p1, p2))
            new_population.append(child)
        population = new_population

    best = min(population, key=lambda x: calcul_energie(x, matrice))
    return best, calcul_energie(best, matrice)

# ----------------------------- Tabu Search -----------------------------
def tabu_search(matrice, iterations=200, tabu_size=10):
    n = len(matrice)
    current = random.sample(range(n), n)
    best = current[:]
    best_cost = calcul_energie(current, matrice)
    tabu_list = []

    for _ in range(iterations):
        voisins = [generer_voisin(current) for _ in range(30)]
        voisins = [(v, calcul_energie(v, matrice)) for v in voisins if v not in tabu_list]

        if not voisins:
            break

        voisins.sort(key=lambda x: x[1])
        meilleur_voisin, cout = voisins[0]

        if cout < best_cost:
            best = meilleur_voisin[:]
            best_cost = cout

        tabu_list.append(meilleur_voisin)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        current = meilleur_voisin[:]

    return best, best_cost

# ----------------------------- Interface Streamlit -----------------------------
st.title("🧠 Optimisation — Algorithmes inspirés de la nature")
st.write("Comparez les performances du **Recuit simulé**, **Algorithme génétique** et **Recherche tabou** sur une même matrice.")

algo = st.selectbox("Choisir un algorithme :", ["Recuit simulé", "Algorithme génétique", "Recherche tabou"])

nb_villes = st.slider("Nombre de villes :", 4, 10, 6)
matrice = [[random.randint(1, 20) if i != j else 0 for j in range(nb_villes)] for i in range(nb_villes)]

st.write("### Matrice de distances")
st.dataframe(matrice)

if st.button("Lancer l’algorithme"):
    if algo == "Recuit simulé":
        chemin, energie = recuit_simule(matrice)
    elif algo == "Algorithme génétique":
        chemin, energie = algo_genetique(matrice)
    else:
        chemin, energie = tabu_search(matrice)

    st.success(f"**Chemin optimal trouvé :** {chemin}")
    st.info(f"**Coût total / énergie :** {energie}")
