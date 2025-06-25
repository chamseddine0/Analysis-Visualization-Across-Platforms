"""
MINI PROJET realise par Chamseddine Bichri : Analyse et visualisation des 
habitudes d'écoute musicale Script complet avec gestion des données, analyses et visualisations
"""

import pandas as pd                   # Traitement des données tabulaires
import numpy as np                    # Statistiques et calculs  
import matplotlib.pyplot as plt       # Visualisation simple  
import seaborn as sns                 # Visualisation avancée et heatmap  
import os                             #Création et Manipulation de dossiers
from datetime import datetime         # Manipulation de dates
import calendar                       # Noms des jours de la semaine  

# ==============================================
# Partie 1 - Préparation & Nettoyage des Données
# ==============================================

"""
Cette section prépare les données pour l'analyse en:
1. Chargeant le fichier CSV
2. Nettoyant les noms de colonnes
3. Convertissant les formats de date/heure
4. Créant de nouvelles colonnes utiles
5. Supprimant les doublons et valeurs manquantes
"""

# Charger les données en spécifiant l'encodage
df = pd.read_csv("ecoute_musique.csv", encoding='utf-8-sig')

# Nettoyer les noms de colonnes
df.columns = df.columns.str.strip().str.lower().str.replace('é', 'e')

# Conversion des dates et heures
df['date'] = pd.to_datetime(df['date'])
df['heure_ecoute'] = pd.to_datetime(df['heure_ecoute'], format='%H:%M').dt.time

# Création des nouvelles colonnes
# - jour_semaine: nom du jour en français
df['jour_semaine'] = df['date'].dt.day_name(locale='French')
df['heure_arrondie'] = df['heure_ecoute'].apply(lambda x: x.hour)

# Nettoyage des données
# - suppression des doublons
# - suppression des lignes avec valeurs manquantes
df = df.drop_duplicates().dropna()

# ==============================================
# Partie 2 - Analyse Temporelle
# ==============================================

"""
Analyse des tendances d'écoute selon:
- Les heures de la journée
- Les jours de la semaine
- Combinaison jour/heure via heatmap
"""

# Créer le dossier pour les graphiques
# exist_ok=True évite les erreurs si le dossier existe déjà
os.makedirs("graphiques", exist_ok=True)

# 1. Répartition par heure
plt.figure(figsize=(10, 6))
df['heure_arrondie'].value_counts().sort_index().plot(kind='bar', color='teal')
plt.title("Fréquence d'écoute par heure")
plt.xlabel("Heure de la journée")
plt.ylabel("Nombre d'écoutes")
plt.savefig("graphiques/frequence_heure.png", bbox_inches='tight')
plt.close()

# 2. Répartition par jour
# Ordre des jours pour un affichage logique
jours_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
plt.figure(figsize=(10, 6))
df['jour_semaine'].value_counts().reindex(jours_order).plot(kind='bar', color='skyblue')
plt.title("Écoutes par jour de la semaine")
plt.savefig("graphiques/ecoute_jour.png", bbox_inches='tight')
plt.close()

# 3. Heatmap
plt.figure(figsize=(12, 6))
heatmap_data = df.pivot_table(index='jour_semaine', columns='heure_arrondie', aggfunc='size', fill_value=0).reindex(jours_order)
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d')
plt.title("Heatmap des écoutes")
plt.savefig("graphiques/heatmap.png", bbox_inches='tight')
plt.close()

# ==============================================
# Partie 3 - Analyse des Préférences Musicales
# ==============================================

"""
Analyse des tendances musicales:
- Genre le plus populaire
- Durée moyenne d'écoute par genre
"""

# 1. Genre le plus écouté
genre_global = df['genre'].value_counts().idxmax()

# 2. Durée moyenne par genre
plt.figure(figsize=(10, 6))
df.groupby('genre')['duree'].mean().sort_values().plot(kind='barh', color='darkorange')
plt.title("Durée moyenne d'écoute par genre")
plt.savefig("graphiques/duree_genre.png", bbox_inches='tight')
plt.close()

# ==============================================
# Partie 4 - Analyse des Plateformes
# ==============================================

"""
Comparaison des plateformes de streaming selon:
- Temps total d'écoute
- Popularité en week-end
"""

# 1. Total minutes par plateforme
total_min = df.groupby('plateforme')['duree'].sum()

# 2. Plateforme la plus utilisée le week-end
plateforme_weekend = df[df['jour_semaine'].isin(['Samedi', 'Dimanche'])]['plateforme'].value_counts().idxmax()

# ==============================================
# Partie 5 - Export et Synthèse
# ==============================================

"""
Export des résultats principaux:
- Fichier CSV avec les statistiques clés
- Graphiques sauvegardés en PNG
"""

# Création du dataframe de résultats
resultats = pd.DataFrame({
    'Genre_plus_ecoute': [genre_global],
    'Plateforme_weekend': [plateforme_weekend],
    'Duree_moyenne_totale': [df['duree'].mean()],
    'Total_sessions': [len(df)]
})

# Export des résultats
resultats.to_csv("resultats_ecoute.csv", index=False)

print("----------------Analyse terminée avec succès!-----------------")

"""
- Résultats exportés dans 'resultats_ecoute.csv'
- Graphiques sauvegardés dans le dossier 'graphiques/
'"""