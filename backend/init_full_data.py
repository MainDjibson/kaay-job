#!/usr/bin/env python3
"""Script d'initialisation complet avec données de test enrichies"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import uuid
from datetime import datetime, timezone, timedelta
import random

MONGO_URL = 'mongodb://localhost:27017'
DB_NAME = 'kaay_job'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

VILLES_AFRIQUE = [
    "Dakar", "Thiès", "Saint-Louis", "Kaolack", "Ziguinchor", "Louga", "Mbour",
    "Abidjan, Côte d'Ivoire", "Lagos, Nigeria", "Accra, Ghana", "Nairobi, Kenya",
    "Kigali, Rwanda", "Casablanca, Maroc", "Tunis, Tunisie", "Alger, Algérie"
]

COMPETENCES_REF = [
    "JavaScript", "Python", "Java", "React", "Angular", "Vue.js", "Node.js",
    "Django", "Flask", "FastAPI", "PostgreSQL", "MongoDB", "MySQL", "AWS", 
    "Azure", "Docker", "Kubernetes", "Git", "CI/CD", "Scrum", "Agile",
    "Marketing Digital", "SEO", "SEM", "Social Media", "Google Analytics",
    "Photoshop", "Illustrator", "Figma", "Adobe XD", "UI/UX Design",
    "Comptabilité", "Fiscalité", "Sage", "Excel", "Finance", "Gestion"
]

POSTS_EXEMPLES = [
    {
        "content": "🎉 Ravi d'annoncer que j'ai commencé un nouveau poste de Développeur Full Stack chez Tech Dakar Solutions ! Hâte de relever de nouveaux défis.",
        "media_type": None
    },
    {
        "content": "📚 Partagez vos meilleurs conseils pour réussir un entretien technique ! Je commence mes recherches d'emploi et j'aimerais avoir vos retours d'expérience.",
        "media_type": None
    },
    {
        "content": "💡 5 astuces pour optimiser votre profil LinkedIn :\n1. Photo professionnelle\n2. Titre accrocheur\n3. Résumé percutant\n4. Expériences détaillées\n5. Recommandations\n\nQu'en pensez-vous ?",
        "media_type": None
    },
    {
        "content": "🚀 Notre entreprise recrute ! Nous recherchons des développeurs passionnés pour rejoindre notre équipe. CDI, salaire compétitif, télétravail possible. Intéressés ? Postulez sur notre page offres !",
        "media_type": None
    },
    {
        "content": "🎓 Je viens d'obtenir ma certification AWS Solutions Architect ! Un an de préparation et beaucoup de pratique. Next step : Kubernetes !",
        "media_type": None
    }
]

COMMENTAIRES_EXEMPLES = [
    "Félicitations ! 🎉",
    "Bravo, c'est mérité !",
    "Super conseil, merci du partage !",
    "Très intéressant, j'ai appris beaucoup de choses.",
    "Je suis totalement d'accord avec toi.",
    "Merci pour ces précieuses informations !",
    "C'est exactement ce que je cherchais.",
    "Excellent post ! Continue comme ça.",
    "Très inspirant, merci !",
    "J'ai une question : comment as-tu fait pour..."
]

async def init_full_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("="*70)
    print("🚀 INITIALISATION COMPLÈTE DE KAAY-JOB")
    print("="*70)
    print("")
    
    # Drop collections
    print("🗑️  Suppression des anciennes données...")
    collections = ['users', 'profiles', 'job_offers', 'applications', 'messages',
                   'forum_categories', 'forum_topics', 'forum_posts', 'ad_banners',
                   'social_posts', 'social_comments', 'social_reactions', 'competences_ref']
    
    for collection in collections:
        await db[collection].drop()
    print("✅ Collections nettoyées\n")
    
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.profiles.create_index("user_id")
    await db.social_posts.create_index([("created_at", -1)])
    
    # === RÉFÉRENTIEL DE COMPÉTENCES ===
    print("📋 Création du référentiel de compétences...")
    for comp in COMPETENCES_REF:
        await db.competences_ref.insert_one({
            "_id": str(uuid.uuid4()),
            "nom": comp,
            "categorie": "Tech" if comp in ["JavaScript", "Python", "React"] else "Autre",
            "created_at": datetime.now(timezone.utc)
        })
    print(f"✅ {len(COMPETENCES_REF)} compétences ajoutées\n")
    
    # === SUPER ADMIN ===
    print("👑 Création du super admin...")
    admin_id = str(uuid.uuid4())
    await db.users.insert_one({
        "_id": admin_id,
        "email": "jiby.njaay@gmail.com",
        "password": pwd_context.hash("M@indjibsoN7"),
        "role": "admin",
        "created_at": datetime.now(timezone.utc)
    })
    
    await db.profiles.insert_one({
        "_id": str(uuid.uuid4()),
        "user_id": admin_id,
        "full_name": "Jiby Njaay",
        "profile_title": "Super Administrateur",
        "bio": "Administrateur de la plateforme kaay-job",
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    })
    print("✅ Admin : jiby.njaay@gmail.com / M@indjibsoN7\n")
    
    # === EMPLOYEURS ===
    print("🏢 Création de 6 employeurs...")
    employeurs = [
        {
            "email": "recrutement@tech-dakar.sn",
            "company_name": "Tech Dakar Solutions",
            "company_sector": "Technologie & IT",
            "company_description": "Leader du développement logiciel en Afrique de l'Ouest",
            "domaine_expertise": "Développement web, mobile, Cloud, IA",
            "chiffre_affaires": "500M FCFA",
            "date_creation": "2020-01-15",
            "effectif": "25-50",
            "location": "Dakar",
            "company_website": "https://tech-dakar.sn",
            "phone": "+221775551234"
        },
        {
            "email": "rh@afribank.sn",
            "company_name": "AfriBanque Sénégal",
            "company_sector": "Banque & Finance",
            "company_description": "Institution bancaire de référence",
            "domaine_expertise": "Services bancaires, Fintech, Microfinance",
            "chiffre_affaires": "15B FCFA",
            "date_creation": "2010-06-01",
            "effectif": "200-500",
            "location": "Dakar",
            "company_website": "https://afribank.sn",
            "phone": "+221775552345"
        },
        {
            "email": "jobs@sonacosmetics.sn",
            "company_name": "Sona Cosmetics",
            "company_sector": "Cosmétiques & Beauté",
            "company_description": "Produits cosmétiques naturels pour peaux africaines",
            "domaine_expertise": "Cosmétiques bio, Soins capillaires",
            "chiffre_affaires": "200M FCFA",
            "date_creation": "2018-03-20",
            "effectif": "10-25",
            "location": "Thiès",
            "company_website": "https://sonacosmetics.sn",
            "phone": "+221775553456"
        },
        {
            "email": "contact@agritech.sn",
            "company_name": "AgriTech Solutions",
            "company_sector": "Agriculture & Technologie",
            "company_description": "Solutions tech pour l'agriculture moderne",
            "domaine_expertise": "IoT agricole, Drones, Irrigation intelligente",
            "chiffre_affaires": "300M FCFA",
            "date_creation": "2019-09-10",
            "effectif": "10-25",
            "location": "Kaolack",
            "company_website": "https://agritech.sn",
            "phone": "+221775554567"
        },
        {
            "email": "recrutement@educare.sn",
            "company_name": "EduCare Africa",
            "company_sector": "Éducation & Formation",
            "company_description": "Plateforme e-learning pour l'Afrique",
            "domaine_expertise": "E-learning, Formation professionnelle",
            "chiffre_affaires": "150M FCFA",
            "date_creation": "2021-01-05",
            "effectif": "10-25",
            "location": "Dakar",
            "company_website": "https://educare.sn",
            "phone": "+221775555678"
        },
        {
            "email": "hr@constructbtp.sn",
            "company_name": "Construct BTP",
            "company_sector": "BTP & Construction",
            "company_description": "Construction et travaux publics",
            "domaine_expertise": "Bâtiment, Génie civil, Routes",
            "chiffre_affaires": "2B FCFA",
            "date_creation": "2015-05-12",
            "effectif": "50-100",
            "location": "Mbour",
            "company_website": "https://constructbtp.sn",
            "phone": "+221775556789"
        }
    ]
    
    employer_ids = []
    for emp in employeurs:
        emp_id = str(uuid.uuid4())
        employer_ids.append(emp_id)
        
        await db.users.insert_one({
            "_id": emp_id,
            "email": emp["email"],
            "password": pwd_context.hash("employeur123"),
            "role": "employer",
            "created_at": datetime.now(timezone.utc)
        })
        
        await db.profiles.insert_one({
            "_id": str(uuid.uuid4()),
            "user_id": emp_id,
            **{k: v for k, v in emp.items() if k != 'email'},
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        })
        
        print(f"  ✅ {emp['company_name']}")
    
    print("")
    
    # === CANDIDATS ===
    print("👨‍💼 Création de 10 candidats...")
    
    candidats = [
        {
            "email": "amadou.diallo@gmail.com",
            "full_name": "Amadou Diallo",
            "profile_title": "Développeur Full Stack",
            "location": "Dakar",
            "education_level": "Master Informatique",
            "date_of_birth": "1995-03-15",
            "phone": "+221776667788",
            "bio": "Développeur passionné avec 3 ans d'expérience",
            "experiences": [
                {
                    "id": str(uuid.uuid4()),
                    "poste": "Développeur Full Stack",
                    "entreprise": "TechCorp Sénégal",
                    "date_debut": "2022-01",
                    "date_fin": None,
                    "en_cours": True,
                    "taches": "Développement d'applications web avec React et Node.js"
                }
            ],
            "diplomes": [
                {
                    "id": str(uuid.uuid4()),
                    "nom": "Master Informatique",
                    "etablissement": "UCAD",
                    "annee": "2020",
                    "domaine": "Génie Logiciel"
                }
            ],
            "certifications": [
                {
                    "id": str(uuid.uuid4()),
                    "nom": "AWS Solutions Architect",
                    "organisme": "Amazon",
                    "date_obtention": "2023-06",
                    "validite": "2026-06"
                }
            ],
            "competences": [
                {"nom": "JavaScript", "niveau": "Expert"},
                {"nom": "React", "niveau": "Expert"},
                {"nom": "Node.js", "niveau": "Avancé"}
            ]
        },
        {
            "email": "fatou.sall@gmail.com",
            "full_name": "Fatou Sall",
            "profile_title": "Responsable Marketing Digital",
            "location": "Dakar",
            "education_level": "Master Marketing",
            "date_of_birth": "1993-07-22",
            "phone": "+221776668899",
            "bio": "Experte en stratégie digitale avec 5 ans d'expérience",
            "experiences": [
                {
                    "id": str(uuid.uuid4()),
                    "poste": "Responsable Marketing",
                    "entreprise": "AgencePro",
                    "date_debut": "2021-03",
                    "date_fin": None,
                    "en_cours": True,
                    "taches": "Stratégie digitale, Gestion réseaux sociaux"
                }
            ],
            "diplomes": [
                {
                    "id": str(uuid.uuid4()),
                    "nom": "Master Marketing Digital",
                    "etablissement": "ISM Dakar",
                    "annee": "2019",
                    "domaine": "Marketing"
                }
            ],
            "certifications": [
                {
                    "id": str(uuid.uuid4()),
                    "nom": "Google Ads Certification",
                    "organisme": "Google",
                    "date_obtention": "2023-01",
                    "validite": "2024-01"
                }
            ],
            "competences": [
                {"nom": "SEO", "niveau": "Expert"},
                {"nom": "Social Media", "niveau": "Expert"}
            ]
        },
        {
            "email": "ousmane.ndiaye@gmail.com",
            "full_name": "Ousmane Ndiaye",
            "profile_title": "Comptable",
            "location": "Thiès",
            "education_level": "Licence Comptabilité",
            "date_of_birth": "1990-11-10",
            "phone": "+221776669900",
            "bio": "Comptable rigoureux avec 8 ans d'expérience",
            "experiences": [],
            "diplomes": [],
            "certifications": [],
            "competences": [
                {"nom": "Comptabilité", "niveau": "Expert"},
                {"nom": "Excel", "niveau": "Avancé"}
            ]
        },
        {
            "email": "aissatou.ba@gmail.com",
            "full_name": "Aissatou Ba",
            "profile_title": "Designer UI/UX",
            "location": "Dakar",
            "education_level": "Licence Design",
            "date_of_birth": "1996-04-18",
            "phone": "+221776660011",
            "bio": "Designer créative spécialisée en UX",
            "experiences": [],
            "diplomes": [],
            "certifications": [],
            "competences": [
                {"nom": "Figma", "niveau": "Expert"},
                {"nom": "UI/UX Design", "niveau": "Avancé"}
            ]
        },
        {
            "email": "moussa.fall@gmail.com",
            "full_name": "Moussa Fall",
            "profile_title": "Ingénieur Agronome",
            "location": "Kaolack",
            "education_level": "Ingénieur Agronome",
            "date_of_birth": "1992-08-25",
            "phone": "+221776661122",
            "bio": "Spécialiste agriculture durable",
            "experiences": [],
            "diplomes": [],
            "certifications": [],
            "competences": []
        }
    ]
    
    # Ajouter 5 candidats supplémentaires simples
    for i in range(5):
        candidats.append({
            "email": f"candidat{i+6}@gmail.com",
            "full_name": f"Candidat Test {i+6}",
            "profile_title": "Professionnel",
            "location": random.choice(VILLES_AFRIQUE),
            "education_level": "Licence",
            "date_of_birth": f"199{random.randint(0,9)}-0{random.randint(1,9)}-{random.randint(10,28)}",
            "phone": f"+22177666{random.randint(1000,9999)}",
            "bio": "Professionnel motivé",
            "experiences": [],
            "diplomes": [],
            "certifications": [],
            "competences": []
        })
    
    candidate_ids = []
    for cand in candidats:
        cand_id = str(uuid.uuid4())
        candidate_ids.append(cand_id)
        
        await db.users.insert_one({
            "_id": cand_id,
            "email": cand["email"],
            "password": pwd_context.hash("candidat123"),
            "role": "job_seeker",
            "created_at": datetime.now(timezone.utc)
        })
        
        await db.profiles.insert_one({
            "_id": str(uuid.uuid4()),
            "user_id": cand_id,
            **{k: v for k, v in cand.items() if k != 'email'},
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        })
        
        print(f"  ✅ {cand['full_name']}")
    
    print("")
    
    # Suite dans la prochaine partie...
    print("✅ Utilisateurs créés : 1 admin + 6 employeurs + 10 candidats = 17 utilisateurs\n")
    
    # === OFFRES D'EMPLOI ===
    print("💼 Création de 15 offres d'emploi...")
    
    jobs = [
        {"title": "Développeur Full Stack React/Node.js", "contract_type": "CDI", "location": "Dakar", "salary": "800k-1.2M FCFA"},
        {"title": "Responsable Marketing Digital", "contract_type": "CDI", "location": "Dakar", "salary": "1M-1.5M FCFA"},
        {"title": "Comptable Confirmé", "contract_type": "CDI", "location": "Thiès", "salary": "600k-900k FCFA"},
        {"title": "Designer UI/UX", "contract_type": "CDD", "location": "Dakar", "salary": "600k-900k FCFA"},
        {"title": "Ingénieur Agronome", "contract_type": "CDI", "location": "Kaolack", "salary": "700k-1M FCFA"},
        {"title": "Professeur d'Anglais", "contract_type": "CDI", "location": "Saint-Louis", "salary": "450k-650k FCFA"},
        {"title": "Chef de Chantier BTP", "contract_type": "CDI", "location": "Mbour", "salary": "800k-1.1M FCFA"},
        {"title": "Data Analyst Junior", "contract_type": "CDD", "location": "Dakar", "salary": "500k-700k FCFA"},
        {"title": "Stagiaire Développement Web", "contract_type": "Stage", "location": "Dakar", "salary": "150k FCFA/mois"},
        {"title": "Community Manager", "contract_type": "Freelance", "location": "Dakar", "salary": "400k-600k FCFA"},
        {"title": "Développeur Mobile Flutter", "contract_type": "CDI", "location": "Dakar", "salary": "900k-1.3M FCFA"},
        {"title": "Alternance - Assistant RH", "contract_type": "Alternance", "location": "Dakar", "salary": "200k FCFA/mois"},
        {"title": "Chef de Projet Digital", "contract_type": "CDI", "location": "Dakar", "salary": "1.2M-1.8M FCFA"},
        {"title": "Développeur Backend Python", "contract_type": "CDI", "location": "Dakar", "salary": "800k-1.2M FCFA"},
        {"title": "Commercial Terrain", "contract_type": "CDD", "location": "Thiès", "salary": "400k + commissions"}
    ]
    
    job_ids = []
    for i, job in enumerate(jobs):
        job_id = str(uuid.uuid4())
        job_ids.append(job_id)
        
        await db.job_offers.insert_one({
            "_id": job_id,
            "employer_id": employer_ids[i % len(employer_ids)],
            **job,
            "description": f"Description détaillée pour {job['title']}. Rejoignez notre équipe dynamique !",
            "education_required": "Bac+3 minimum",
            "skills": "Motivation, Dynamisme, Esprit d'équipe",
            "status": "active",
            "created_at": datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))
        })
    
    print(f"✅ {len(jobs)} offres créées\n")
    
    # === CANDIDATURES ===
    print("📝 Création de candidatures...")
    for _ in range(25):
        await db.applications.insert_one({
            "_id": str(uuid.uuid4()),
            "job_offer_id": random.choice(job_ids),
            "candidate_id": random.choice(candidate_ids),
            "message": "Je suis très motivé pour rejoindre votre équipe.",
            "status": random.choice(["en_cours", "en_cours", "accepte", "refuse"]),
            "created_at": datetime.now(timezone.utc) - timedelta(days=random.randint(1, 20))
        })
    print("✅ 25 candidatures créées\n")
    
    # === PUBLICATIONS (RÉSEAU SOCIAL) ===
    print("📱 Création de publications réseau social...")
    
    all_users = candidate_ids + employer_ids
    post_ids = []
    
    for i, post_data in enumerate(POSTS_EXEMPLES * 3):  # 15 posts
        post_id = str(uuid.uuid4())
        post_ids.append(post_id)
        
        await db.social_posts.insert_one({
            "_id": post_id,
            "author_id": random.choice(all_users),
            "content": post_data["content"],
            "media_url": None,
            "media_type": None,
            "likes_count": random.randint(0, 50),
            "comments_count": random.randint(0, 10),
            "created_at": datetime.now(timezone.utc) - timedelta(days=random.randint(0, 15))
        })
    
    print(f"✅ {len(post_ids)} publications créées\n")
    
    # === COMMENTAIRES ===
    print("💬 Création de commentaires...")
    for _ in range(40):
        await db.social_comments.insert_one({
            "_id": str(uuid.uuid4()),
            "post_id": random.choice(post_ids),
            "author_id": random.choice(all_users),
            "content": random.choice(COMMENTAIRES_EXEMPLES),
            "likes_count": random.randint(0, 20),
            "created_at": datetime.now(timezone.utc) - timedelta(days=random.randint(0, 10))
        })
    print("✅ 40 commentaires créés\n")
    
    # === RÉACTIONS ===
    print("👍 Création de réactions...")
    for _ in range(60):
        await db.social_reactions.insert_one({
            "_id": str(uuid.uuid4()),
            "user_id": random.choice(all_users),
            "target_id": random.choice(post_ids),
            "target_type": "post",
            "reaction_type": random.choice(["like", "love", "support", "celebrate"]),
            "created_at": datetime.now(timezone.utc)
        })
    print("✅ 60 réactions créées\n")
    
    # === BANNIÈRES ===
    print("🎨 Création de 10 bannières publicitaires...")
    banners = [
        {
            "titre": "Formation Développeur Web",
            "texte": "Devenez développeur en 6 mois",
            "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=400&fit=crop",
            "telephone": "+221770001111",
            "mail": "contact@bootcamp.sn",
            "url": "https://bootcamp.sn",
            "is_active": True
        },
        {
            "titre": "Boutique Kaay-Tech",
            "texte": "Matériel informatique à prix imbattables",
            "image": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800&h=400&fit=crop",
            "telephone": "+221770002222",
            "mail": "support@kaaytech.sn",
            "url": "https://kaaytech.sn",
            "is_active": True
        },
        {
            "titre": "Cabinet RH Talents Plus",
            "texte": "Recrutement pour PME et startups",
            "image": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&h=400&fit=crop",
            "telephone": "+221770003333",
            "mail": "contact@talentsplus.sn",
            "url": "https://talentsplus.sn",
            "is_active": True
        },
        {
            "titre": "Coworking Dakar Center",
            "texte": "Espaces de travail modernes",
            "image": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=400&fit=crop",
            "telephone": "+221770004444",
            "mail": "info@coworkdakar.sn",
            "url": "https://coworkdakar.sn",
            "is_active": True
        },
        {
            "titre": "E-learning Kaay-Jang",
            "texte": "500+ cours en ligne certifiés",
            "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=400&fit=crop",
            "telephone": "+221770005555",
            "mail": "hello@kaayjang.sn",
            "url": "https://kaayjang.sn",
            "is_active": True
        },
        {
            "titre": "Digital Marketing Boost",
            "texte": "Augmentez votre visibilité en ligne",
            "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop",
            "telephone": "+221770006666",
            "mail": "contact@digitalboost.sn",
            "url": "https://digitalboost.sn",
            "is_active": False  # Désactivée pour test
        },
        {
            "titre": "Restaurant Le Teranga",
            "texte": "Cuisine sénégalaise authentique",
            "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=400&fit=crop",
            "telephone": "+221770007777",
            "mail": "info@leteranga.sn",
            "url": "https://leteranga.sn",
            "is_active": True
        },
        {
            "titre": "Auto-École Moderne",
            "texte": "Permis B en 30 jours - 92% réussite",
            "image": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&h=400&fit=crop",
            "telephone": "+221770008888",
            "mail": "inscription@autoecole.sn",
            "url": "https://autoecole.sn",
            "is_active": True
        },
        {
            "titre": "Salle de Sport FitZone",
            "texte": "Coach personnel - Essai gratuit 7j",
            "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&h=400&fit=crop",
            "telephone": "+221770009999",
            "mail": "contact@fitzone.sn",
            "url": "https://fitzone.sn",
            "is_active": True
        },
        {
            "titre": "Agence Immobilière DakarHomes",
            "texte": "1000+ biens disponibles à Dakar",
            "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=400&fit=crop",
            "telephone": "+221770010000",
            "mail": "info@dakarhomes.sn",
            "url": "https://dakarhomes.sn",
            "is_active": True
        }
    ]
    
    for banner in banners:
        await db.ad_banners.insert_one({
            "_id": str(uuid.uuid4()),
            **banner,
            "created_at": datetime.now(timezone.utc)
        })
    
    print(f"✅ {len(banners)} bannières créées (1 désactivée pour test)\n")
    
    # === CATÉGORIES FORUM (pour compatibilité) ===
    print("💭 Création des catégories forum...")
    categories = [
        {"name": "Général", "description": "Discussions générales"},
        {"name": "Tech & Innovation", "description": "Actualités tech"},
        {"name": "Carrière", "description": "Conseils carrière"}
    ]
    
    for cat in categories:
        await db.forum_categories.insert_one({
            "_id": str(uuid.uuid4()),
            **cat,
            "created_at": datetime.now(timezone.utc)
        })
    
    print(f"✅ {len(categories)} catégories créées\n")
    
    print("="*70)
    print("✨ INITIALISATION TERMINÉE AVEC SUCCÈS !")
    print("="*70)
    print("")
    print("📊 STATISTIQUES:")
    print(f"   • 17 utilisateurs (1 admin + 6 employeurs + 10 candidats)")
    print(f"   • 15 offres d'emploi")
    print(f"   • 25 candidatures")
    print(f"   • 15 publications réseau social")
    print(f"   • 40 commentaires")
    print(f"   • 60 réactions")
    print(f"   • 10 bannières publicitaires (9 actives, 1 désactivée)")
    print(f"   • {len(COMPETENCES_REF)} compétences dans le référentiel")
    print("")
    print("🔑 COMPTES:")
    print("")
    print("   👑 Admin: jiby.njaay@gmail.com / M@indjibsoN7")
    print("")
    print("   🏢 Employeurs (pass: employeur123):")
    for emp in employeurs[:3]:
        print(f"      • {emp['email']}")
    print("      • ... et 3 autres")
    print("")
    print("   👨‍💼 Candidats (pass: candidat123):")
    for cand in candidats[:5]:
        print(f"      • {cand['email']}")
    print("      • ... et 5 autres")
    print("")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_full_database())
