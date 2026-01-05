# 📊 Report Builder TRACK/LIVE - SOCOCIM Industries
## Solution de Consolidation des Rapports GPS Fleet Management

---

## 🎯 Présentation du Projet

Cette solution a été développée pour **consolider plus de 30 rapports dispersés en 8 rapports optimisés**, permettant une réduction de **70% du nombre de rapports** tout en centralisant l'information clé et en standardisant les indicateurs.

### Problématique Initiale
- ❌ Plus de 30 rapports dispersés difficiles à gérer
- ❌ Information fragmentée sur plusieurs fichiers
- ❌ Indicateurs non standardisés
- ❌ Difficulté d'automatisation
- ❌ Perte de temps dans la génération manuelle

### Solution Apportée
- ✅ 8 rapports consolidés optimisés
- ✅ Information centralisée et structurée
- ✅ Indicateurs standardisés et cohérents
- ✅ Automatisation facilitée
- ✅ Visualisations interactives
- ✅ Export Excel/CSV intégré
- ✅ Données fictives réalistes pour démonstration

---

## 📦 Contenu de la Solution

### Fichiers Principaux

1. **`report_builder_enhanced.py`** (Application principale)
   - Interface Streamlit complète
   - 8 rapports pré-configurés
   - Visualisations interactives (Plotly)
   - Export Excel/CSV
   - Filtres et personnalisation

2. **`data_generator.py`** (Générateur de données)
   - Génère des données fictives réalistes
   - 15 véhicules de la flotte SOCOCIM
   - 30 jours d'historique
   - Données de trajets, performance, sécurité, maintenance, alertes

3. **Fichiers de données générés** (CSV)
   - `trips_data.csv` - 1079 trajets détaillés
   - `daily_summary.csv` - 347 résumés quotidiens
   - `performance_data.csv` - 15 analyses de performance
   - `safety_data.csv` - 221 analyses de sécurité
   - `maintenance_data.csv` - 15 états de maintenance
   - `alerts_data.csv` - 45 alertes

4. **`requirements.txt`**
   - Dépendances Python nécessaires

5. **`README_COMPLET.md`**
   - Documentation complète
   - Guide d'utilisation
   - Architecture du système

---

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Générer les données fictives (si nécessaire)
python data_generator.py

# 3. Lancer l'application
streamlit run report_builder_enhanced.py
```

### Accès à l'Application
Une fois lancée, l'application s'ouvre automatiquement dans votre navigateur à l'adresse :
```
http://localhost:8501
```

---

## 📋 Les 8 Rapports Consolidés

### 1. 📊 Tableau de Bord Unifié
- **Objectif** : Vue temps réel de la flotte complète
- **Utilisateurs** : Gestionnaires
- **Fréquence** : En continu
- **Remplace** : Tableau de bord moteur, Utilisation flotte, Température en direct

### 2. 🗺️ Analyse de Trajets
- **Objectif** : Historique complet des déplacements
- **Utilisateurs** : Gestionnaires
- **Fréquence** : À la demande
- **Remplace** : Voyages, Itinéraires, Visites, Analyse géographique

### 3. 📈 Performance Véhicules
- **Objectif** : Consommation et utilisation
- **Utilisateurs** : Gestionnaires
- **Fréquence** : Quotidien/Hebdo
- **Remplace** : Consommation carburant, Statistiques moteur, Ralenti

### 4. 🛡️ Conduite & Sécurité
- **Objectif** : Comportement routier
- **Utilisateurs** : Gestionnaires/Sécurité
- **Fréquence** : Hebdo/Mensuel
- **Remplace** : Excès vitesse, Durées vitesse, Événements conduite

### 5. 🔧 Maintenance & Diagnostic
- **Objectif** : Santé des véhicules
- **Utilisateurs** : Gestionnaires/Atelier
- **Fréquence** : Hebdo
- **Remplace** : Codes panne, Maintenance programmée, Alertes

### 6. ⏰ Rapports Quotidiens
- **Objectif** : Synthèse journalière
- **Utilisateurs** : Gestionnaires
- **Fréquence** : Quotidien auto
- **Remplace** : Résumé quotidien, 24h détaillé, Compteurs quotidiens

### 7. 📄 Résumé Exécutif
- **Objectif** : KPIs essentiels
- **Utilisateurs** : Direction
- **Fréquence** : Mensuel
- **Remplace** : Multiple (vue simplifiée)

### 8. 📋 Historique Alertes
- **Objectif** : Journal des alertes
- **Utilisateurs** : Sécurité
- **Fréquence** : À la demande
- **Remplace** : Détails événements, Alertes diverses

---

## 💻 Utilisation de l'Application

### Interface Principale

L'application est organisée en **3 onglets principaux** :

#### 1️⃣ Rapports Consolidés
- Sélection parmi les 8 rapports pré-configurés
- Génération instantanée du rapport
- Prévisualisation des données
- Export Excel avec un clic
- Statistiques clés en temps réel

**Comment utiliser :**
1. Cliquez sur un rapport dans la grille
2. Consultez les détails et statistiques
3. Cliquez sur "📥 Générer le Rapport"
4. Téléchargez en Excel si nécessaire
5. Utilisez les filtres pour affiner les données

#### 2️⃣ Visualisations
Tableaux de bord interactifs avec 4 types d'analyses :

**A. Performance Flotte**
- Top 10 véhicules par distance
- Consommation moyenne par type
- Efficacité vs Distance parcourue

**B. Analyse Sécurité**
- Distribution des scores de conduite
- Top 10 incidents de conduite
- Répartition par niveau de risque

**C. Consommation Carburant**
- Évolution quotidienne de la consommation
- Top 10 consommateurs
- Efficacité carburant

**D. Vue d'Ensemble**
- KPIs principaux de la flotte
- Répartition par type de véhicule
- Alertes par type

#### 3️⃣ Configuration
- Statistiques du système
- Documentation de la consolidation
- Paramètres d'export et d'automatisation

---

## 📊 Données Fictives Générées

### Flotte SOCOCIM
- **15 véhicules** de types variés :
  - Camions Ciment (Mercedes Actros, Volvo FH16)
  - Camions Benne
  - Véhicules Légers (Renault Master, Toyota Hilux)
  - Chariots Élévateurs (Hyster H50)

### Conducteurs
- 15 conducteurs fictifs avec noms sénégalais réalistes
- Affectation dynamique aux véhicules

### Zones Géographiques
- 15 zones autour de Dakar et Rufisque :
  - SOCOCIM Rufisque
  - Port de Dakar
  - Plateau, Almadies, Parcelles Assainies
  - Guédiawaye, Pikine, Thiaroye
  - Keur Massar, Diamniadio, Bargny, etc.

### Métriques Générées
- **1079 trajets** sur 30 jours
- **347 résumés quotidiens** par véhicule
- **Distance totale** : >20,000 km
- **Consommation totale** : >4,000 litres
- **Incidents de conduite** : excès de vitesse, freinages brusques
- **Alertes** : 45 alertes de différents types

---

## 🎨 Caractéristiques Techniques

### Interface Utilisateur
- Design moderne et responsive
- Couleurs corporate SOCOCIM (#fc6b03 orange, #1bc29e turquoise)
- Navigation intuitive par onglets
- Cards interactives pour les rapports
- Visualisations Plotly interactives

### Fonctionnalités Avancées
1. **Génération de Rapports**
   - Instantanée avec données réelles
   - Métadonnées incluses
   - Statistiques calculées en temps réel

2. **Filtres Dynamiques**
   - Par véhicule
   - Par période (dans les futures versions)
   - Par zone géographique

3. **Export de Données**
   - Format Excel (.xlsx) avec métadonnées
   - Format CSV pour traitement externe
   - Structure organisée en feuilles

4. **Visualisations**
   - Graphiques à barres interactifs
   - Graphiques en ligne pour les tendances
   - Scatter plots pour les corrélations
   - Histogrammes pour les distributions
   - Pie charts pour les répartitions

### Performance
- Chargement des données optimisé avec `@st.cache_data`
- Rendu rapide même avec 1000+ lignes
- Interface réactive

---

## 📈 Bénéfices de la Consolidation

### Gains Quantitatifs
- **70% de réduction** du nombre de rapports
- **30+ rapports** consolidés en **8 rapports**
- **84 colonnes** disponibles au total
- **Temps de génération** : < 5 secondes par rapport

### Gains Qualitatifs
- ✅ Information centralisée
- ✅ Indicateurs standardisés
- ✅ Facilité d'automatisation
- ✅ Meilleure prise de décision
- ✅ Vue d'ensemble de la flotte
- ✅ Détection rapide des anomalies
- ✅ Suivi de performance facilité

---

## 🔄 Évolutions Futures

### Fonctionnalités Prévues
- [ ] **Export PDF** avec graphiques intégrés
- [ ] **Planification automatique** des rapports
- [ ] **Envoi email** automatique
- [ ] **Alertes en temps réel** configurables
- [ ] **Comparaisons période à période**
- [ ] **Benchmarking** entre véhicules
- [ ] **Intégration API** TRACK/LIVE
- [ ] **Historique** des rapports générés
- [ ] **Partage de modèles** entre utilisateurs
- [ ] **Dashboard temps réel** avec rafraîchissement auto
- [ ] **Rapports personnalisés** avancés
- [ ] **Prévisions** basées sur ML

### Améliorations Techniques
- [ ] Base de données PostgreSQL pour stockage
- [ ] Cache Redis pour performance
- [ ] API REST pour intégration externe
- [ ] Authentication multi-utilisateurs
- [ ] Logs et audit trail
- [ ] Tests unitaires et d'intégration

---

## 🛠️ Architecture Technique

### Stack Technologique
```
Frontend:
  - Streamlit (interface web)
  - Plotly (visualisations)
  - HTML/CSS personnalisé

Backend:
  - Python 3.8+
  - Pandas (traitement données)
  - NumPy (calculs)

Export:
  - OpenPyXL (Excel)
  - CSV natif Python

Données:
  - CSV (actuellement)
  - Future: PostgreSQL/MongoDB
```

### Structure des Fichiers
```
report-builder/
│
├── report_builder_enhanced.py    # Application principale
├── data_generator.py              # Générateur de données
├── requirements.txt               # Dépendances
├── README_COMPLET.md             # Documentation
│
├── data/                          # Données générées
│   ├── trips_data.csv
│   ├── daily_summary.csv
│   ├── performance_data.csv
│   ├── safety_data.csv
│   ├── maintenance_data.csv
│   └── alerts_data.csv
│
└── docs/                          # Documentation supplémentaire
    ├── user_guide.md
    └── api_specification.md
```

---

## 📞 Support et Contact

### Informations
- **Projet** : Report Builder TRACK/LIVE
- **Client** : SOCOCIM Industries
- **Département** : Gestion de Flotte
- **Système** : TRACK/LIVE GPS Fleet Management

### Assistance
Pour toute question ou assistance technique :
- Contact : Big Data - SOCOCIM Industries
- Module : TRACK/LIVE Report Builder

---

## 📄 Licence et Copyright

**Report Builder TRACK/LIVE** - SOCOCIM Industries © 2025  
Tous droits réservés.

Ce système a été développé spécifiquement pour la gestion de la flotte SOCOCIM Industries dans le cadre du projet de consolidation des rapports GPS TRACK/LIVE.

---

## 🎓 Guide de Démarrage Rapide

### En 5 Minutes

1. **Installation** (1 minute)
   ```bash
   pip install -r requirements.txt
   ```

2. **Génération des données** (30 secondes)
   ```bash
   python data_generator.py
   ```

3. **Lancement de l'application** (10 secondes)
   ```bash
   streamlit run report_builder_enhanced.py
   ```

4. **Premier rapport** (2 minutes)
   - Sélectionnez "Performance Véhicules"
   - Cliquez sur "Générer le Rapport"
   - Explorez les données et visualisations
   - Téléchargez en Excel

5. **Exploration** (1 minute)
   - Testez les autres rapports
   - Consultez les visualisations
   - Essayez les filtres

**Et voilà ! Vous maîtrisez le système en 5 minutes ! 🚀**

---

## 🌟 Points Forts de la Solution

1. **Simplicité d'Utilisation** 👍
   - Interface intuitive
   - Pas de formation complexe requise
   - 3 clics pour générer un rapport

2. **Données Réalistes** 📊
   - Basées sur la flotte SOCOCIM
   - Zones géographiques de Dakar
   - Métriques cohérentes

3. **Visualisations Puissantes** 📈
   - Graphiques interactifs
   - Drill-down possible
   - Export d'images

4. **Extensibilité** 🔧
   - Architecture modulaire
   - Facile à adapter
   - Prêt pour l'intégration API

5. **Performance** ⚡
   - Chargement rapide
   - Traitement efficace
   - Cache intelligent

---

**Développé avec ❤️ pour optimiser la gestion de flotte SOCOCIM**
