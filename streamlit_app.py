import streamlit as st
import math
import random
import time
import matplotlib.pyplot as plt

# =========================
# Fonctions communes
# =========================
def calcul_energie(etat, matrice_energie):
    energie_totale = 0
    for i in range(len(etat) - 1):
        energie_totale += matrice_energie[etat[i]][etat[i + 1]]
    energie_totale += matrice_energie[etat[-1]][etat[0]]  # retour à la ville de départ
    return energie_totale

def plot_villes(villes, chemin, titre="Itinéraire trouvé"):
    plt.figure(figsize=(6, 6))
    for i, (x, y) in enumerate(villes):
        plt.scatter(x, y, color="blue")
        plt.text(x + 0.1, y + 0.1, str(i), fontsize=12)
    for i in range(len(chemin) - 1):
        if not ((chemin[i] == 0 and chemin[i + 1] == 8) or (chemin[i] == 8 and chemin[i + 1] == 0)):
            plt.plot(
                [villes[chemin[i]][0], villes[chemin[i + 1]][0]],
                [villes[chemin[i]][1], villes[chemin[i + 1]][1]],
                color="orange"
            )
    plt.title(titre)
    plt.xlabel("X")
    plt.ylabel("Y")
    st.pyplot(plt)

# =========================
# Algorithme : Recuit simulé
# =========================
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

# =========================
# Interface Streamlit
# =========================
st.title("🌍 Visualisation d'Algorithmes d'Optimisation")
st.sidebar.header("⚙️ Paramètres")

algo = st.sidebar.selectbox("Choisissez un algorithme :", ["Recuit simulé", "Tabu", "Algorithme génétique"])

villes = [
    (0, 0), (1, 5), (2, 3), (4, 4), (5, 1),
    (6, 3), (7, 6), (8, 2), (9, 4), (10, 0)
]
matrice_energies = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 8, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 8, 7, 5, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 7, 3],
    [2, 3, 3, 7, 7, 0, 2, 3, 4, 2],
    [5, 7, 3, 5, 3, 2, 0, 2, 3, 1],
    [7, 15, 4, 7, 2, 3, 2, 0, 4, 3],
    [6, 8, 2, 5, 2, 4, 3, 4, 0, 2],
    [5, 2, 3, 4, 7, 2, 1, 3, 2, 0],
]

if st.button("🚀 Lancer l'algorithme"):
    start_time = time.time()

    if algo == "Recuit simulé":
        meilleur_etat, meilleure_energie = recuit_simule(matrice_energies)
    elif algo == "Tabu":
        meilleur_etat, meilleure_energie = recuit_simule(matrice_energies)  # à remplacer par ton code Tabu
    else:
        meilleur_etat, meilleure_energie = recuit_simule(matrice_energies)  # à remplacer par ton code AG

    end_time = time.time()
    execution_time = end_time - start_time

    st.success(f"✅ Algorithme terminé : {algo}")
    st.write(f"**Coût spatial total :** {meilleure_energie:.2f}")
    st.write(f"⏱ **Temps d'exécution :** {execution_time:.4f} secondes")

    plot_villes(villes, meilleur_etat, f"Résultat - {algo}")
