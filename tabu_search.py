import streamlit as st
import random
from collections import deque
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tabu Search Visualizer", page_icon="🚀", layout="centered")

# En-tête
st.title("🚀 Algorithme Tabu Search")
st.subheader("Problème du Voyageur de Commerce (TSP)")
st.write("""
Cet outil permet de visualiser le fonctionnement de l'algorithme **Tabu Search** 
pour trouver le chemin le plus court entre plusieurs villes.
""")

# === Paramètres utilisateur ===
with st.expander("🧠 Paramètres de l'algorithme", expanded=True):
    nombre_iterations = st.slider("Nombre d'itérations", 100, 5000, 1000, step=100)
    taille_tabu = st.slider("Taille de la liste tabou", 5, 100, 50)
    nb_villes = st.slider("Nombre de villes", 5, 10, 10)

# === Matrice distance aléatoire ===
@st.cache_data
def generer_matrice(nb_villes):
    return [[0 if i == j else random.randint(5, 15) for j in range(nb_villes)] for i in range(nb_villes)]

matrice_distance = generer_matrice(nb_villes)

# === Fonctions ===
def calculer_distance_totale(solution, matrice):
    distance = sum(matrice[solution[i]][solution[i + 1]] for i in range(len(solution) - 1))
    return distance + matrice[solution[-1]][solution[0]]

def generer_voisins(solution):
    voisins = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins

def tabu_search(matrice, iterations, taille_tabu):
    nb_villes = len(matrice)
    solution_actuelle = list(range(nb_villes))
    random.shuffle(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice)
    tabu_list = deque(maxlen=taille_tabu)

    for _ in range(iterations):
        voisins = generer_voisins(solution_actuelle)
        voisins = [v for v in voisins if v not in tabu_list]
        if not voisins:
            break
        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice)
        tabu_list.append(solution_actuelle)
        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle
    return meilleure_solution, meilleure_distance

# === Lancement ===
if st.button("🚀 Lancer la recherche Tabou"):
    with st.spinner("Calcul en cours..."):
        meilleure_solution, meilleure_distance = tabu_search(matrice_distance, nombre_iterations, taille_tabu)
    
    st.success(f"✅ Distance minimale trouvée : **{meilleure_distance}**")
    st.write(f"Chemin optimal : {meilleure_solution}")

    # === Visualisation graphique ===
    plt.figure(figsize=(8, 5))
    y = meilleure_solution + [meilleure_solution[0]]
    plt.plot(y, marker='o')
    plt.title("Chemin du voyageur (ordre des villes)")
    plt.xlabel("Étapes")
    plt.ylabel("Ville visitée")
    st.pyplot(plt)
