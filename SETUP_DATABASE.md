# Configuration de la base de données Supabase pour kaay-job

## Étape 1 : Créer les tables dans Supabase

1. Connectez-vous à votre dashboard Supabase : https://zlgxkhgvkslyksfjjqod.supabase.co
2. Allez dans l'éditeur SQL (SQL Editor)
3. Copiez et exécutez le contenu du fichier `/app/backend/schema.sql`

Le fichier `schema.sql` contient toutes les tables nécessaires :
- users
- profiles
- job_offers
- applications
- messages
- forum_categories
- forum_topics
- forum_posts
- ad_banners

## Étape 2 : Créer les buckets de stockage

Dans votre dashboard Supabase :
1. Allez dans Storage
2. Créez deux buckets :
   - `cvs` (public)
   - `avatars` (public)

## Étape 3 : Insérer les données de test

Une fois les tables créées, exécutez le script d'initialisation :

```bash
cd /app/backend
python3 init_db.py
```

Ce script va créer :
- 5 bannières publicitaires de test
- 5 catégories de forum
- 1 utilisateur admin (admin@kaay-job.sn / admin123)
- 1 employeur de test (recruteur@tech-dakar.sn / recruteur123)
- 1 chercheur d'emploi de test (candidat@example.sn / candidat123)
- 2 offres d'emploi de test

## Comptes de test

Après l'initialisation, vous pouvez vous connecter avec :

**Admin:**
- Email: admin@kaay-job.sn
- Mot de passe: admin123

**Employeur:**
- Email: recruteur@tech-dakar.sn
- Mot de passe: recruteur123

**Candidat:**
- Email: candidat@example.sn
- Mot de passe: candidat123

## Vérification

Pour vérifier que tout fonctionne, testez l'API backend :

```bash
# Test de connexion
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@kaay-job.sn","password":"admin123"}'

# Test des bannières
curl http://localhost:8001/api/banners
```
