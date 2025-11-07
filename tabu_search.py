import streamlit as st
import random
import matplotlib.pyplot as plt
from collections import deque
import math

# ===================== ALGORITHME TABU SEARCH =====================
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

    historique = [(meilleure_solution, meilleure_distance)]

    for iteration in range(nombre_iterations):
        voisins = generer_voisins(solution_actuelle)
        voisins = [v for v in voisins if v not in tabu_list]

        if not voisins:
            break

        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

        tabu_list.append(solution_actuelle)

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle
            historique.append((meilleure_solution, meilleure_distance))

    return meilleure_solution, meilleure_distance, historique

# ===================== INTERFACE STREAMLIT =====================
st.set_page_config(page_title="Tabu Search Visualizer", page_icon="🧠", layout="centered")

st.title("🧠 Visualisation de la Recherche Tabou (TSP)")
st.write("Ce projet illustre le fonctionnement de l’algorithme de recherche tabou appliqué au **problème du voyageur de commerce**.")

# --- paramètres utilisateur
col1, col2, col3 = st.columns(3)
with col1:
    nb_villes = st.slider("Nombre de villes", 4, 15, 8)
with col2:
    nb_iter = st.slider("Nombre d’itérations", 100, 2000, 500)
with col3:
    taille_tabu = st.slider("Taille de la liste tabou", 5, 100, 30)

# --- génération des coordonnées aléatoires
coords = [(random.random() * 100, random.random() * 100) for _ in range(nb_villes)]
matrice = [[math.dist(coords[i], coords[j]) if i != j else 0 for j in range(nb_villes)] for i in range(nb_villes)]

# --- exécution du modèle
if st.button("🚀 Lancer la recherche tabou"):
    meilleure_solution, meilleure_distance, historique = tabu_search(matrice, nb_iter, taille_tabu)

    st.success(f"✅ Meilleure distance trouvée : **{meilleure_distance:.2f}**")
    st.text(f"Meilleure solution : {meilleure_solution}")

    # --- visualisation graphique
    fig, ax = plt.subplots(figsize=(6, 6))
    x = [coords[i][0] for i in meilleure_solution] + [coords[meilleure_solution[0]][0]]
    y = [coords[i][1] for i in meilleure_solution] + [coords[meilleure_solution[0]][1]]
    ax.plot(x, y, '-o', color='royalblue')
    for i, (cx, cy) in enumerate(coords):
        ax.text(cx + 1, cy + 1, str(i), fontsize=9)
    ax.set_title("Meilleur chemin trouvé")
    st.pyplot(fig)

    # --- évolution du score
    fig2, ax2 = plt.subplots()
    ax2.plot([d for _, d in historique], color='orange')
    ax2.set_xlabel("Améliorations successives")
    ax2.set_ylabel("Distance minimale")
    ax2.set_title("Évolution de la solution")
    st.pyplot(fig2)
