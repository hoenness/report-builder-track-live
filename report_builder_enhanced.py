import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Plateforme de consolidation intelligente des rapports",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec couleurs SOCOCIM
st.markdown("""
<style>
    :root {
        --sococim-orange: #fc6b03;
        --sococim-green: #1bc29e;
    }
    
    .main-header {
        background: linear-gradient(135deg, #003366, #005fa3);

        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stat-card {
        background: linear-gradient(135deg, var(--color-start) 0%, var(--color-end) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .report-card {
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
        background: white;
    }
    
    .report-card:hover {
        border-color: #fc6b03;
        box-shadow: 0 4px 12px rgba(252, 107, 3, 0.1);
        transform: translateY(-2px);
    }
    
    .report-card.selected {
        border-color: #fc6b03;
        background: #fff5f0;
        box-shadow: 0 0 0 3px rgba(252, 107, 3, 0.1);
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .badge-orange {
        background: #fff5f0;
        color: #fc6b03;
    }
    
    .badge-green {
        background: #f0fdf4;
        color: #1bc29e;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# Charger les données
@st.cache_data
def load_data():
    """Charge toutes les données générées"""
    return {
        'trips': pd.read_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/trips_data.csv'),
        'daily': pd.read_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/daily_summary.csv'),
        'performance': pd.read_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/performance_data.csv'),
        'safety': pd.read_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/safety_data.csv'),
        'maintenance': pd.read_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/maintenance_data.csv'),
        'alerts': pd.read_csv('C:/Users/jhhjjh/Desktop/report-builder2/data/alerts_data.csv')
    }

data = load_data()

# Initialisation de session_state
if 'selected_report' not in st.session_state:
    st.session_state.selected_report = None
if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = []
if 'generated_report' not in st.session_state:
    st.session_state.generated_report = None

# Définition des 8 rapports consolidés
PREDEFINED_REPORTS = [
    {
        "id": 1,
        "name": "Tableau de Bord Unifié",
        "icon": "📊",
        "color": "#fc6b03",
        "objective": "Vue temps réel de la flotte complète",
        "users": "Gestionnaires",
        "frequency": "En continu",
        "data_source": "performance",
        "replaces": ["Tableau de bord moteur", "Utilisation flotte", "Température en direct"]
    },
    {
        "id": 2,
        "name": "Analyse de Trajets",
        "icon": "🗺️",
        "color": "#1bc29e",
        "objective": "Historique complet déplacements",
        "users": "Gestionnaires",
        "frequency": "À la demande",
        "data_source": "trips",
        "replaces": ["Voyages", "Itinéraires", "Visites", "Analyse géographique"]
    },
    {
        "id": 3,
        "name": "Performance Véhicules",
        "icon": "📈",
        "color": "#2563eb",
        "objective": "Consommation et utilisation",
        "users": "Gestionnaires",
        "frequency": "Quotidien/Hebdo",
        "data_source": "performance",
        "replaces": ["Consommation carburant", "Statistiques moteur", "Ralenti"]
    },
    {
        "id": 4,
        "name": "Conduite & Sécurité",
        "icon": "🛡️",
        "color": "#dc2626",
        "objective": "Comportement routier",
        "users": "Gestionnaires/Sécurité",
        "frequency": "Hebdo/Mensuel",
        "data_source": "safety",
        "replaces": ["Excès vitesse", "Durées vitesse", "Événements conduite"]
    },
    {
        "id": 5,
        "name": "Maintenance & Diagnostic",
        "icon": "🔧",
        "color": "#f59e0b",
        "objective": "Santé véhicules",
        "users": "Gestionnaires/Atelier",
        "frequency": "Hebdo",
        "data_source": "maintenance",
        "replaces": ["Codes panne", "Maintenance programmée", "Alertes"]
    },
    {
        "id": 6,
        "name": "Rapports Quotidiens",
        "icon": "⏰",
        "color": "#8b5cf6",
        "objective": "Synthèse journalière",
        "users": "Gestionnaires",
        "frequency": "Quotidien auto",
        "data_source": "daily",
        "replaces": ["Résumé quotidien", "24h détaillé", "Compteurs quotidiens"]
    },
    {
        "id": 7,
        "name": "Résumé Exécutif",
        "icon": "📄",
        "color": "#06b6d4",
        "objective": "KPIs essentiels",
        "users": "Direction",
        "frequency": "Mensuel",
        "data_source": "performance",
        "replaces": ["Multiple (vue simplifiée)"]
    },
    {
        "id": 8,
        "name": "Historique Alertes",
        "icon": "📋",
        "color": "#14b8a6",
        "objective": "Journal alertes",
        "users": "Sécurité",
        "frequency": "À la demande",
        "data_source": "alerts",
        "replaces": ["Détails événements", "Alertes diverses"]
    }
]

# Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>📊 Report Builder TRACK/LIVE</h1>
            <p>Plateforme de consolidation intelligente des rapports - FAIT PAR JAïR MOUSSODOU</p>
        </div>
        <div style="text-align: right;">
            <div style="font-weight: bold; font-size: 1.1rem;">Gestion de Flotte</div>
            <div style="opacity: 0.9;">Consolidation 30+ → 8 rapports</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Statistiques globales
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_vehicles = len(data['performance'])
    st.markdown(f"""
    <div class="stat-card" style="--color-start: #2563eb; --color-end: #1d4ed8;">
        <div style="font-size: 1.5rem;">🚛</div>
        <div class="stat-value">{total_vehicles}</div>
        <div class="stat-label">Véhicules Actifs</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_distance = data['performance']['Km Parcourus'].sum()
    st.markdown(f"""
    <div class="stat-card" style="--color-start: #10b981; --color-end: #059669;">
        <div style="font-size: 1.5rem;">📏</div>
        <div class="stat-value">{total_distance:,.0f}</div>
        <div class="stat-label">Km Parcourus (30j)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_fuel = data['performance']['Carburant Total (L)'].sum()
    st.markdown(f"""
    <div class="stat-card" style="--color-start: #f59e0b; --color-end: #d97706;">
        <div style="font-size: 1.5rem;">⛽</div>
        <div class="stat-value">{total_fuel:,.0f}</div>
        <div class="stat-label">Litres Consommés</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_score = data['safety']['Score Conduite'].mean()
    st.markdown(f"""
    <div class="stat-card" style="--color-start: #8b5cf6; --color-end: #7c3aed;">
        <div style="font-size: 1.5rem;">⭐</div>
        <div class="stat-value">{avg_score:.0f}/100</div>
        <div class="stat-label">Score Sécurité Moyen</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Fonction pour générer un rapport
def generate_report(report_config):
    """Génère un rapport selon la configuration"""
    report_id = report_config['id']
    data_source = report_config['data_source']
    
    df = data[data_source].copy()
    
    # Ajouter des métadonnées au rapport
    metadata = {
        "Rapport": report_config['name'],
        "Généré le": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Période": "30 derniers jours",
        "Nombre de lignes": len(df)
    }
    
    return df, metadata

def export_to_excel(df, metadata, report_name):
    """Exporte le rapport en Excel"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Écrire les métadonnées
        meta_df = pd.DataFrame([metadata])
        meta_df.to_excel(writer, sheet_name='Informations', index=False)
        
        # Écrire les données
        df.to_excel(writer, sheet_name='Données', index=False)
    
    output.seek(0)
    return output

# Tabs principaux
tab1, tab2, tab3 = st.tabs(["📄 Rapports Consolidés", "📊 Visualisations", "⚙️ Configuration"])

# ============================================
# TAB 1: RAPPORTS CONSOLIDÉS
# ============================================
with tab1:
    st.markdown("### Sélectionnez un rapport consolidé")
    
    # Afficher les rapports en grille 2x4
    for row in range(4):
        cols = st.columns(2)
        for col_idx in range(2):
            report_idx = row * 2 + col_idx
            if report_idx < len(PREDEFINED_REPORTS):
                report = PREDEFINED_REPORTS[report_idx]
                
                with cols[col_idx]:
                    is_selected = st.session_state.selected_report and st.session_state.selected_report['id'] == report['id']
                    
                    # Carte de rapport
                    st.markdown(f"""
                    <div class="report-card {'selected' if is_selected else ''}">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{report['icon']}</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem; color: {report['color']};">
                            {report['name']}
                        </div>
                        <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                            {report['objective']}
                        </div>
                        <div style="font-size: 0.85rem; color: #6b7280;">
                            👥 {report['users']} &nbsp;|&nbsp; ⏰ {report['frequency']}
                        </div>
                        <div style="margin-top: 1rem;">
                            <span class="badge badge-orange">Remplace: {len(report['replaces'])} rapports</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"{'✓ Sélectionné' if is_selected else '→ Sélectionner'}", 
                               key=f"btn_report_{report['id']}", 
                               type="primary" if is_selected else "secondary",
                               use_container_width=True):
                        st.session_state.selected_report = report
                        st.rerun()
    
    # Afficher le rapport sélectionné
    if st.session_state.selected_report:
        st.markdown("---")
        selected = st.session_state.selected_report
        
        st.markdown(f"""
        ### 📊 {selected['icon']} {selected['name']}
        
        **Objectif:** {selected['objective']}  
        **Utilisateurs:** {selected['users']}  
        **Fréquence:** {selected['frequency']}
        
        **Remplace les rapports suivants:**
        """)
        
        for old_report in selected['replaces']:
            st.markdown(f"  - ❌ {old_report}")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("📥 Générer le Rapport", type="primary", use_container_width=True):
                df, metadata = generate_report(selected)
                st.session_state.generated_report = (df, metadata, selected['name'])
                st.success(f"✅ Rapport généré avec {len(df)} lignes de données")
        
        with col2:
            if st.session_state.generated_report:
                df, metadata, name = st.session_state.generated_report
                excel_data = export_to_excel(df, metadata, name)
                st.download_button(
                    label="📥 Télécharger Excel",
                    data=excel_data,
                    file_name=f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col3:
            if st.session_state.generated_report:
                st.info(f"📄 Rapport prêt: {st.session_state.generated_report[2]}")
        
        # Afficher le rapport généré
        if st.session_state.generated_report:
            df, metadata, name = st.session_state.generated_report
            
            st.markdown("### 📊 Aperçu des Données")
            
            # Métadonnées
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rapport", metadata["Rapport"])
            with col2:
                st.metric("Généré le", metadata["Généré le"])
            with col3:
                st.metric("Période", metadata["Période"])
            with col4:
                st.metric("Lignes", metadata["Nombre de lignes"])
            
            # Filtres
            with st.expander("🔍 Filtres", expanded=False):
                if 'Véhicule' in df.columns:
                    selected_vehicles = st.multiselect(
                        "Sélectionner les véhicules",
                        options=df['Véhicule'].unique(),
                        default=df['Véhicule'].unique()[:5]
                    )
                    if selected_vehicles:
                        df = df[df['Véhicule'].isin(selected_vehicles)]
            
            # Affichage du dataframe
            st.dataframe(
                df,
                use_container_width=True,
                height=400,
                hide_index=True
            )
            
            # Statistiques rapides
            if selected['id'] == 3:  # Performance
                st.markdown("### 📈 Statistiques Clés")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Distance Totale",
                        f"{df['Km Parcourus'].sum():,.0f} km",
                        f"{df['Km Parcourus'].mean():.0f} km/véhicule"
                    )
                with col2:
                    st.metric(
                        "Consommation Moyenne",
                        f"{df['Conso Moy (L/100km)'].mean():.2f} L/100km",
                        f"{df['Conso Moy (L/100km)'].std():.2f} écart-type"
                    )
                with col3:
                    st.metric(
                        "Efficacité Moyenne",
                        f"{df['Efficacité (%)'].mean():.0f}%",
                        f"{df['Efficacité (%)'].max():.0f}% max"
                    )
            
            elif selected['id'] == 4:  # Sécurité
                st.markdown("### 🛡️ Indicateurs de Sécurité")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Incidents Totaux",
                        f"{df['Incidents Totaux'].sum():,.0f}",
                        f"{df['Incidents Totaux'].mean():.0f} par véhicule"
                    )
                with col2:
                    st.metric(
                        "Score Moyen",
                        f"{df['Score Conduite'].mean():.0f}/100",
                        f"Min: {df['Score Conduite'].min():.0f}"
                    )
                with col3:
                    high_risk = len(df[df['Niveau Risque'].str.contains('Élevé')])
                    st.metric(
                        "Véhicules à Risque",
                        high_risk,
                        f"{high_risk/len(df)*100:.0f}% de la flotte"
                    )

# ============================================
# TAB 2: VISUALISATIONS
# ============================================
with tab2:
    st.markdown("### 📊 Tableaux de Bord et Visualisations")
    
    viz_type = st.selectbox(
        "Choisir le type de visualisation",
        ["Performance Flotte", "Analyse Sécurité", "Consommation Carburant", "Vue d'Ensemble"]
    )
    
    if viz_type == "Performance Flotte":
        st.markdown("#### 📈 Performance de la Flotte")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 véhicules par distance
            top_distance = data['performance'].nlargest(10, 'Km Parcourus')
            fig = px.bar(
                top_distance,
                x='Véhicule',
                y='Km Parcourus',
                title='Top 10 - Distance Parcourue',
                color='Km Parcourus',
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Consommation par type de véhicule
            conso_by_type = data['performance'].groupby('Type')['Conso Moy (L/100km)'].mean().reset_index()
            fig = px.bar(
                conso_by_type,
                x='Type',
                y='Conso Moy (L/100km)',
                title='Consommation Moyenne par Type',
                color='Conso Moy (L/100km)',
                color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Efficacité vs Distance
        fig = px.scatter(
            data['performance'],
            x='Km Parcourus',
            y='Efficacité (%)',
            color='Type',
            size='Carburant Total (L)',
            hover_data=['Véhicule', 'Conso Moy (L/100km)'],
            title='Efficacité vs Distance Parcourue'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Analyse Sécurité":
        st.markdown("#### 🛡️ Analyse de Sécurité")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution des scores de conduite
            fig = px.histogram(
                data['safety'],
                x='Score Conduite',
                nbins=20,
                title='Distribution des Scores de Conduite',
                color_discrete_sequence=['#dc2626']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Incidents par véhicule
            top_incidents = data['safety'].nlargest(10, 'Incidents Totaux')
            fig = px.bar(
                top_incidents,
                x='Véhicule',
                y='Incidents Totaux',
                title='Top 10 - Incidents de Conduite',
                color='Score Conduite',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Niveau de risque - répartition
        risk_counts = data['safety']['Niveau Risque'].value_counts()
        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title='Répartition par Niveau de Risque',
            color_discrete_sequence=['#10b981', '#f59e0b', '#dc2626']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Consommation Carburant":
        st.markdown("#### ⛽ Analyse de Consommation")
        
        # Consommation dans le temps
        daily_fuel = data['daily'].groupby('Date')['Carburant Jour (L)'].sum().reset_index()
        fig = px.line(
            daily_fuel,
            x='Date',
            y='Carburant Jour (L)',
            title='Consommation Quotidienne de la Flotte',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top consommateurs
            top_fuel = data['performance'].nlargest(10, 'Carburant Total (L)')
            fig = px.bar(
                top_fuel,
                x='Véhicule',
                y='Carburant Total (L)',
                title='Top 10 - Consommation Totale',
                color='Carburant Total (L)',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Efficacité carburant
            fig = px.scatter(
                data['performance'],
                x='Carburant Total (L)',
                y='Conso Moy (L/100km)',
                color='Type',
                size='Km Parcourus',
                title='Carburant Total vs Consommation Moyenne',
                hover_data=['Véhicule']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:  # Vue d'ensemble
        st.markdown("#### 📊 Vue d'Ensemble de la Flotte")
        
        # KPIs principaux
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Véhicules", len(data['performance']))
        with col2:
            st.metric("Distance Totale", f"{data['performance']['Km Parcourus'].sum():,.0f} km")
        with col3:
            st.metric("Carburant Total", f"{data['performance']['Carburant Total (L)'].sum():,.0f} L")
        with col4:
            st.metric("Alertes Actives", len(data['alerts'][data['alerts']['Statut'] == 'Active']))
        
        # Graphiques combinés
        col1, col2 = st.columns(2)
        
        with col1:
            # Répartition par type
            type_counts = data['performance']['Type'].value_counts()
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title='Répartition par Type de Véhicule'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Alertes par type
            alert_counts = data['alerts']['Type'].value_counts()
            fig = px.bar(
                x=alert_counts.index,
                y=alert_counts.values,
                title='Alertes par Type',
                labels={'x': 'Type', 'y': 'Nombre'}
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 3: CONFIGURATION
# ============================================
with tab3:
    st.markdown("### ⚙️ Configuration du Système")
    
    st.markdown("""
    #### 🎯 Consolidation Réalisée
    
    Ce système a permis de **consolider plus de 30 rapports dispersés** en **8 rapports optimisés** :
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Avantages de la Consolidation:**
        - Réduction de 70% du nombre de rapports
        - Information clé centralisée
        - Indicateurs standardisés
        - Automatisation facilitée
        - Amélioration de la prise de décision
        - Économie de temps significative
        """)
    
    with col2:
        st.markdown("""
        **📊 Données Disponibles:**
        - Trajets détaillés
        - Performance véhicules
        - Sécurité et conduite
        - Maintenance préventive
        - Alertes en temps réel
        - Analyses historiques
        """)
    
    st.markdown("---")
    
    st.markdown("#### 📈 Statistiques du Système")
    
    stats_df = pd.DataFrame({
        "Métrique": [
            "Rapports Consolidés",
            "Anciens Rapports Remplacés",
            "Réduction (%)",
            "Colonnes Disponibles",
            "Véhicules Suivis",
            "Trajets Enregistrés (30j)",
            "Alertes Générées (30j)"
        ],
        "Valeur": [
            "8",
            "30+",
            "70%",
            "84",
            f"{len(data['performance'])}",
            f"{len(data['trips']):,}",
            f"{len(data['alerts']):,}"
        ]
    })
    
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("""
    #### 💾 Export et Sauvegarde
    
    Les rapports peuvent être exportés dans les formats suivants :
    - 📊 **Excel (.xlsx)** - Format structuré avec métadonnées
    - 📄 **CSV (.csv)** - Format texte compatible
    - 📈 **PDF (.pdf)** - Format imprimable (à venir)
    
    #### 🔄 Automatisation
    
    Les rapports peuvent être générés automatiquement selon la fréquence définie :
    - ⏰ **Quotidien** - Envoi automatique à 8h
    - 📅 **Hebdomadaire** - Tous les lundis
    - 📆 **Mensuel** - Le 1er de chaque mois
    - 🔴 **Temps réel** - Mise à jour continue
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <strong>Report Builder TRACK/LIVE</strong> - SOCOCIM Industries © 2025<br>
    Développé pour la consolidation et l'optimisation des rapports de flotte
</div>
""", unsafe_allow_html=True)
