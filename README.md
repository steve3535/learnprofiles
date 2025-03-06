# Plateforme d'Évaluation du Profil d'Apprentissage

Une plateforme web pour évaluer le profil d'apprentissage des jeunes et adolescents dans le cadre d'un coaching familial.

## Fonctionnalités

- Inscription des utilisateurs avec vérification par email
- Questionnaires avec différents types de questions (QCM, questions ouvertes, jauges)
- Calcul de scores par catégorie
- Interface d'administration pour gérer les questions et voir les résultats

## Structure du Projet

- `backend/` : API FastAPI
- `frontend/` : Application Next.js (à venir)

## Prérequis

- Python 3.9+
- PostgreSQL
- Node.js 14+ (pour le frontend)

## Installation

### Backend

1. Cloner le dépôt
   ```
   git clone <repo-url>
   cd <repo-directory>
   ```

2. Installer les dépendances
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Configurer les variables d'environnement
   ```
   cp .env.example .env
   # Modifier les valeurs dans .env
   ```

4. Exécuter les migrations
   ```
   alembic upgrade head
   ```

5. Démarrer le serveur
   ```
   python run.py
   ```

### Frontend (à venir)

## Déploiement

### Backend

Le backend peut être déployé sur Railway :

1. Connectez-vous à Railway
2. Créez un nouveau projet
3. Ajoutez un service PostgreSQL
4. Ajoutez un service depuis GitHub
5. Configurez les variables d'environnement

### Frontend

Le frontend peut être déployé sur Vercel :

1. Connectez-vous à Vercel
2. Importez le projet depuis GitHub
3. Configurez les variables d'environnement

## Licence

Ce projet est sous licence MIT.