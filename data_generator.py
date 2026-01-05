import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class FleetDataGenerator:
    """Générateur de données fictives pour la flotte GPS TRACK/LIVE"""
    
    def __init__(self, num_vehicles=15, num_days=30):
        self.num_vehicles = num_vehicles
        self.num_days = num_days
        self.start_date = datetime.now() - timedelta(days=num_days)
        
        # Définir les véhicules de la flotte SOCOCIM
        self.vehicles = [
            {"id": f"SOC-{str(i+1).zfill(3)}", 
             "immat": f"DK-{random.randint(1000,9999)}-{chr(65+random.randint(0,25))}{chr(65+random.randint(0,25))}", 
             "type": random.choice(["Camion Ciment", "Camion Benne", "Véhicule Léger", "Chariot Élévateur"]),
             "modele": random.choice(["Mercedes Actros", "Volvo FH16", "Renault Master", "Toyota Hilux", "Hyster H50"])}
            for i in range(num_vehicles)
        ]
        
        # Conducteurs
        self.drivers = [
            "Mamadou Diop", "Fatou Sall", "Cheikh Ndiaye", "Aïssatou Ba", 
            "Ousmane Fall", "Ndèye Mbaye", "Ibrahima Sarr", "Aminata Sy",
            "Moussa Diouf", "Khadija Kane", "Abdou Gueye", "Mariama Wade",
            "Alioune Seck", "Astou Diallo", "Babacar Sow"
        ]
        
        # Zones géographiques de Dakar et environs
        self.zones = [
            "SOCOCIM Rufisque", "Port de Dakar", "Plateau (Dakar)", 
            "Almadies", "Parcelles Assainies", "Guédiawaye", "Pikine",
            "Thiaroye", "Keur Massar", "Diamniadio", "Bargny", "Sébikotane",
            "Mbao", "Yeumbeul", "Grand Yoff"
        ]
        
        # Coordonnées GPS approximatives pour Dakar
        self.gps_base = {"lat": 14.7167, "lon": -17.4677}
        
    def generate_trips_data(self):
        """Génère des données de trajets"""
        trips = []
        
        for day in range(self.num_days):
            current_date = self.start_date + timedelta(days=day)
            
            # Chaque véhicule peut faire 2-5 trajets par jour
            for vehicle in self.vehicles:
                num_trips = random.randint(0, 5) if random.random() > 0.1 else 0  # 10% de véhicules inactifs
                
                for trip in range(num_trips):
                    # Heure de départ (entre 6h et 18h)
                    hour_start = random.randint(6, 18)
                    minute_start = random.randint(0, 59)
                    departure_time = current_date.replace(hour=hour_start, minute=minute_start)
                    
                    # Durée du trajet (15 min à 3h)
                    trip_duration = timedelta(minutes=random.randint(15, 180))
                    arrival_time = departure_time + trip_duration
                    
                    # Distance (5-150 km)
                    distance = round(random.uniform(5, 150), 2)
                    
                    # Vitesse moyenne
                    avg_speed = round(distance / (trip_duration.total_seconds() / 3600), 2)
                    
                    # Consommation (dépend du type de véhicule)
                    if "Camion" in vehicle["type"]:
                        base_consumption = random.uniform(25, 35)  # L/100km
                    elif "Chariot" in vehicle["type"]:
                        base_consumption = random.uniform(15, 20)
                    else:
                        base_consumption = random.uniform(8, 12)
                    
                    fuel_used = round((distance * base_consumption / 100), 2)
                    
                    # Nombre d'arrêts
                    num_stops = random.randint(0, 5)
                    stop_duration = timedelta(minutes=random.randint(5, 30) * num_stops)
                    
                    # Zones de départ et d'arrivée
                    departure_zone = random.choice(self.zones)
                    arrival_zone = random.choice([z for z in self.zones if z != departure_zone])
                    
                    trips.append({
                        "Date": current_date.strftime("%Y-%m-%d"),
                        "Véhicule": vehicle["id"],
                        "Immatriculation": vehicle["immat"],
                        "Type": vehicle["type"],
                        "Modèle": vehicle["modele"],
                        "Conducteur": random.choice(self.drivers),
                        "Départ": departure_time.strftime("%H:%M"),
                        "Arrivée": arrival_time.strftime("%H:%M"),
                        "Zone Départ": departure_zone,
                        "Zone Arrivée": arrival_zone,
                        "Distance (km)": distance,
                        "Durée Trajet": str(trip_duration).split('.')[0],
                        "Durée Arrêts": str(stop_duration).split('.')[0],
                        "Nombre Arrêts": num_stops,
                        "Vitesse Moy (km/h)": avg_speed,
                        "Vitesse Max (km/h)": round(avg_speed * random.uniform(1.1, 1.4), 2),
                        "Carburant (L)": fuel_used,
                        "Conso Moy (L/100km)": base_consumption,
                        "Temps Ralenti (min)": random.randint(5, 30),
                        "Excès Vitesse (nb)": random.randint(0, 5) if random.random() > 0.7 else 0,
                        "Freinages Brusques": random.randint(0, 8) if random.random() > 0.6 else 0,
                        "Accélérations Brusques": random.randint(0, 6) if random.random() > 0.6 else 0,
                        "Score Conduite": random.randint(60, 100),
                    })
        
        return pd.DataFrame(trips)
    
    def generate_daily_summary(self, trips_df):
        """Génère un résumé quotidien par véhicule"""
        summary = trips_df.groupby(['Date', 'Véhicule', 'Immatriculation', 'Type']).agg({
            'Distance (km)': 'sum',
            'Carburant (L)': 'sum',
            'Nombre Arrêts': 'sum',
            'Excès Vitesse (nb)': 'sum',
            'Freinages Brusques': 'sum',
            'Score Conduite': 'mean',
            'Durée Trajet': 'count'  # Nombre de trajets
        }).reset_index()
        
        summary.columns = ['Date', 'Véhicule', 'Immatriculation', 'Type', 
                          'Distance Jour (km)', 'Carburant Jour (L)', 
                          'Arrêts Totaux', 'Excès Vitesse', 'Freinages Brusques',
                          'Score Moyen', 'Nb Trajets']
        
        summary['Distance Jour (km)'] = summary['Distance Jour (km)'].round(2)
        summary['Carburant Jour (L)'] = summary['Carburant Jour (L)'].round(2)
        summary['Conso Jour (L/100km)'] = (summary['Carburant Jour (L)'] / summary['Distance Jour (km)'] * 100).round(2)
        summary['Score Moyen'] = summary['Score Moyen'].round(0)
        
        return summary
    
    def generate_performance_data(self, trips_df):
        """Génère des données de performance par véhicule"""
        performance = trips_df.groupby(['Véhicule', 'Immatriculation', 'Type', 'Modèle']).agg({
            'Distance (km)': 'sum',
            'Carburant (L)': 'sum',
            'Temps Ralenti (min)': 'sum',
            'Vitesse Moy (km/h)': 'mean',
            'Vitesse Max (km/h)': 'max',
            'Score Conduite': 'mean'
        }).reset_index()
        
        performance['Conso Moy (L/100km)'] = (performance['Carburant (L)'] / performance['Distance (km)'] * 100).round(2)
        performance['Km Parcourus'] = performance['Distance (km)'].round(2)
        performance['Carburant Total (L)'] = performance['Carburant (L)'].round(2)
        performance['Temps Ralenti (h)'] = (performance['Temps Ralenti (min)'] / 60).round(2)
        performance['Vitesse Moy (km/h)'] = performance['Vitesse Moy (km/h)'].round(2)
        performance['Vitesse Max (km/h)'] = performance['Vitesse Max (km/h)'].round(2)
        performance['Score Conduite'] = performance['Score Conduite'].round(0)
        
        # Calcul de l'efficacité (score combiné)
        performance['Efficacité (%)'] = (
            (performance['Score Conduite'] * 0.4) +  # 40% comportement
            (100 - (performance['Conso Moy (L/100km)'] / 30 * 100).clip(0, 100)) * 0.3 +  # 30% conso
            (100 - (performance['Temps Ralenti (h)'] / 10 * 100).clip(0, 100)) * 0.3  # 30% ralenti
        ).round(0)
        
        return performance[['Véhicule', 'Immatriculation', 'Type', 'Modèle', 
                          'Km Parcourus', 'Carburant Total (L)', 'Conso Moy (L/100km)',
                          'Temps Ralenti (h)', 'Vitesse Moy (km/h)', 'Vitesse Max (km/h)',
                          'Score Conduite', 'Efficacité (%)']]
    
    def generate_safety_data(self, trips_df):
        """Génère des données de sécurité"""
        safety = trips_df.groupby(['Véhicule', 'Immatriculation', 'Conducteur']).agg({
            'Excès Vitesse (nb)': 'sum',
            'Freinages Brusques': 'sum',
            'Accélérations Brusques': 'sum',
            'Score Conduite': 'mean',
            'Distance (km)': 'sum'
        }).reset_index()
        
        # Calcul des incidents pour 100 km
        safety['Excès/100km'] = (safety['Excès Vitesse (nb)'] / safety['Distance (km)'] * 100).round(2)
        safety['Freinages/100km'] = (safety['Freinages Brusques'] / safety['Distance (km)'] * 100).round(2)
        safety['Incidents Totaux'] = safety['Excès Vitesse (nb)'] + safety['Freinages Brusques'] + safety['Accélérations Brusques']
        safety['Score Conduite'] = safety['Score Conduite'].round(0)
        
        # Niveau de risque
        safety['Niveau Risque'] = safety['Score Conduite'].apply(
            lambda x: '🟢 Faible' if x >= 85 else ('🟡 Moyen' if x >= 70 else '🔴 Élevé')
        )
        
        return safety[['Véhicule', 'Immatriculation', 'Conducteur', 
                      'Excès Vitesse (nb)', 'Freinages Brusques', 'Accélérations Brusques',
                      'Incidents Totaux', 'Score Conduite', 'Niveau Risque']]
    
    def generate_maintenance_data(self):
        """Génère des données de maintenance fictives"""
        maintenance = []
        
        for vehicle in self.vehicles:
            # Dernière maintenance il y a 0-90 jours
            last_maint_days = random.randint(0, 90)
            last_maint_km = random.randint(1000, 15000)
            
            # Prochaine maintenance
            next_maint_km = random.randint(5000, 20000)
            km_until_maint = next_maint_km - last_maint_km
            
            # Codes erreur (30% de chance d'avoir une erreur)
            has_error = random.random() < 0.3
            
            maintenance.append({
                "Véhicule": vehicle["id"],
                "Immatriculation": vehicle["immat"],
                "Type": vehicle["type"],
                "Km depuis Maint.": last_maint_km,
                "Km jusqu'à Maint.": km_until_maint,
                "Jours depuis Maint.": last_maint_days,
                "Code Erreur": random.choice(["P0171", "P0420", "P0301", "C0035", "Aucun"]) if has_error else "Aucun",
                "Description": random.choice([
                    "Système mélange pauvre",
                    "Catalyseur défaillant",
                    "Raté allumage cylindre 1",
                    "Capteur vitesse roue",
                    "Aucune"
                ]) if has_error else "Aucune",
                "Statut": random.choice(["✅ OK", "⚠️ Attention", "🔴 Urgent"]) if has_error else "✅ OK",
                "Prochaine Intervention": "Révision" if km_until_maint < 2000 else ("Vidange" if km_until_maint < 5000 else "Entretien Standard")
            })
        
        return pd.DataFrame(maintenance)
    
    def generate_alerts_data(self, trips_df):
        """Génère des données d'alertes"""
        alerts = []
        
        # Générer des alertes aléatoires basées sur les données de trajets
        high_speed_trips = trips_df[trips_df['Excès Vitesse (nb)'] > 0]
        harsh_braking_trips = trips_df[trips_df['Freinages Brusques'] > 3]
        
        for _, trip in high_speed_trips.head(20).iterrows():
            alerts.append({
                "Date": trip['Date'],
                "Heure": trip['Départ'],
                "Véhicule": trip['Véhicule'],
                "Type": "🚨 Excès de vitesse",
                "Zone": trip['Zone Départ'],
                "Détails": f"Vitesse max: {trip['Vitesse Max (km/h)']} km/h",
                "Statut": random.choice(["Active", "Résolue"]),
                "Priorité": "Haute"
            })
        
        for _, trip in harsh_braking_trips.head(15).iterrows():
            alerts.append({
                "Date": trip['Date'],
                "Heure": trip['Arrivée'],
                "Véhicule": trip['Véhicule'],
                "Type": "⚠️ Conduite dangereuse",
                "Zone": trip['Zone Arrivée'],
                "Détails": f"{trip['Freinages Brusques']} freinages brusques",
                "Statut": random.choice(["Active", "Résolue"]),
                "Priorité": "Moyenne"
            })
        
        # Ajouter quelques alertes de géolocalisation
        for _ in range(10):
            alerts.append({
                "Date": (self.start_date + timedelta(days=random.randint(0, self.num_days))).strftime("%Y-%m-%d"),
                "Heure": f"{random.randint(0,23):02d}:{random.randint(0,59):02d}",
                "Véhicule": random.choice(self.vehicles)["id"],
                "Type": "📍 Sortie de zone",
                "Zone": random.choice(self.zones),
                "Détails": "Sortie zone autorisée",
                "Statut": "Résolue",
                "Priorité": "Faible"
            })
        
        return pd.DataFrame(alerts)

# Utilisation
if __name__ == "__main__":
    generator = FleetDataGenerator(num_vehicles=15, num_days=30)
    
    print("Génération des données...")
    trips_df = generator.generate_trips_data()
    daily_summary = generator.generate_daily_summary(trips_df)
    performance = generator.generate_performance_data(trips_df)
    safety = generator.generate_safety_data(trips_df)
    maintenance = generator.generate_maintenance_data()
    alerts = generator.generate_alerts_data(trips_df)
    
    print(f"\n✅ Données générées:")
    print(f"  - {len(trips_df)} trajets")
    print(f"  - {len(daily_summary)} résumés quotidiens")
    print(f"  - {len(performance)} véhicules analysés (performance)")
    print(f"  - {len(safety)} véhicules analysés (sécurité)")
    print(f"  - {len(maintenance)} véhicules en maintenance")
    print(f"  - {len(alerts)} alertes")
    
    # Sauvegarder
    trips_df.to_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/trips_data.csv', index=False)
    daily_summary.to_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/daily_summary.csv', index=False)
    performance.to_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/performance_data.csv', index=False)
    safety.to_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/safety_data.csv', index=False)
    maintenance.to_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/maintenance_data.csv', index=False)
    alerts.to_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/alerts_data.csv', index=False)
    
    print("\n✅ Fichiers sauvegardés dans C:/Users/jhhjjh/Desktop/report-builder2/data/")
