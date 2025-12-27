# 🚨 IMPORTANT : Créer les tables Supabase AVANT d'initialiser les données

## ⚠️ Problème détecté

L'environnement actuel ne peut pas se connecter directement à Supabase pour créer les tables.
Vous devez **manuellement** créer les tables via le dashboard Supabase.

## 📋 Étape 1 : Créer les tables (OBLIGATOIRE)

### Option A : Via le Dashboard Supabase (RECOMMANDÉ)

1. **Connectez-vous à Supabase**
   - Allez sur : https://supabase.com/dashboard
   - Ou directement : https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod

2. **Ouvrez l'éditeur SQL**
   - Dans le menu de gauche, cliquez sur **"SQL Editor"**
   - Cliquez sur **"+ New query"**

3. **Copiez le schéma SQL**
   - Ouvrez le fichier `/app/backend/schema.sql`
   - Sélectionnez TOUT le contenu (Ctrl+A)
   - Copiez (Ctrl+C)

4. **Exécutez le SQL**
   - Collez le contenu dans l'éditeur SQL Supabase
   - Cliquez sur **"Run"** ou appuyez sur **Ctrl+Enter**
   - Attendez le message **"Success! No rows returned"**

### Option B : Via l'API Supabase (si vous avez la clé service)

Si vous avez votre clé service Supabase avec les permissions administrateur, je peux créer les tables directement. Sinon, utilisez l'Option A.

## 📋 Étape 2 : Créer les buckets de stockage

1. **Dans votre dashboard Supabase**
   - Allez dans **"Storage"** dans le menu de gauche

2. **Créez le bucket "cvs"**
   - Cliquez sur **"New bucket"**
   - Nom : `cvs`
   - ✅ Cochez **"Public bucket"**
   - Cliquez sur **"Create bucket"**

3. **Créez le bucket "avatars"**
   - Cliquez sur **"New bucket"**
   - Nom : `avatars`
   - ✅ Cochez **"Public bucket"**
   - Cliquez sur **"Create bucket"**

## 📋 Étape 3 : Initialiser les données de test

Une fois les tables créées, exécutez le script d'initialisation :

```bash
cd /app/backend
python3 init_db_enriched.py
```

Ce script va créer :
- ✅ 1 super admin (jiby.njaay@gmail.com)
- ✅ 6 entreprises avec identifiants
- ✅ 8 candidats avec identifiants
- ✅ 12 offres d'emploi variées
- ✅ 5 sujets de forum avec réponses
- ✅ 15+ candidatures automatiques
- ✅ 5 bannières publicitaires

## ✅ Vérification

Après avoir exécuté le script, vous devriez voir :

```
🚀 Initialisation enrichie de la base de données kaay-job...

📦 Création des buckets de stockage...
🎨 Insertion des bannières publicitaires...
✅ 5 bannières publicitaires insérées

💬 Création des catégories de forum...
✅ 5 catégories de forum créées

👑 Création du super admin...
✅ Super admin créé: jiby.njaay@gmail.com

🏢 Création des employeurs...
  ✅ Tech Dakar Solutions - recrutement@tech-dakar.sn
  ✅ AfriBanque Sénégal - rh@afribank.sn
  [...]

👨‍💼 Création des candidats...
  ✅ Amadou Diallo - amadou.diallo@gmail.com
  ✅ Fatou Sall - fatou.sall@gmail.com
  [...]

💼 Création des offres d'emploi...
  ✅ Développeur Full Stack React/Node.js (CDI)
  [...]

📝 Création de quelques candidatures...
  ✅ Candidatures créées

💭 Création des posts de forum...
  [...]

✨ Initialisation terminée avec succès!
```

## 🎯 Tester votre site

Une fois les données créées, connectez-vous avec :

**Super Admin :**
- Email : jiby.njaay@gmail.com
- Mot de passe : M@indjibsoN7

**Employeur (exemple) :**
- Email : recrutement@tech-dakar.sn
- Mot de passe : employeur123

**Candidat (exemple) :**
- Email : amadou.diallo@gmail.com
- Mot de passe : candidat123

## 📚 Documentation

- Liste complète des comptes : `/app/COMPTES_TEST.md`
- Liste des emails : `/app/LISTE_EMAILS.txt`
- Guide d'initialisation : `/app/INITIALIZATION_GUIDE.md`

---

**⚠️ RAPPEL : Vous DEVEZ créer les tables dans Supabase avant de pouvoir initialiser les données !**
