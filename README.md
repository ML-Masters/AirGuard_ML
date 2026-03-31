
-----

# ML Masters: AirGuard

[](https://www.python.org/)
[](https://scikit-learn.org/)
[](https://www.google.com/search?q=https://indabaxcameroon.com)

> **"L'IA au service de la santé et de la sécurité climatique au Cameroun."**
> Projet développé par l'équipe **ML Masters** dans le cadre du Hackathon IndabaX Cameroon 2026.

## Présentation

AirGuard est une solution de surveillance et de prédiction climatique conçue pour répondre aux défis spécifiques du Cameroun : vagues de chaleur humide (Douala), sécheresse agricole (Nord) et pollution de l'air urbaine.

Comme le Cameroun dispose de peu de capteurs de pollution en temps réel, nous avons développé des **proxies mathématiques basés sur la physique atmosphérique** pour transformer les données météo en indicateurs de santé publique.

## Fonctionnalités Clés

Le moteur IA modélise **7 indicateurs critiques** répartis en 3 axes :

1.  **Axe Eau :** Déficit hydrique (FAO 56), risque d'inondation et stress agricole.
2.  **Axe Thermique :** Indice de chaleur (Heat Index de Rothfusz) et score de chaleur extrême.
3.  **Axe Santé :** Estimation des particules fines (**Proxy PM2.5**) et conversion en indice **AQI** (Air Quality Index).

## Stack Technique

  * **Langage :** Python
  * **Modélisation :** `XGBoost`, `LightGBM`, `RandomForest`, `Scikit-Learn` (VotingRegressor).
  * **Explicabilité :** `SHAP` (pour comprendre quels facteurs climatiques augmentent la pollution).
  * **Preprocessing :** TimeSeriesSplit (validation croisée temporelle), Feature Engineering (Lags, Rolling stats, Sin/Cos encoding).

## Résultats du Modèle (PM2.5)

Notre modèle "Ensemble" (LightGBM + XGBoost) obtient des performances robustes sur les données de test :

  * **R² :** `> 0.95` (sur les proxies construits)
  * **MAE :** Précision fine pour les alertes sanitaires.
  * **Interprétabilité :** Grâce à SHAP, nous avons identifié que le rayonnement solaire et l'absence de vent sont les principaux vecteurs de pollution au Cameroun.

##  Structure du Repository

```text
.
├── data/                   # Datasets bruts (Excel/CSV)
├── models/                 # Modèles exportés (.joblib) pour l'API
├── plots/                  # Visualisations générées (Rankings, SHAP, Loss)
├── Notebook_Final.ipynb    # Pipeline complet de modélisation
├── requirements.txt        # Dépendances du projet
└── README.md
```

## Installation

```bash
1.  Clonez le repo :
    
    git clone https://github.com/votre-username/airguard-cameroun.git

2.  Installez les dépendances :
    
    pip install -r requirements.txt
    
3.  Exécutez le notebook pour reproduire les résultats.
```


-----
