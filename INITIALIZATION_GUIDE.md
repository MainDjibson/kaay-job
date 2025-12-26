# 🎉 Guide final d'initialisation de kaay-job

## ✅ Améliorations apportées

1. **Type de contrat "Alternance" ajouté** ✅
2. **Villes du Sénégal et d'Afrique disponibles** ✅
3. **Jeu de données enrichi créé** ✅

## 📊 Contenu du jeu de données enrichi

### 👑 Super Admin
- **Email**: jiby.njaay@gmail.com
- **Mot de passe**: M@indjibsoN7

### 🏢 6 Entreprises (mot de passe: employeur123)
1. Tech Dakar Solutions - recrutement@tech-dakar.sn
2. AfriBanque Sénégal - rh@afribank.sn
3. Sona Cosmetics - jobs@sonacosmetics.sn
4. AgriTech Solutions - contact@agritech-solutions.sn
5. EduCare Africa - recrutement@educare-africa.com
6. Construct BTP Sénégal - hr@constructbtp.sn

### 👨‍💼 8 Candidats (mot de passe: candidat123)
1. Amadou Diallo - amadou.diallo@gmail.com - Développeur Full Stack
2. Fatou Sall - fatou.sall@gmail.com - Responsable Marketing Digital
3. Ousmane Ndiaye - ousmane.ndiaye@gmail.com - Comptable Confirmé
4. Aissatou Ba - aissatou.ba@gmail.com - Designer UI/UX
5. Moussa Fall - moussa.fall@gmail.com - Ingénieur Agronome
6. Marième Diop - marieme.diop@gmail.com - Professeur d'Anglais
7. Ibrahima Sarr - ibrahima.sarr@gmail.com - Chef de Chantier BTP
8. Awa Niang - awa.niang@gmail.com - Data Analyst

### 💼 12 Offres d'emploi variées
- Développeur Full Stack React/Node.js (CDI)
- Responsable Marketing Digital (CDI)
- Comptable (CDI)
- Designer UI/UX (CDD)
- Ingénieur Agronome (CDI)
- Professeur d'Anglais (CDI)
- Chef de Chantier (CDI)
- Data Analyst Junior (CDD)
- Stagiaire Développement Web (Stage)
- Community Manager (Freelance)
- Développeur Mobile Flutter (CDI)
- **Alternance - Assistant RH (Alternance)** ← NOUVEAU TYPE

### 💬 5 Sujets de forum avec réponses
- Comment rédiger un CV qui attire l'attention des recruteurs ?
- Les meilleures formations en ligne pour devenir développeur
- Créer sa startup au Sénégal : par où commencer ?
- Recherche développeur Python pour projet freelance
- Équilibre vie pro / vie perso : vos astuces ?

### 🎨 5 Bannières publicitaires
- Formation Développeur Web
- Boutique Kaay-Tech
- Cabinet RH Talents Plus
- Coworking Dakar Center
- Plateforme E-learning Kaay-Jang

### 🌍 Villes disponibles

**Sénégal (10 villes):**
- Dakar, Thiès, Saint-Louis, Kaolack, Ziguinchor
- Louga, Mbour, Rufisque, Kolda, Tambacounda

**Afrique (20 villes au total):**
- + Abidjan, Lagos, Accra, Nairobi, Kigali
- + Casablanca, Tunis, Alger, Douala, Kinshasa
- + Bamako, Ouagadougou, Abuja, Addis-Abeba, Cotonou
- + Libreville, Yaoundé, Lomé, Conakry

## 🚀 Étapes d'initialisation

### Étape 1 : Créer les tables dans Supabase

1. Connectez-vous à votre dashboard Supabase
2. Allez dans **SQL Editor**
3. Copiez et exécutez le contenu de `/app/backend/schema.sql`
4. Attendez le message "Success!"

### Étape 2 : Créer les buckets de stockage

1. Allez dans **Storage**
2. Créez un bucket `cvs` (cochez Public)
3. Créez un bucket `avatars` (cochez Public)

### Étape 3 : Initialiser les données enrichies

```bash
cd /app/backend
python3 init_db_enriched.py
```

Vous verrez :
```
🚀 Initialisation enrichie de la base de données kaay-job...

📦 Création des buckets de stockage...
🎨 Insertion des bannières publicitaires...
💬 Création des catégories de forum...
👑 Création du super admin...
🏢 Création des employeurs...
👨‍💼 Création des candidats...
💼 Création des offres d'emploi...
📝 Création de quelques candidatures...
💭 Création des posts de forum...

✨ Initialisation terminée avec succès!
```

## 🎯 Tester l'application

### 1. Connexion Super Admin
- Email: `jiby.njaay@gmail.com`
- Mot de passe: `M@indjibsoN7`
- Rôle: Gestion complète, bannières publicitaires

### 2. Connexion Employeur (exemple)
- Email: `recrutement@tech-dakar.sn`
- Mot de passe: `employeur123`
- Tester: Créer offres, voir candidatures

### 3. Connexion Candidat (exemple)
- Email: `amadou.diallo@gmail.com`
- Mot de passe: `candidat123`
- Tester: Postuler, voir offres, messagerie

### 4. Fonctionnalités à tester

✅ **Offres d'emploi**
- Filtrer par type de contrat (CDI, CDD, Stage, **Alternance**, Freelance)
- Filtrer par localisation (villes d'Afrique)
- Voir les détails d'une offre
- Postuler à une offre

✅ **Forum**
- Naviguer dans les catégories
- Lire les sujets existants
- Créer un nouveau sujet
- Répondre à un sujet

✅ **Messagerie**
- Voir les conversations
- Envoyer des messages
- Recevoir des messages

✅ **Bannières publicitaires**
- Observer la rotation toutes les 15 secondes
- Vérifier qu'elles changent aléatoirement

✅ **Page À propos**
- Voir les informations du développeur
- Voir les infos pour la publicité

## 📝 Notes importantes

- Les candidatures sont créées aléatoirement entre candidats et offres
- Chaque compte a un profil complet avec informations réalistes
- Les offres d'emploi couvrent différents secteurs et niveaux
- Le forum contient des discussions réalistes avec réponses

## 🔗 Liens utiles

- **Application**: https://recruit-link-2.preview.emergentagent.com
- **API**: https://recruit-link-2.preview.emergentagent.com/api
- **Supabase Dashboard**: https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod

---

**🎨 Bon test de kaay-job !**
