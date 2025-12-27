# 🚨 L'environnement ne peut pas se connecter à Supabase

## Problème

L'environnement Emergent actuel a une restriction DNS qui empêche la connexion directe à Supabase.
C'est pourquoi les comptes n'ont pas pu être créés automatiquement.

## ✅ Solution Simple (5 minutes)

### Étape 1 : Créer les tables dans Supabase (OBLIGATOIRE)

1. Allez sur https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod
2. Cliquez sur **"SQL Editor"** (menu gauche)
3. Cliquez sur **"New query"**
4. **Copiez TOUT le contenu** du fichier `/app/backend/schema.sql`
5. **Collez** dans l'éditeur
6. Cliquez **"Run"** (ou Ctrl+Enter)
7. Attendez le message **"Success!"**

### Étape 2 : Créer les buckets de stockage

1. Dans le menu gauche, cliquez sur **"Storage"**
2. Créez bucket **"cvs"** :
   - Cliquez "New bucket"
   - Nom : cvs
   - ✅ Cochez "Public bucket"
   - Cliquez "Create bucket"
3. Créez bucket **"avatars"** :
   - Cliquez "New bucket"  
   - Nom : avatars
   - ✅ Cochez "Public bucket"
   - Cliquez "Create bucket"

### Étape 3 : Initialiser les données

**Sur votre ordinateur local :**

#### A. Téléchargez les fichiers

Téléchargez ces 2 fichiers depuis l'environnement :
- `/app/backend/init_db_enriched.py`
- `/app/backend/.env`

#### B. Installez les dépendances

Ouvrez un terminal et exécutez :
```bash
pip install supabase python-dotenv passlib
```

#### C. Exécutez le script

```bash
python3 init_db_enriched.py
```

Vous verrez :
```
🚀 Initialisation enrichie de la base de données kaay-job...
📦 Création des buckets de stockage...
✅ Bucket 'cvs' créé
✅ Bucket 'avatars' créé
🎨 Insertion des bannières publicitaires...
✅ 10 bannières publicitaires insérées
...
✨ Initialisation terminée avec succès!
```

## 🎉 Après l'initialisation

Vous pourrez vous connecter sur :
https://recruit-link-2.preview.emergentagent.com

### Comptes disponibles

**Super Admin :**
- Email : jiby.njaay@gmail.com
- Pass : M@indjibsoN7

**Employeur (exemple) :**
- Email : recrutement@tech-dakar.sn
- Pass : employeur123

**Candidat (exemple) :**
- Email : amadou.diallo@gmail.com
- Pass : candidat123

## 📊 Données créées

✅ 1 super admin
✅ 6 employeurs  
✅ 8 candidats
✅ 12 offres d'emploi (CDI, CDD, Stage, Alternance, Freelance)
✅ 10 bannières publicitaires
✅ 5 sujets de forum avec réponses
✅ 15+ candidatures automatiques

## ❓ Pourquoi cette limitation ?

Les environnements Kubernetes Emergent ont des restrictions réseau pour la sécurité.
L'application web elle-même fonctionne parfaitement car elle se connecte via le navigateur de l'utilisateur.
Seule l'initialisation des données doit être faite depuis l'extérieur.

## 📚 Fichiers importants

- `/app/backend/schema.sql` - **SQL à exécuter en premier dans Supabase**
- `/app/backend/init_db_enriched.py` - Script d'initialisation des données
- `/app/COMPTES_TEST.md` - Liste complète de tous les comptes
- `/app/LISTE_EMAILS.txt` - Récapitulatif visuel des emails

---

**Une fois les données initialisées, votre application kaay-job sera 100% fonctionnelle ! 🚀**
