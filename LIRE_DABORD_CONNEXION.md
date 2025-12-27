# 🚨 IMPORTANT : Instructions pour initialiser kaay-job

## ❌ Pourquoi vous ne pouvez pas vous connecter ?

**Les comptes n'existent PAS ENCORE dans la base de données !**

Les tables Supabase doivent être créées et les données initialisées **MANUELLEMENT** car l'environnement actuel ne peut pas se connecter à Supabase via internet.

---

## ✅ Solution en 3 étapes simples

### ÉTAPE 1 : Créer les tables dans Supabase (5 minutes)

1. **Allez sur votre dashboard Supabase** :
   https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod

2. **Ouvrez SQL Editor** (menu de gauche)

3. **Créez une nouvelle requête** et **copiez-collez TOUT le contenu** du fichier :
   `/app/backend/schema.sql`

4. **Cliquez sur "Run"** (ou Ctrl+Enter)

5. **Attendez "Success!"**

### ÉTAPE 2 : Créer les buckets de stockage (2 minutes)

1. **Dans Storage** (menu de gauche)

2. **Créez bucket "cvs"** :
   - New bucket → Nom: `cvs`
   - ✅ Cochez "Public bucket"
   - Create bucket

3. **Créez bucket "avatars"** :
   - New bucket → Nom: `avatars`
   - ✅ Cochez "Public bucket"
   - Create bucket

### ÉTAPE 3 : Initialiser les données (sur votre ordinateur)

**Sur votre machine locale** (pas dans l'environnement) :

1. **Téléchargez ces fichiers** :
   - `/app/backend/init_db_enriched.py`
   - `/app/backend/.env`

2. **Installez les dépendances** :
   ```bash
   pip install supabase python-dotenv passlib
   ```

3. **Exécutez le script** :
   ```bash
   python3 init_db_enriched.py
   ```

---

## 🎉 Résultat attendu

Après l'exécution, vous verrez :

```
✨ Initialisation terminée avec succès!

📋 COMPTES CRÉÉS:

👑 SUPER ADMIN:
   Email: jiby.njaay@gmail.com
   Mot de passe: M@indjibsoN7

🏢 EMPLOYEURS (mot de passe: employeur123):
   • recrutement@tech-dakar.sn
   • rh@afribank.sn
   [... 4 autres]

👨‍💼 CANDIDATS (mot de passe: candidat123):
   • amadou.diallo@gmail.com
   • fatou.sall@gmail.com
   [... 6 autres]
```

---

## 🔑 Données créées

### ✅ 15 Utilisateurs
- 1 super admin
- 6 employeurs
- 8 candidats

### ✅ 12 Offres d'emploi
- CDI, CDD, Stage, Alternance, Freelance
- Secteurs variés (Tech, Finance, BTP, etc.)
- 20 villes africaines

### ✅ 10 Bannières publicitaires
1. Formation Développeur Web - Bootcamp 2025
2. Boutique Kaay-Tech - Matériel Informatique
3. Cabinet RH Talents Plus
4. Coworking Dakar Center
5. Kaay-Jang E-learning
6. Agence Digital Marketing Boost
7. Restaurant Le Teranga
8. Auto-École Moderne Dakar
9. Salle de Sport FitZone
10. Agence Immobilière DakarHomes

### ✅ 5 Sujets de forum avec réponses

### ✅ 15+ Candidatures automatiques

---

## 🆕 Nouvelles fonctionnalités ajoutées

### Page Offres d'emploi améliorée
- ✅ Types de contrat avec boutons blancs en surbrillance
- ✅ Au survol : police noire avec surbrillage blanc
- ✅ Auto-complétion pour la localisation (20 villes africaines)

### Page Inscription améliorée
- ✅ Radio buttons chercheur/employeur mis en exergue
- ✅ Couleurs différentes (cyan/violet)

### Bannière publicitaire
- ✅ Pleine largeur de la page
- ✅ Apparaît sur toutes les pages sous le menu
- ✅ Design amélioré avec plus d'espace

### Profil amélioré
- ✅ Lien "Profil" dans le menu (entre Forum et À propos)
- ✅ Pour candidats : date de naissance, expériences, CV, diplômes, certifications, champ actif
- ✅ Mise à jour du schéma de base de données

### Administration des bannières
- ✅ Créer/Modifier bannières
- ✅ Activer/Désactiver bannières
- ✅ Seules les bannières actives sont affichées

---

## 🔗 Liens utiles

- **Application** : https://recruit-link-2.preview.emergentagent.com
- **API** : https://recruit-link-2.preview.emergentagent.com/api
- **Supabase Dashboard** : https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod

---

## 📚 Documentation

- `/app/GUIDE_INITIALISATION_COMPLETE.md` - Guide détaillé complet
- `/app/COMPTES_TEST.md` - Liste de tous les comptes avec détails
- `/app/LISTE_EMAILS.txt` - Tableau récapitulatif visuel
- `/app/backend/schema.sql` - **FICHIER SQL À EXÉCUTER EN PREMIER**

---

## ⚠️ Important

**VOUS NE POURREZ PAS VOUS CONNECTER** tant que :
1. Les tables ne sont pas créées dans Supabase
2. Le script d'initialisation n'est pas exécuté

Une fois ces étapes faites, TOUS les comptes fonctionneront ! 🎉
