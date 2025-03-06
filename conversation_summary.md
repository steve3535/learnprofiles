# Résumé de la Conversation - Plateforme d'Évaluation du Profil d'Apprentissage

## Introduction du Projet

Le projet consiste à développer une plateforme web pour évaluer le profil d'apprentissage des jeunes et adolescents dans le cadre d'un coaching familial. Les fonctionnalités principales incluent :

1. Inscription des utilisateurs avec vérification par email
2. Questionnaires avec différents types de questions (QCM, questions ouvertes, jauges)
3. Calcul de scores par catégorie
4. Interface d'administration pour gérer les questions et voir les résultats

Le budget est limité (10-15€) et le projet doit être développé rapidement, avec une interface responsive mais sans nécessairement une version mobile dédiée.

## Architecture Choisie

### Backend
- **Framework**: FastAPI (Python)
- **Base de données**: PostgreSQL sur Railway
- **Authentification**: Système JWT personnalisé
- **Déploiement**: Railway

### Frontend (à venir)
- **Framework**: Next.js (React)
- **CSS**: Tailwind CSS
- **Déploiement**: Vercel

## Structure du Projet Backend