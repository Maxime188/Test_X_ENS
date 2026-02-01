import pandas as pd
import numpy as np
from scipy.stats import norm


letudiant_df = pd.read_excel('data/LETUDIANT_INGE.xlsx')
scei_df = pd.read_excel('data/SCEI_cleaned.xlsx')

#on renomme la colonne anonyme en "Details_formation"
scei_df.rename(columns={scei_df.columns[5]: 'Details_formation'}, inplace=True)

letudiant_df['Nombre intégrés'] = pd.to_numeric(letudiant_df['1_an_nb_integres'], errors='coerce')
letudiant_df['Total élèves'] = pd.to_numeric(letudiant_df['1_an_total_eleves'], errors='coerce')
letudiant_df['Classement 5 ans'] = pd.to_numeric(letudiant_df['classement_5_ans'], errors='coerce')

def estimer_rang_concours(nom_ecole, filiere, rang_interne, panier):

    #on filtre les données par filière et par panier
    df_filiere_panier = letudiant_df[(letudiant_df['Filière'] == filiere) & (letudiant_df['Panier'] == panier)].copy()

    if df_filiere_panier.empty:
        return None

    #log sert à réduire l'écart entre les prépas très bien classées et les autres (le +10 évite les nombres négatifs ou nuls)
    df_filiere_panier.loc[:, 'Coefficient'] = 1 / np.log(df_filiere_panier['Classement 5 ans'] + 10)

    #normalisation du coeff
    df_filiere_panier.loc[:, 'Coefficient'] = df_filiere_panier['Coefficient'] / df_filiere_panier['Coefficient'].max()

    #on trie les prépas
    df_filiere_panier = df_filiere_panier.sort_values(by='Classement 5 ans')

    #on calcule du rang global estimé
    rang_global = 0
    for index, row in df_filiere_panier.iterrows():
        if row['Nom_ecole'] == nom_ecole:

            #quand on trouve la prépa de l'étudiant, on ajoute son rang interne pondéré par le coeff de la prépa
            rang_global += rang_interne * row['Coefficient']
            break
        else:
            #tant que ce n'est pas la prépa de l'étudiant, on ajoute le nombre d'intégrés pondéré par le coeff de la prépa
            rang_global += row['Nombre intégrés'] * row['Coefficient']

    #on introduit une légère variation aléatoire pour simuler l'incertitude dûe au stress du concours etc
    rang_global *= np.random.uniform(0.98, 1.02)

    return int(rang_global)

def estimer_chances_integration(filiere, rang_global, ecole_cible, details_formation=None):
    #on filtre les données SCEI pour la filière, l'école cible et éventuellement la spécialité
    if details_formation:
        scei_filiere_ecole = scei_df[(scei_df['Filière'] == filiere) &
                                     (scei_df['Ecole'] == ecole_cible) &
                                     (scei_df['Details_formation'] == details_formation)]
    else:
        scei_filiere_ecole = scei_df[(scei_df['Filière'] == filiere) &
                                     (scei_df['Ecole'] == ecole_cible)]

    if scei_filiere_ecole.empty:
        return None

    #on obtient le rang médian et le rang moyen
    rang_median = scei_filiere_ecole['Rg médian'].iloc[0]
    rang_moyen = scei_filiere_ecole['Rg moyen'].iloc[0]

    #on estime l'écart-type
    ecart_type = abs(rang_moyen - rang_median) / 2

    #si l'écart-type est nul, on utilise une valeur minimale pour éviter une division par zéro
    if ecart_type == 0:
        ecart_type = 1  # Valeur minimale arbitraire pour éviter une division par zéro

    #on calcule la probabilité d'intégration
    proba = 1 - norm.cdf(rang_global, loc=rang_median, scale=ecart_type)

    return proba

#exemple type
nom_ecole = "Louis-le-Grand"
filiere = "MP"
rang_interne = 5
panier = "ENS"
ecole_cible = "ENS Ulm"

rang_concours = estimer_rang_concours(nom_ecole, filiere, rang_interne, panier)

if rang_concours is not None:
    #on calcule les chances pour chaque spécialité
    specialites = scei_df[(scei_df['Filière'] == filiere) & (scei_df['Ecole'] == ecole_cible)]['Details_formation'].unique()

    for specialite in specialites:
        chances = estimer_chances_integration(filiere, rang_concours, ecole_cible, specialite)
        if chances is not None:
            print(f"Spécialité : {specialite}")
            print(f"Rang estimé au concours {ecole_cible} : {rang_concours}")
            print(f"Chances estimées d'intégration à {ecole_cible} ({specialite}) : {chances:.2%}")
        else:
            print(f"Données non disponibles pour la spécialité {specialite}.")
else:
    print("Données non disponibles pour cette combinaison.")