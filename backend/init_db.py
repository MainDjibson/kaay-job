"""
Script d'initialisation de la base de données Supabase pour kaay-job
Ce script crée toutes les tables nécessaires et insère les données de test
"""

from supabase import create_client
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

supabase_url = os.environ['SUPABASE_URL']
supabase_key = os.environ['SUPABASE_KEY']
supabase = create_client(supabase_url, supabase_key)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

print("🚀 Initialisation de la base de données kaay-job...")

# Créer les buckets de stockage
print("\n📦 Création des buckets de stockage...")
try:
    supabase.storage.create_bucket("cvs", {"public": True})
    print("✅ Bucket 'cvs' créé")
except Exception as e:
    print(f"ℹ️  Bucket 'cvs' existe déjà ou erreur: {e}")

try:
    supabase.storage.create_bucket("avatars", {"public": True})
    print("✅ Bucket 'avatars' créé")
except Exception as e:
    print(f"ℹ️  Bucket 'avatars' existe déjà ou erreur: {e}")

# Insérer les 5 bannières publicitaires de test
print("\n🎨 Insertion des bannières publicitaires...")
banners = [
    {
        "id": str(uuid.uuid4()),
        "titre": "Formation Développeur Web",
        "texte": "Apprends à coder ton avenir avec notre bootcamp intensif.",
        "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=400&fit=crop",
        "telephone": "+221770000001",
        "mail": "contact@formationdev.sn",
        "url": "https://formationdev.sn",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Boutique Kaay-Tech",
        "texte": "Matériel informatique, accessoires et gadgets à petits prix.",
        "image": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800&h=400&fit=crop",
        "telephone": "+221770000002",
        "mail": "support@kaaytech.sn",
        "url": "https://kaaytech.sn",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Cabinet RH Talents Plus",
        "texte": "Accompagnement recrutement pour PME et startups africaines.",
        "image": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&h=400&fit=crop",
        "telephone": "+221770000003",
        "mail": "contact@talentsplus.sn",
        "url": "https://talentsplus.sn",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Coworking Dakar Center",
        "texte": "Espace de travail moderne, wifi haut débit, ambiance pro.",
        "image": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=400&fit=crop",
        "telephone": "+221770000004",
        "mail": "info@coworkdakar.sn",
        "url": "https://coworkdakar.sn",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Plateforme E-learning Kaay-Jang",
        "texte": "Cours en ligne pour étudiants, pros et entrepreneurs.",
        "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=400&fit=crop",
        "telephone": "+221770000005",
        "mail": "hello@kaayjang.sn",
        "url": "https://kaayjang.sn",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

try:
    supabase.table("ad_banners").insert(banners).execute()
    print(f"✅ {len(banners)} bannières publicitaires insérées")
except Exception as e:
    print(f"ℹ️  Bannières déjà présentes ou erreur: {e}")

# Créer des catégories de forum
print("\n💬 Création des catégories de forum...")
forum_categories = [
    {
        "id": str(uuid.uuid4()),
        "name": "Offres & Demandes",
        "description": "Publiez vos offres d'emploi ou recherches",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Conseils CV & Carrière",
        "description": "Partagez vos conseils pour réussir sa carrière",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Entrepreneuriat",
        "description": "Discussions sur l'entrepreneuriat et les startups",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Tech & Innovation",
        "description": "Actualités tech et innovations",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Général",
        "description": "Discussions générales",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

try:
    supabase.table("forum_categories").insert(forum_categories).execute()
    print(f"✅ {len(forum_categories)} catégories de forum créées")
except Exception as e:
    print(f"ℹ️  Catégories déjà présentes ou erreur: {e}")

# Créer un utilisateur admin
print("\n👤 Création de l'utilisateur admin...")
admin_id = str(uuid.uuid4())
admin_user = {
    "id": admin_id,
    "email": "admin@kaay-job.sn",
    "password": pwd_context.hash("admin123"),
    "role": "admin",
    "created_at": datetime.now(timezone.utc).isoformat()
}

try:
    supabase.table("users").insert(admin_user).execute()
    
    admin_profile = {
        "id": str(uuid.uuid4()),
        "user_id": admin_id,
        "full_name": "Administrateur kaay-job",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    supabase.table("profiles").insert(admin_profile).execute()
    print("✅ Utilisateur admin créé (email: admin@kaay-job.sn, password: admin123)")
except Exception as e:
    print(f"ℹ️  Admin déjà présent ou erreur: {e}")

# Créer un employeur de test
print("\n🏢 Création d'un employeur de test...")
employer_id = str(uuid.uuid4())
employer_user = {
    "id": employer_id,
    "email": "recruteur@tech-dakar.sn",
    "password": pwd_context.hash("recruteur123"),
    "role": "employer",
    "created_at": datetime.now(timezone.utc).isoformat()
}

try:
    supabase.table("users").insert(employer_user).execute()
    
    employer_profile = {
        "id": str(uuid.uuid4()),
        "user_id": employer_id,
        "company_name": "Tech Dakar Solutions",
        "company_description": "Entreprise innovante spécialisée dans le développement logiciel",
        "company_sector": "Technologie & IT",
        "location": "Dakar, Sénégal",
        "company_website": "https://tech-dakar.sn",
        "phone": "+221775551234",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    supabase.table("profiles").insert(employer_profile).execute()
    print("✅ Employeur créé (email: recruteur@tech-dakar.sn, password: recruteur123)")
    
    # Créer quelques offres d'emploi
    print("💼 Création d'offres d'emploi de test...")
    jobs = [
        {
            "id": str(uuid.uuid4()),
            "employer_id": employer_id,
            "title": "Développeur Full Stack React/Node.js",
            "description": "Nous recherchons un développeur passionné pour rejoindre notre équipe. Vous travaillerez sur des projets innovants utilisant React, Node.js et PostgreSQL.",
            "contract_type": "CDI",
            "location": "Dakar",
            "salary": "800 000 - 1 200 000 FCFA",
            "education_required": "Licence/Master en Informatique",
            "skills": "React, Node.js, PostgreSQL, Git",
            "status": "active",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "employer_id": employer_id,
            "title": "Designer UI/UX",
            "description": "Créez des expériences utilisateur exceptionnelles pour nos applications web et mobile. Maîtrise de Figma requise.",
            "contract_type": "CDD",
            "location": "Dakar",
            "salary": "600 000 - 900 000 FCFA",
            "education_required": "Licence en Design ou équivalent",
            "skills": "Figma, Adobe XD, Photoshop, Illustrator",
            "status": "active",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    supabase.table("job_offers").insert(jobs).execute()
    print(f"✅ {len(jobs)} offres d'emploi créées")
    
except Exception as e:
    print(f"ℹ️  Employeur déjà présent ou erreur: {e}")

# Créer un chercheur d'emploi de test
print("\n👨‍💼 Création d'un chercheur d'emploi de test...")
seeker_id = str(uuid.uuid4())
seeker_user = {
    "id": seeker_id,
    "email": "candidat@example.sn",
    "password": pwd_context.hash("candidat123"),
    "role": "job_seeker",
    "created_at": datetime.now(timezone.utc).isoformat()
}

try:
    supabase.table("users").insert(seeker_user).execute()
    
    seeker_profile = {
        "id": str(uuid.uuid4()),
        "user_id": seeker_id,
        "full_name": "Amadou Diallo",
        "profile_title": "Développeur Web Junior",
        "location": "Dakar, Sénégal",
        "education_level": "Licence en Informatique",
        "bio": "Passionné par le développement web et les nouvelles technologies",
        "skills": "JavaScript, React, Python, FastAPI",
        "phone": "+221776667788",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    supabase.table("profiles").insert(seeker_profile).execute()
    print("✅ Chercheur d'emploi créé (email: candidat@example.sn, password: candidat123)")
    
except Exception as e:
    print(f"ℹ️  Chercheur d'emploi déjà présent ou erreur: {e}")

print("\n✨ Initialisation terminée avec succès!")
print("\n📋 Récapitulatif des comptes de test:")
print("   👑 Admin: admin@kaay-job.sn / admin123")
print("   🏢 Employeur: recruteur@tech-dakar.sn / recruteur123")
print("   👨‍💼 Candidat: candidat@example.sn / candidat123")
