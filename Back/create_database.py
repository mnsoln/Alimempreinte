import pandas as pd
import argparse
import sqlite3
import csv
import os


parser = argparse.ArgumentParser(description="Fusionne les données de l'ADEME et de l'ANSES pour créer une base de données exploitable par Alimempreinte.")
parser.add_argument('-AD', '--ADEME', type=str, required=False, default='AGRIBALYSE3.1_produits alimentaires.xlsm', help='Chemin vers le fichier de l\'ADEME')
parser.add_argument('-AN', '--ANSES', type=str, required=False,default='Table Ciqual 2020_FR_2020 07 07.xls', help='Chemin vers le fichier de l\'ANSES')
parser.add_argument('--accents', type=bool, required=False, help="True si il y a un problème avec les accents.")
args = parser.parse_args()

### Lecture des données

## ADEME: les données sont obtenues avec la feuille "Synthèse" du document, le sheet_name peut donc être amené à changer si le format de publication des données 
# est modifié dans le futur. Le header correspond au nombre de lignes à ignorer (ici logo + titre), sa valeur est également susceptible de changer à l'avenir.
ademe = pd.read_excel(args.ADEME, sheet_name=1, header = 2)
# Les noms des colonnes sont modifiés pour être simplifiés et avoir une cohérence entre les tables fusionnées. La colonne CIQUAL est indispensable car elle permettra la fusion.
ademe = ademe.rename(columns={"Code\nCIQUAL":"CIQUAL", "Nom du Produit en Français":"Aliment", "kg CO2 eq/kg de produit": 'eCO2'})
# Réduction de la taille de la table pour ne garder que les colonnes d'intérêt
ademe = ademe[['CIQUAL', "Groupe d'aliment", "Sous-groupe d'aliment", 'Aliment', 'eCO2' ]]

## ANSES
anses = pd.read_excel(args.ANSES, sheet_name=0)
anses = anses.rename(columns={"alim_nom_fr":"Aliment2", 
                                "alim_code":"CIQUAL2", 
                                'Protéines, N x 6.25 (g/100 g)': "Proteines (g/kg)", 
                                'Glucides (g/100 g)': "Glucides (g/kg)", 
                                'Sucres (g/100 g)': "Sucres (g/kg)", 
                                'Lipides (g/100 g)': "Lipides (g/kg)"})
anses = anses[['CIQUAL2', 'Proteines (g/kg)', 'Glucides (g/kg)', 'Sucres (g/kg)', 'Lipides (g/kg)']]

# Problème de typage dans les valeurs de la table, une ligne (son de blé) a été dupliquée et contient des valeurs non conformes
anses['CIQUAL2'] = anses['CIQUAL2'].astype(str)
# anses[anses['CIQUAL2']=='9621'] # le coupable

## Élimination des NaN et assimilés
anses['Sucres (g/kg)'] = anses['Sucres (g/kg)'].fillna('0')
anses = anses.replace('-', '0')
anses = anses.replace('traces','0')
anses = anses.apply(lambda x: x.str.replace('<', ''))
# nan_rows = anses[anses.isna().any(axis=1)] # Aide à la visualisation des NaN avec un notebook
anses = anses.dropna()
anses = anses.reset_index(drop=True)

## Conversion des valeurs de certaines colonnes pour correspondre à leur intitulé
anses['Proteines (g/kg)'] = anses['Proteines (g/kg)'].str.replace(',','.').apply(lambda x: float(x) * 10)
anses['Glucides (g/kg)'] = anses['Glucides (g/kg)'].str.replace(',','.').apply(lambda x: float(x)* 10)
anses['Sucres (g/kg)'] = anses['Sucres (g/kg)'].str.replace(',','.').apply(lambda x: float(x) * 10)
anses['Lipides (g/kg)'] = anses['Lipides (g/kg)'].str.replace(',','.').apply(lambda x: float(x) * 10)


### Création de la base de données (bd)
conn = sqlite3.connect('fusion.sql') # bd temporaire pour permettre la fusion (c'est plus simple en SQL que de fusionner deux dataframes)
# conversion des tables en SQL
ademe.to_sql("ademe", conn, index=False, if_exists='replace')
anses.to_sql("ciqual", conn, index=False, if_exists= 'replace')

# requête SQL de fusion
query = 'SELECT *\
            FROM ademe A LEFT JOIN ciqual C ON A.CIQUAL == C.CIQUAL2\
            '

# conversion de la table complète fusionnée en dataframe pandas
df_fusion = pd.read_sql(query, conn)
df_fusion = df_fusion.dropna()
df_fusion = df_fusion.drop(['CIQUAL2'], axis = 1)

# conversion vers un fichier csv pour permettre la lecture et le remplissage de la base de données finale
df_fusion.to_csv('fulldata.csv', index= False, sep=';')
df_fusion

# Suppression de la bd temporaire
# os.remove('fusion.sql')
###

### Création de la base de données finale
conn2 = sqlite3.connect('final_database.sql')
conn2.text_factory = lambda data: str(data, encoding="latin2")
cur = conn2.cursor()
# Création des tables de la bd
cur.execute("DROP TABLE IF EXISTS ingredient")
cur.execute('''CREATE TABLE ingredient
               (id INTEGER PRIMARY KEY, "Nom" TEXT, "kg_CO2" TEXT, "Groupe_aliment" TEXT, "CIQUAL" TEXT, "Proteines" TEXT, "Glucides" TEXT, "Sucres" TEXT, "Lipides" TEXT)''')

# Ajout des données
with open('fulldata.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        cur.execute("INSERT INTO ingredient ('Nom', 'kg_CO2', 'Groupe_aliment', 'CIQUAL', 'Proteines', 'Glucides', 'Sucres', 'Lipides') VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                    (row['Aliment'], row['eCO2'], row['Groupe d\'aliment'], row['CIQUAL'], row['Proteines (g/kg)'], row['Glucides (g/kg)'], row['Sucres (g/kg)'], row['Lipides (g/kg)']))

conn2.commit()
conn2.close()


if args.accents:
    # with open('fulldata.csv', 'r') as csvfile:
    pass
    


