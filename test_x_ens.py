import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#on charge le fichier intéressant
df = pd.read_excel('data/LETUDIANT_INGE.xlsx')

#on nettoie les données nécessaires
df['Taux intégration 1 an (%)'] = pd.to_numeric(df['1_an_taux_integration'], errors='coerce')



#on filtre les données par filière et panier, puis on crée les graphiques
filieres = df['Filière'].unique()
paniers = df['Panier'].unique()

for filiere in filieres:
    df_filiere = df[df['Filière'] == filiere]
    for panier in paniers:
        df_panier = df_filiere[df_filiere['Panier'] == panier]

        if not df_panier.empty:
            #on filtre les prépas avec un ratio d'intégration significatif
            df_panier = df_panier[df_panier['Taux intégration 1 an (%)'] > 0.01]

            if not df_panier.empty:

                #on trie par ordre décroissant de taux d'intégration
                df_panier = df_panier.sort_values(by='Taux intégration 1 an (%)', ascending=False)
                # Préparer les données pour le graphique
                etabs = df_panier['Nom_ecole']
                taux_integration = df_panier['Taux intégration 1 an (%)']

                #on crée le graphique
                x = np.arange(len(etabs))
                width = 0.35

                fig, ax = plt.subplots(figsize=(15, 8))
                rects1 = ax.bar(x - width/2, taux_integration, width, label='Taux intégration 1 an (%)', color='blue')

                ax.set_ylabel('Pourcentage')
                ax.set_title(f'Comparaison des chances d\'intégration pour {filiere} - {panier}')
                ax.set_xticks(x)
                ax.set_xticklabels(etabs, rotation=90)
                ax.legend()

                plt.tight_layout()
                plt.savefig(f'résultats/comparaison_{filiere}_{panier}.png')
                plt.close()

print("Graphiques générés.")
