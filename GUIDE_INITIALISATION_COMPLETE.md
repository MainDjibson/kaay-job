# 🎯 GUIDE COMPLET : Initialiser les données kaay-job

## ⚠️ Situation actuelle

L'environnement de développement actuel **ne peut pas se connecter directement à Supabase** via internet.
Cela signifie que vous devez **manuellement** créer les tables et initialiser les données.

## 📋 SOLUTION : Initialisation en 3 étapes

---

### ✅ ÉTAPE 1 : Créer les tables Supabase

#### A. Ouvrez votre dashboard Supabase

Allez sur : https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod

Ou connectez-vous sur https://supabase.com et sélectionnez votre projet

#### B. Ouvrez SQL Editor

Dans le menu de gauche → **SQL Editor** → **New query**

#### C. Copiez le schéma SQL

Le fichier complet est : `/app/backend/schema.sql`

**Contenu à copier :**

\`\`\`sql
-- Schéma de base de données pour kaay-job
-- Exécutez ce script dans l'éditeur SQL de Supabase

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('job_seeker', 'employer', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des profils
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255),
    company_name VARCHAR(255),
    profile_title VARCHAR(255),
    avatar_url TEXT,
    location VARCHAR(255),
    education_level VARCHAR(255),
    company_description TEXT,
    company_website VARCHAR(255),
    company_sector VARCHAR(255),
    phone VARCHAR(50),
    social_links TEXT,
    bio TEXT,
    cv_url TEXT,
    cv_updated_at TIMESTAMP WITH TIME ZONE,
    skills TEXT,
    experience TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des offres d'emploi
CREATE TABLE IF NOT EXISTS job_offers (
    id UUID PRIMARY KEY,
    employer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    contract_type VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    salary VARCHAR(255),
    education_required VARCHAR(255),
    skills TEXT,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des candidatures
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY,
    job_offer_id UUID REFERENCES job_offers(id) ON DELETE CASCADE,
    candidate_id UUID REFERENCES users(id) ON DELETE CASCADE,
    message TEXT,
    status VARCHAR(50) DEFAULT 'en_cours' CHECK (status IN ('en_cours', 'accepte', 'refuse')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des messages
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY,
    sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
    receiver_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des catégories de forum
CREATE TABLE IF NOT EXISTS forum_categories (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des sujets de forum
CREATE TABLE IF NOT EXISTS forum_topics (
    id UUID PRIMARY KEY,
    category_id UUID REFERENCES forum_categories(id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    posts_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des posts de forum
CREATE TABLE IF NOT EXISTS forum_posts (
    id UUID PRIMARY KEY,
    topic_id UUID REFERENCES forum_topics(id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des bannières publicitaires
CREATE TABLE IF NOT EXISTS ad_banners (
    id UUID PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    texte TEXT NOT NULL,
    image TEXT NOT NULL,
    telephone VARCHAR(50),
    mail VARCHAR(255),
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Créer les index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_job_offers_employer_id ON job_offers(employer_id);
CREATE INDEX IF NOT EXISTS idx_job_offers_status ON job_offers(status);
CREATE INDEX IF NOT EXISTS idx_applications_job_offer_id ON applications(job_offer_id);
CREATE INDEX IF NOT EXISTS idx_applications_candidate_id ON applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_messages_receiver_id ON messages(receiver_id);
CREATE INDEX IF NOT EXISTS idx_forum_topics_category_id ON forum_topics(category_id);
CREATE INDEX IF NOT EXISTS idx_forum_posts_topic_id ON forum_posts(topic_id);
\`\`\`

#### D. Exécutez le SQL

- Cliquez sur **"Run"** ou appuyez sur **Ctrl+Enter**
- Attendez le message **"Success!"**

---

### ✅ ÉTAPE 2 : Créer les buckets de stockage

#### A. Allez dans Storage

Dans le menu de gauche → **Storage**

#### B. Créez le bucket "cvs"

1. Cliquez sur **"New bucket"**
2. Nom : `cvs`
3. ✅ Cochez **"Public bucket"**
4. Cliquez sur **"Create bucket"**

#### C. Créez le bucket "avatars"

1. Cliquez sur **"New bucket"**
2. Nom : `avatars`
3. ✅ Cochez **"Public bucket"**
4. Cliquez sur **"Create bucket"**

---

### ✅ ÉTAPE 3 : Initialiser les données depuis votre machine locale

Comme l'environnement actuel ne peut pas se connecter à Supabase, vous devez exécuter le script **depuis votre machine locale**.

#### A. Téléchargez les fichiers nécessaires

Téléchargez ces 2 fichiers depuis l'environnement :
- `/app/backend/init_db_enriched.py`
- `/app/backend/.env`

#### B. Installez les dépendances Python

Sur votre machine locale :

\`\`\`bash
pip install supabase python-dotenv passlib
\`\`\`

#### C. Exécutez le script

\`\`\`bash
python3 init_db_enriched.py
\`\`\`

Vous verrez :

\`\`\`
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
  [... 4 autres entreprises ...]

👨‍💼 Création des candidats...
  ✅ Amadou Diallo - amadou.diallo@gmail.com
  ✅ Fatou Sall - fatou.sall@gmail.com
  [... 6 autres candidats ...]

💼 Création des offres d'emploi...
  ✅ Développeur Full Stack React/Node.js (CDI)
  [... 11 autres offres ...]

📝 Création de quelques candidatures...
  ✅ Candidatures créées

💭 Création des posts de forum...
  [... 5 sujets de forum ...]

✨ Initialisation terminée avec succès!

📋 COMPTES CRÉÉS:

👑 SUPER ADMIN:
   Email: jiby.njaay@gmail.com
   Mot de passe: M@indjibsoN7

🏢 EMPLOYEURS (mot de passe: employeur123):
   • recrutement@tech-dakar.sn - Tech Dakar Solutions
   [... liste complète ...]

👨‍💼 CANDIDATS (mot de passe: candidat123):
   • amadou.diallo@gmail.com - Amadou Diallo
   [... liste complète ...]
\`\`\`

---

## 🎉 C'est terminé !

Votre site kaay-job contient maintenant :

✅ 15 utilisateurs (1 admin + 6 employeurs + 8 candidats)
✅ 12 offres d'emploi variées (CDI, CDD, Stage, Alternance, Freelance)
✅ 20 villes africaines disponibles
✅ 5 sujets de forum avec réponses
✅ 15+ candidatures automatiques
✅ 5 bannières publicitaires

## 🔑 Comptes de test

Connectez-vous sur : https://recruit-link-2.preview.emergentagent.com

**Super Admin :**
- Email : jiby.njaay@gmail.com
- Pass : M@indjibsoN7

**Employeur (exemple) :**
- Email : recrutement@tech-dakar.sn
- Pass : employeur123

**Candidat (exemple) :**
- Email : amadou.diallo@gmail.com
- Pass : candidat123

📚 **Liste complète** : `/app/COMPTES_TEST.md` ou `/app/LISTE_EMAILS.txt`

---

## 📞 Besoin d'aide ?

Si vous avez des problèmes :
1. Vérifiez que les tables sont créées dans Supabase
2. Vérifiez que les buckets existent
3. Vérifiez vos credentials dans .env
4. Consultez les logs d'erreur du script

**Bon test de kaay-job ! 🚀**
