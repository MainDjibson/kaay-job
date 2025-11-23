# kaay-job - Plateforme de recrutement

## 🎯 Description

**kaay-job** est une plateforme professionnelle de type LinkedIn qui met en relation des chercheurs d'emploi et des employeurs. La plateforme offre une expérience complète avec profils détaillés, offres d'emploi, candidatures, messagerie interne, forum de discussion et bannières publicitaires dynamiques.

## ✨ Fonctionnalités principales

### Pour les chercheurs d'emploi
- Création et gestion de profil complet
- Upload et mise à jour du CV
- Recherche et filtrage d'offres d'emploi
- Candidature en un clic avec lettre de motivation
- Suivi des candidatures
- Messagerie directe avec les recruteurs
- Participation au forum professionnel

### Pour les employeurs
- Profil entreprise détaillé
- Publication et gestion d'offres d'emploi
- Réception et gestion des candidatures
- Accès direct au CV des candidats
- Messagerie avec les candidats
- Changement de statut des candidatures

### Fonctionnalités communes
- Authentification JWT sécurisée
- Forum de discussion par catégories
- Messagerie interne
- Bannière publicitaire rotative (15 secondes)
- Design futuriste et ergonomique
- Interface responsive (mobile/desktop)

### Administration
- Dashboard d'administration
- Statistiques globales
- Gestion des bannières publicitaires
- Gestion des utilisateurs

## 🛠️ Stack Technique

### Backend
- **Framework**: FastAPI (Python)
- **Base de données**: Supabase (PostgreSQL)
- **Authentification**: JWT
- **Storage**: Supabase Storage

### Frontend
- **Framework**: React 19
- **Routing**: React Router DOM
- **Styling**: Tailwind CSS + shadcn/ui
- **HTTP Client**: Axios
- **Notifications**: Sonner

## 🚀 Installation

### 1. Configuration Supabase

1. Connectez-vous à votre dashboard Supabase
2. Allez dans SQL Editor
3. Copiez et exécutez le contenu de `/app/backend/schema.sql`
4. Dans Storage, créez deux buckets publics : `cvs` et `avatars`

### 2. Initialiser les données

```bash
cd /app/backend
python3 init_db.py
```

### 3. Démarrer l'application

```bash
sudo supervisorctl restart backend frontend
```

## 👤 Comptes de test

- **Admin**: admin@kaay-job.sn / admin123
- **Employeur**: recruteur@tech-dakar.sn / recruteur123
- **Candidat**: candidat@example.sn / candidat123

## 📝 Remarques importantes

1. Exécutez d'abord le schéma SQL dans Supabase avant d'initialiser les données
2. Les services sont gérés par supervisord
3. Le frontend est accessible via l'URL configurée dans `.env`

---

Développé avec ❤️ pour kaay-job
