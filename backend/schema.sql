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
    date_of_birth DATE,
    is_active BOOLEAN DEFAULT TRUE,
    diplomas TEXT,
    certifications TEXT,
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
