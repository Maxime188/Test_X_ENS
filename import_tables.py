import pandas as pd
import requests

#liste des liens et des noms de fichiers correspondants
links = {
    "https://www.letudiant.fr/classements/classement-des-prepas-mpi-maths-physique-et-informatique/vous-visez-polytechnique.html": "classement_MPI_Polytechnique.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-mpi-maths-physique-et-informatique/vous-visez-ens.html": "classement_MPI_ENS.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-mpi-maths-physique-et-informatique/vous-visez-polytechnique-ens.html": "classement_MPI_Polytechnique_ENS.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-mpi-maths-physique-et-informatique/vous-visez-panier-large.html": "classement_MPI_Panier_Large.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-pc-physique-chimie/vous-visez-polytechnique.html": "classement_PC_Polytechnique.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-pc-physique-chimie/vous-visez-ens.html": "classement_PC_ENS.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-pc-physique-chimie/vous-visez-polytechnique-ens.html": "classement_PC_Polytechnique_ENS.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-pc-physique-chimie/vous-visez-panier-large.html": "classement_PC_Panier_Large.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-psi-physique-et-sciences-de-lingenieur/vous-visez-polytechnique.html": "classement_PSI_Polytechnique.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-psi-physique-et-sciences-de-lingenieur/vous-visez-polytechnique-ens.html": "classement_PSI_Polytechnique_ENS.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-psi-physique-et-sciences-de-lingenieur/vous-visez-arts-et-metiers.html": "classement_PSI_Arts_et_Metiers.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-psi-physique-et-sciences-de-lingenieur/vous-visez-panier-large.html": "classement_PSI_Panier_Large.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-pt-physique-et-technologie/vous-visez-polytechnique.html": "classement_PT_Polytechnique.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-pt-physique-et-technologie/vous-visez-polytechnique-ens.html": "classement_PT_Polytechnique_ENS.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-pt-physique-et-technologie/vous-visez-arts-et-metiers.html": "classement_PT_Arts_et_Metiers.csv",
    "https://www.letudiant.fr/classements/classement-des-prepas-scientifiques-pt-physique-et-technologie/vous-visez-panier-large.html": "classement_PT_Panier_Large.csv"
}

#on peut extraire les tableaux des pages web et les sauvegarder en CSV
def extract_tables_from_url(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        tables = pd.read_html(response.text)
        if tables:
            df = tables[0]
            df.to_csv(filename, index=False)
            print(f"Tableau extrait et sauvegardé dans {filename}")
            return True
    print(f"Échec de l'extraction pour {filename}")
    return False

#on sauvegarde tous les tableaux
for url, filename in links.items():
    extract_tables_from_url(url, filename)
