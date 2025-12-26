#!/usr/bin/env python3
"""
Script d'initialisation enrichi de la base de données Supabase pour kaay-job
Crée un jeu de données complet pour tester toutes les fonctionnalités
"""

from supabase import create_client
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

supabase_url = os.environ['SUPABASE_URL']
supabase_key = os.environ['SUPABASE_KEY']
supabase = create_client(supabase_url, supabase_key)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

print("🚀 Initialisation enrichie de la base de données kaay-job...")

# ==================== DONNÉES DE RÉFÉRENCE ====================

# Villes du Sénégal et d'Afrique
VILLES_SENEGAL = [
    "Dakar", "Thiès", "Saint-Louis", "Kaolack", "Ziguinchor",
    "Louga", "Mbour", "Rufisque", "Kolda", "Tambacounda"
]

VILLES_AFRIQUE = VILLES_SENEGAL + [
    "Abidjan, Côte d'Ivoire", "Lagos, Nigeria", "Accra, Ghana",
    "Nairobi, Kenya", "Kigali, Rwanda", "Casablanca, Maroc",
    "Tunis, Tunisie", "Alger, Algérie", "Douala, Cameroun",
    "Kinshasa, RDC", "Bamako, Mali", "Ouagadougou, Burkina Faso"
]

TYPES_CONTRAT = ["CDI", "CDD", "Stage", "Alternance", "Freelance"]

# Entreprises à créer
ENTREPRISES = [
    {
        "email": "recrutement@tech-dakar.sn",
        "company_name": "Tech Dakar Solutions",
        "company_sector": "Technologie & IT",
        "company_description": "Entreprise innovante spécialisée dans le développement logiciel et les solutions digitales pour l'Afrique.",
        "location": "Dakar",
        "company_website": "https://tech-dakar.sn",
        "phone": "+221775551234"
    },
    {
        "email": "rh@afribank.sn",
        "company_name": "AfriBanque Sénégal",
        "company_sector": "Banque & Finance",
        "company_description": "Institution bancaire leader en Afrique de l'Ouest offrant des services financiers innovants.",
        "location": "Dakar",
        "company_website": "https://afribank.sn",
        "phone": "+221775552345"
    },
    {
        "email": "jobs@sonacosmetics.sn",
        "company_name": "Sona Cosmetics",
        "company_sector": "Cosmétiques & Beauté",
        "company_description": "Fabricant de produits cosmétiques naturels pour peaux africaines.",
        "location": "Thiès",
        "company_website": "https://sonacosmetics.sn",
        "phone": "+221775553456"
    },
    {
        "email": "contact@agritech-solutions.sn",
        "company_name": "AgriTech Solutions",
        "company_sector": "Agriculture & Technologie",
        "company_description": "Solutions technologiques innovantes pour l'agriculture moderne en Afrique.",
        "location": "Kaolack",
        "company_website": "https://agritech-solutions.sn",
        "phone": "+221775554567"
    },
    {
        "email": "recrutement@educare-africa.com",
        "company_name": "EduCare Africa",
        "company_sector": "Éducation & Formation",
        "company_description": "Plateforme d'apprentissage en ligne pour l'Afrique francophone.",
        "location": "Dakar",
        "company_website": "https://educare-africa.com",
        "phone": "+221775555678"
    },
    {
        "email": "hr@constructbtp.sn",
        "company_name": "Construct BTP Sénégal",
        "company_sector": "BTP & Construction",
        "company_description": "Entreprise de construction et travaux publics de référence au Sénégal.",
        "location": "Mbour",
        "company_website": "https://constructbtp.sn",
        "phone": "+221775556789"
    }
]

# Candidats à créer
CANDIDATS = [
    {
        "email": "amadou.diallo@gmail.com",
        "password": "candidat123",
        "full_name": "Amadou Diallo",
        "profile_title": "Développeur Full Stack",
        "location": "Dakar",
        "education_level": "Master Informatique",
        "bio": "Passionné par le développement web et mobile, spécialisé en React et Node.js.",
        "skills": "JavaScript, React, Node.js, Python, PostgreSQL, MongoDB",
        "phone": "+221776667788"
    },
    {
        "email": "fatou.sall@gmail.com",
        "password": "candidat123",
        "full_name": "Fatou Sall",
        "profile_title": "Responsable Marketing Digital",
        "location": "Dakar",
        "education_level": "Master Marketing",
        "bio": "Experte en stratégie digitale et réseaux sociaux avec 5 ans d'expérience.",
        "skills": "SEO, SEM, Social Media, Google Analytics, Content Marketing",
        "phone": "+221776668899"
    },
    {
        "email": "ousmane.ndiaye@gmail.com",
        "password": "candidat123",
        "full_name": "Ousmane Ndiaye",
        "profile_title": "Comptable Confirmé",
        "location": "Thiès",
        "education_level": "Licence Comptabilité",
        "bio": "Comptable rigoureux avec expertise en gestion financière et fiscalité.",
        "skills": "Comptabilité générale, Fiscalité, Sage, Excel avancé",
        "phone": "+221776669900"
    },
    {
        "email": "aissatou.ba@gmail.com",
        "password": "candidat123",
        "full_name": "Aissatou Ba",
        "profile_title": "Designer UI/UX",
        "location": "Dakar",
        "education_level": "Licence Design Graphique",
        "bio": "Créative et passionnée par l'expérience utilisateur et le design moderne.",
        "skills": "Figma, Adobe XD, Photoshop, Illustrator, Sketch",
        "phone": "+221776660011"
    },
    {
        "email": "moussa.fall@gmail.com",
        "password": "candidat123",
        "full_name": "Moussa Fall",
        "profile_title": "Ingénieur Agronome",
        "location": "Kaolack",
        "education_level": "Ingénieur Agronome",
        "bio": "Spécialiste en agriculture durable et nouvelles technologies agricoles.",
        "skills": "Agriculture de précision, IoT, Irrigation, Gestion de cultures",
        "phone": "+221776661122"
    },
    {
        "email": "marieme.diop@gmail.com",
        "password": "candidat123",
        "full_name": "Marième Diop",
        "profile_title": "Professeur d'Anglais",
        "location": "Saint-Louis",
        "education_level": "Master Lettres Anglaises",
        "bio": "Enseignante passionnée avec 8 ans d'expérience dans l'enseignement secondaire.",
        "skills": "Pédagogie, Anglais avancé, TOEFL, Gestion de classe",
        "phone": "+221776662233"
    },
    {
        "email": "ibrahima.sarr@gmail.com",
        "password": "candidat123",
        "full_name": "Ibrahima Sarr",
        "profile_title": "Chef de Chantier BTP",
        "location": "Mbour",
        "education_level": "BTS Bâtiment",
        "bio": "Chef de chantier expérimenté, spécialisé dans la construction de bâtiments.",
        "skills": "Gestion de chantier, Lecture de plans, AutoCAD, Management",
        "phone": "+221776663344"
    },
    {
        "email": "awa.niang@gmail.com",
        "password": "candidat123",
        "full_name": "Awa Niang",
        "profile_title": "Data Analyst",
        "location": "Dakar",
        "education_level": "Master Data Science",
        "bio": "Analyste de données passionnée par l'extraction d'insights business.",
        "skills": "Python, R, SQL, Power BI, Machine Learning, Statistics",
        "phone": "+221776664455"
    }
]

# Offres d'emploi variées
OFFRES_EMPLOI = [
    {
        "title": "Développeur Full Stack React/Node.js",
        "description": "Nous recherchons un développeur passionné pour rejoindre notre équipe. Vous travaillerez sur des projets innovants utilisant React, Node.js et PostgreSQL.\n\nResponsabilités :\n- Développer des applications web modernes\n- Participer aux revues de code\n- Collaborer avec l'équipe design\n\nProfil recherché :\n- Expérience en React et Node.js\n- Connaissance de PostgreSQL\n- Esprit d'équipe",
        "contract_type": "CDI",
        "location": "Dakar",
        "salary": "800 000 - 1 200 000 FCFA",
        "education_required": "Licence/Master en Informatique",
        "skills": "React, Node.js, PostgreSQL, Git"
    },
    {
        "title": "Responsable Marketing Digital",
        "description": "Rejoignez notre banque innovante en tant que Responsable Marketing Digital.\n\nMissions :\n- Élaborer la stratégie digitale\n- Gérer les campagnes sur les réseaux sociaux\n- Analyser les performances\n- Manager une équipe de 3 personnes",
        "contract_type": "CDI",
        "location": "Dakar",
        "salary": "1 000 000 - 1 500 000 FCFA",
        "education_required": "Master Marketing/Communication",
        "skills": "SEO, SEM, Social Media, Google Analytics"
    },
    {
        "title": "Comptable",
        "description": "Nous recherchons un comptable confirmé pour notre siège à Thiès.\n\nTâches :\n- Tenue de la comptabilité générale\n- Préparation des déclarations fiscales\n- Suivi de la trésorerie\n- Établissement des bilans",
        "contract_type": "CDI",
        "location": "Thiès",
        "salary": "600 000 - 900 000 FCFA",
        "education_required": "Licence Comptabilité",
        "skills": "Comptabilité générale, Sage, Excel"
    },
    {
        "title": "Designer UI/UX",
        "description": "Créez des expériences utilisateur exceptionnelles pour nos applications web et mobile.\n\nVous serez en charge de :\n- Concevoir des interfaces modernes\n- Réaliser des prototypes\n- Conduire des tests utilisateurs\n- Collaborer avec les développeurs",
        "contract_type": "CDD",
        "location": "Dakar",
        "salary": "600 000 - 900 000 FCFA",
        "education_required": "Licence en Design",
        "skills": "Figma, Adobe XD, Photoshop, Illustrator"
    },
    {
        "title": "Ingénieur Agronome",
        "description": "Rejoignez notre équipe d'AgriTech pour révolutionner l'agriculture africaine.\n\nMissions :\n- Conseiller les agriculteurs sur les techniques modernes\n- Déployer des solutions IoT dans les fermes\n- Former les équipes sur le terrain",
        "contract_type": "CDI",
        "location": "Kaolack",
        "salary": "700 000 - 1 000 000 FCFA",
        "education_required": "Ingénieur Agronome",
        "skills": "Agriculture de précision, IoT, Agronomie"
    },
    {
        "title": "Professeur d'Anglais",
        "description": "Enseignez l'anglais à nos étudiants de niveau secondaire et préparez-les aux examens internationaux.\n\nProfil :\n- Expérience dans l'enseignement\n- Maîtrise parfaite de l'anglais\n- Pédagogue et patient",
        "contract_type": "CDI",
        "location": "Saint-Louis",
        "salary": "450 000 - 650 000 FCFA",
        "education_required": "Master Lettres Anglaises",
        "skills": "Pédagogie, Anglais avancé, TOEFL"
    },
    {
        "title": "Chef de Chantier",
        "description": "Supervisez nos chantiers de construction à Mbour et ses environs.\n\nResponsabilités :\n- Coordonner les équipes de chantier\n- Veiller au respect des délais\n- Assurer la qualité des travaux\n- Gérer les aspects sécurité",
        "contract_type": "CDI",
        "location": "Mbour",
        "salary": "800 000 - 1 100 000 FCFA",
        "education_required": "BTS/Licence Génie Civil",
        "skills": "Gestion de chantier, AutoCAD, Management"
    },
    {
        "title": "Data Analyst Junior",
        "description": "Intégrez notre équipe data et participez à l'analyse de nos données business.\n\nVous apprendrez à :\n- Extraire et nettoyer des données\n- Créer des tableaux de bord\n- Réaliser des analyses statistiques",
        "contract_type": "CDD",
        "location": "Dakar",
        "salary": "500 000 - 700 000 FCFA",
        "education_required": "Licence/Master Data Science",
        "skills": "Python, SQL, Power BI"
    },
    {
        "title": "Stagiaire Développement Web",
        "description": "Stage de 6 mois au sein de notre équipe de développement.\n\nVous travaillerez sur :\n- Le développement de features frontend\n- L'intégration d'APIs\n- Les tests et le debugging",
        "contract_type": "Stage",
        "location": "Dakar",
        "salary": "150 000 FCFA/mois",
        "education_required": "Étudiant en Informatique",
        "skills": "HTML, CSS, JavaScript, Git"
    },
    {
        "title": "Community Manager",
        "description": "Gérez notre présence sur les réseaux sociaux et animez notre communauté.\n\nMissions :\n- Créer du contenu engageant\n- Répondre aux commentaires\n- Analyser les performances\n- Organiser des événements en ligne",
        "contract_type": "Freelance",
        "location": "Dakar",
        "salary": "400 000 - 600 000 FCFA",
        "education_required": "Licence Communication",
        "skills": "Social Media, Content Creation, Canva"
    },
    {
        "title": "Développeur Mobile Flutter",
        "description": "Développez nos applications mobiles avec Flutter.\n\nProfil recherché :\n- Maîtrise de Flutter/Dart\n- Expérience en développement mobile\n- Connaissance des APIs REST",
        "contract_type": "CDI",
        "location": "Dakar",
        "salary": "900 000 - 1 300 000 FCFA",
        "education_required": "Licence/Master Informatique",
        "skills": "Flutter, Dart, Firebase, Git"
    },
    {
        "title": "Alternance - Assistant RH",
        "description": "Contrat d'alternance pour intégrer notre service RH.\n\nVous participerez à :\n- La gestion administrative du personnel\n- Le recrutement\n- La formation\n- L'organisation d'événements internes",
        "contract_type": "Alternance",
        "location": "Dakar",
        "salary": "200 000 FCFA/mois",
        "education_required": "Étudiant Master RH",
        "skills": "RH, Communication, Organisation"
    }
]

# Posts pour le forum
FORUM_POSTS_DATA = [
    {
        "category": "Conseils CV & Carrière",
        "title": "Comment rédiger un CV qui attire l'attention des recruteurs ?",
        "content": "Bonjour à tous,\n\nJe cherche des conseils pour améliorer mon CV. Quels sont les éléments essentiels à ne pas oublier ? Des exemples de CV réussis ?\n\nMerci d'avance !",
        "replies": [
            "Salut ! Voici mes conseils : 1) Sois concis (max 2 pages) 2) Utilise des verbes d'action 3) Quantifie tes résultats 4) Personnalise pour chaque offre",
            "N'oublie pas de mettre en avant tes compétences techniques et soft skills. Le design compte aussi, reste sobre mais moderne.",
        ]
    },
    {
        "category": "Tech & Innovation",
        "title": "Les meilleures formations en ligne pour devenir développeur",
        "content": "Salut la communauté tech !\n\nJe veux me reconvertir dans le développement web. Quelles sont vos recommandations de formations en ligne ?\n\nMerci !",
        "replies": [
            "Je recommande FreeCodeCamp, c'est gratuit et très complet !",
            "Udemy a d'excellents cours, notamment ceux de Maximilian Schwarzmüller pour React.",
            "The Odin Project est excellent aussi, très pratique et orienté projets.",
        ]
    },
    {
        "category": "Entrepreneuriat",
        "title": "Créer sa startup au Sénégal : par où commencer ?",
        "content": "Bonjour entrepreneurs,\n\nJe souhaite lancer ma startup dans la fintech. Quelles sont les démarches administratives ? Des conseils de financement ?\n\nMerci pour votre aide !",
        "replies": [
            "Commence par valider ton idée avec des clients potentiels. Ensuite, regarde du côté de l'APIX pour les démarches.",
            "Pour le financement, il y a des incubateurs comme Jokkolabs et des programmes de la Banque Mondiale.",
        ]
    },
    {
        "category": "Offres & Demandes",
        "title": "Recherche développeur Python pour projet freelance",
        "content": "Bonjour,\n\nJe recherche un développeur Python expérimenté pour un projet de web scraping et automatisation.\n\nBudget : 500k FCFA\nDurée : 2 mois\n\nContactez-moi en MP si intéressé !",
        "replies": []
    },
    {
        "category": "Général",
        "title": "Équilibre vie pro / vie perso : vos astuces ?",
        "content": "Comment gérez-vous l'équilibre entre travail et vie personnelle ?\n\nPartagez vos astuces !",
        "replies": [
            "Je déconnecte complètement après 18h, pas de mails professionnels le soir.",
            "Le sport m'aide beaucoup à décompresser après une journée de travail.",
            "J'utilise la technique Pomodoro pour être plus productif et finir à temps.",
        ]
    }
]

# ==================== CRÉATION DES BUCKETS ====================

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

# ==================== BANNIÈRES PUBLICITAIRES ====================

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

# ==================== CATÉGORIES DE FORUM ====================

print("\n💬 Création des catégories de forum...")
forum_categories = [
    {"id": str(uuid.uuid4()), "name": "Offres & Demandes", "description": "Publiez vos offres d'emploi ou recherches", "created_at": datetime.now(timezone.utc).isoformat()},
    {"id": str(uuid.uuid4()), "name": "Conseils CV & Carrière", "description": "Partagez vos conseils pour réussir sa carrière", "created_at": datetime.now(timezone.utc).isoformat()},
    {"id": str(uuid.uuid4()), "name": "Entrepreneuriat", "description": "Discussions sur l'entrepreneuriat et les startups", "created_at": datetime.now(timezone.utc).isoformat()},
    {"id": str(uuid.uuid4()), "name": "Tech & Innovation", "description": "Actualités tech et innovations", "created_at": datetime.now(timezone.utc).isoformat()},
    {"id": str(uuid.uuid4()), "name": "Général", "description": "Discussions générales", "created_at": datetime.now(timezone.utc).isoformat()}
]

try:
    result = supabase.table("forum_categories").insert(forum_categories).execute()
    print(f"✅ {len(forum_categories)} catégories de forum créées")
    categories_map = {cat["name"]: cat["id"] for cat in result.data}
except Exception as e:
    print(f"ℹ️  Catégories déjà présentes ou erreur: {e}")
    # Récupérer les catégories existantes
    result = supabase.table("forum_categories").select("*").execute()
    categories_map = {cat["name"]: cat["id"] for cat in result.data}

# ==================== SUPER ADMIN ====================

print("\n👑 Création du super admin...")
super_admin_id = str(uuid.uuid4())
super_admin = {
    "id": super_admin_id,
    "email": "jiby.njaay@gmail.com",
    "password": pwd_context.hash("M@indjibsoN7"),
    "role": "admin",
    "created_at": datetime.now(timezone.utc).isoformat()
}

try:
    supabase.table("users").insert(super_admin).execute()
    supabase.table("profiles").insert({
        "id": str(uuid.uuid4()),
        "user_id": super_admin_id,
        "full_name": "Jiby Njaay (Super Admin)",
        "created_at": datetime.now(timezone.utc).isoformat()
    }).execute()
    print(f"✅ Super admin créé: {super_admin['email']}")
except Exception as e:
    print(f"ℹ️  Super admin déjà présent: {e}")

# ==================== EMPLOYEURS ====================

print("\n🏢 Création des employeurs...")
employer_ids = []

for i, emp in enumerate(ENTREPRISES):
    employer_id = str(uuid.uuid4())
    employer_ids.append(employer_id)
    
    try:
        supabase.table("users").insert({
            "id": employer_id,
            "email": emp["email"],
            "password": pwd_context.hash("employeur123"),
            "role": "employer",
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        
        supabase.table("profiles").insert({
            "id": str(uuid.uuid4()),
            "user_id": employer_id,
            "company_name": emp["company_name"],
            "company_sector": emp["company_sector"],
            "company_description": emp["company_description"],
            "location": emp["location"],
            "company_website": emp["company_website"],
            "phone": emp["phone"],
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        
        print(f"  ✅ {emp['company_name']} - {emp['email']}")
    except Exception as e:
        print(f"  ℹ️  {emp['company_name']} déjà présent")

# ==================== CANDIDATS ====================

print("\n👨‍💼 Création des candidats...")
candidate_ids = []

for cand in CANDIDATS:
    candidate_id = str(uuid.uuid4())
    candidate_ids.append(candidate_id)
    
    try:
        supabase.table("users").insert({
            "id": candidate_id,
            "email": cand["email"],
            "password": pwd_context.hash(cand["password"]),
            "role": "job_seeker",
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        
        supabase.table("profiles").insert({
            "id": str(uuid.uuid4()),
            "user_id": candidate_id,
            "full_name": cand["full_name"],
            "profile_title": cand["profile_title"],
            "location": cand["location"],
            "education_level": cand["education_level"],
            "bio": cand["bio"],
            "skills": cand["skills"],
            "phone": cand["phone"],
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        
        print(f"  ✅ {cand['full_name']} - {cand['email']}")
    except Exception as e:
        print(f"  ℹ️  {cand['full_name']} déjà présent")

# ==================== OFFRES D'EMPLOI ====================

print("\n💼 Création des offres d'emploi...")
job_ids = []

for i, job in enumerate(OFFRES_EMPLOI):
    # Assigner l'offre à un employeur de manière cyclique
    employer_id = employer_ids[i % len(employer_ids)] if employer_ids else None
    
    if employer_id:
        job_id = str(uuid.uuid4())
        job_ids.append(job_id)
        
        try:
            supabase.table("job_offers").insert({
                "id": job_id,
                "employer_id": employer_id,
                "title": job["title"],
                "description": job["description"],
                "contract_type": job["contract_type"],
                "location": job["location"],
                "salary": job["salary"],
                "education_required": job["education_required"],
                "skills": job["skills"],
                "status": "active",
                "created_at": datetime.now(timezone.utc).isoformat()
            }).execute()
            
            print(f"  ✅ {job['title']} ({job['contract_type']})")
        except Exception as e:
            print(f"  ℹ️  Erreur création offre: {e}")

# ==================== CANDIDATURES ====================

print("\n📝 Création de quelques candidatures...")
if candidate_ids and job_ids:
    # Créer quelques candidatures aléatoires
    for i in range(min(15, len(candidate_ids) * 2)):
        candidate_id = random.choice(candidate_ids)
        job_id = random.choice(job_ids)
        
        try:
            supabase.table("applications").insert({
                "id": str(uuid.uuid4()),
                "job_offer_id": job_id,
                "candidate_id": candidate_id,
                "message": "Je suis très intéressé par cette opportunité. Mon profil correspond parfaitement aux exigences du poste.",
                "status": random.choice(["en_cours", "en_cours", "accepte", "refuse"]),
                "created_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))).isoformat()
            }).execute()
        except:
            pass  # Ignore duplicates

print(f"  ✅ Candidatures créées")

# ==================== POSTS DE FORUM ====================

print("\n💭 Création des posts de forum...")
for post_data in FORUM_POSTS_DATA:
    category_id = categories_map.get(post_data["category"])
    if not category_id:
        continue
    
    # Choisir un auteur aléatoire
    author_id = random.choice(candidate_ids + employer_ids) if (candidate_ids or employer_ids) else super_admin_id
    
    try:
        topic_id = str(uuid.uuid4())
        supabase.table("forum_topics").insert({
            "id": topic_id,
            "category_id": category_id,
            "author_id": author_id,
            "title": post_data["title"],
            "content": post_data["content"],
            "posts_count": len(post_data["replies"]),
            "created_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60))).isoformat()
        }).execute()
        
        # Créer les réponses
        for reply in post_data["replies"]:
            reply_author = random.choice(candidate_ids + employer_ids) if (candidate_ids or employer_ids) else super_admin_id
            supabase.table("forum_posts").insert({
                "id": str(uuid.uuid4()),
                "topic_id": topic_id,
                "author_id": reply_author,
                "content": reply,
                "created_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))).isoformat()
            }).execute()
        
        print(f"  ✅ {post_data['title']}")
    except Exception as e:
        print(f"  ℹ️  Erreur post forum: {e}")

# ==================== RÉSUMÉ ====================

print("\n" + "="*60)
print("✨ Initialisation terminée avec succès!")
print("="*60)

print("\n📋 COMPTES CRÉÉS:\n")

print("👑 SUPER ADMIN:")
print(f"   Email: jiby.njaay@gmail.com")
print(f"   Mot de passe: M@indjibsoN7")

print("\n🏢 EMPLOYEURS (mot de passe: employeur123):")
for emp in ENTREPRISES:
    print(f"   • {emp['email']} - {emp['company_name']}")

print("\n👨‍💼 CANDIDATS (mot de passe: candidat123):")
for cand in CANDIDATS:
    print(f"   • {cand['email']} - {cand['full_name']}")

print(f"\n📊 STATISTIQUES:")
print(f"   • {len(ENTREPRISES)} entreprises")
print(f"   • {len(CANDIDATS)} candidats")
print(f"   • {len(OFFRES_EMPLOI)} offres d'emploi")
print(f"   • {len(FORUM_POSTS_DATA)} sujets de forum")
print(f"   • 5 bannières publicitaires")
print(f"   • 5 catégories de forum")

print("\n🌍 VILLES DISPONIBLES:")
print(f"   Sénégal: {', '.join(VILLES_SENEGAL)}")
print(f"   Afrique: {len(VILLES_AFRIQUE)} villes au total")

print("\n" + "="*60)
