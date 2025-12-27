#!/usr/bin/env python3
"""Script d'initialisation MongoDB pour kaay-job"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import uuid
from datetime import datetime, timezone, timedelta
import random

MONGO_URL = 'mongodb://localhost:27017'
DB_NAME = 'kaay_job'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Villes africaines
VILLES_AFRIQUE = [
    "Dakar", "Thiès", "Saint-Louis", "Kaolack", "Ziguinchor",
    "Abidjan, Côte d'Ivoire", "Lagos, Nigeria", "Accra, Ghana",
    "Nairobi, Kenya", "Kigali, Rwanda", "Casablanca, Maroc"
]

async def init_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🚀 Initialisation de la base de données MongoDB kaay-job...")
    print("")
    
    # Drop existing collections
    print("🗑️  Suppression des anciennes données...")
    for collection in ['users', 'profiles', 'job_offers', 'applications', 'messages', 
                       'forum_categories', 'forum_topics', 'forum_posts', 'ad_banners']:
        await db[collection].drop()
    
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.profiles.create_index("user_id")
    
    print("✅ Collections réinitialisées\n")
    
    # Super Admin
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
        "full_name": "Jiby Njaay (Super Admin)",
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    })
    
    print(f"✅ Admin créé: jiby.njaay@gmail.com / M@indjibsoN7\n")
    
    # Employeurs
    print("🏢 Création des employeurs...")
    employeurs = [
        {
            "email": "recrutement@tech-dakar.sn",
            "company_name": "Tech Dakar Solutions",
            "company_sector": "Technologie & IT",
            "company_description": "Entreprise innovante spécialisée dans le développement logiciel",
            "domaine_expertise": "Développement web et mobile, Cloud, IA",
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
            "company_description": "Institution bancaire leader en Afrique de l'Ouest",
            "domaine_expertise": "Services bancaires, Fintech, Microfinance",
            "chiffre_affaires": "15B FCFA",
            "date_creation": "2010-06-01",
            "effectif": "200-500",
            "location": "Dakar",
            "company_website": "https://afribank.sn",
            "phone": "+221775552345"
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
        
        print(f"  ✅ {emp['company_name']} - {emp['email']}")
    
    print("")
    
    # Candidats
    print("👨‍💼 Création des candidats...")
    candidats = [
        {
            "email": "amadou.diallo@gmail.com",
            "full_name": "Amadou Diallo",
            "profile_title": "Développeur Full Stack",
            "location": "Dakar",
            "education_level": "Master Informatique",
            "bio": "Passionné par le développement web et mobile",
            "phone": "+221776667788",
            "date_of_birth": "1995-03-15",
            "experiences": [
                {
                    "id": str(uuid.uuid4()),
                    "poste": "Développeur Full Stack",
                    "entreprise": "TechCorp Sénégal",
                    "date_debut": "2022-01",
                    "date_fin": None,
                    "en_cours": True,
                    "taches": "Développement d'applications web avec React et Node.js, Gestion de bases de données PostgreSQL"
                },
                {
                    "id": str(uuid.uuid4()),
                    "poste": "Développeur Junior",
                    "entreprise": "Digital Agency",
                    "date_debut": "2020-06",
                    "date_fin": "2021-12",
                    "en_cours": False,
                    "taches": "Intégration de maquettes, Développement frontend"
                }
            ],
            "diplomes": [
                {
                    "id": str(uuid.uuid4()),
                    "nom": "Master Informatique",
                    "etablissement": "Université Cheikh Anta Diop",
                    "annee": "2020",
                    "domaine": "Génie Logiciel"
                },
                {
                    "id": str(uuid.uuid4()),
                    "nom": "Licence Informatique",
                    "etablissement": "UCAD",
                    "annee": "2018",
                    "domaine": "Informatique Générale"
                }
            ],
            "certifications": [
                {
                    "id": str(uuid.uuid4()),
                    "nom": "AWS Certified Developer",
                    "organisme": "Amazon Web Services",
                    "date_obtention": "2023-06",
                    "validite": "2026-06"
                }
            ],
            "competences": [
                {"nom": "JavaScript", "niveau": "Expert"},
                {"nom": "React", "niveau": "Expert"},
                {"nom": "Node.js", "niveau": "Avancé"},
                {"nom": "Python", "niveau": "Intermédiaire"},
                {"nom": "PostgreSQL", "niveau": "Avancé"}
            ]
        },
        {
            "email": "fatou.sall@gmail.com",
            "full_name": "Fatou Sall",
            "profile_title": "Responsable Marketing Digital",
            "location": "Dakar",
            "education_level": "Master Marketing",
            "bio": "Experte en stratégie digitale et réseaux sociaux",
            "phone": "+221776668899",
            "date_of_birth": "1993-07-22",
            "experiences": [
                {
                    "id": str(uuid.uuid4()),
                    "poste": "Responsable Marketing Digital",
                    "entreprise": "AgencePro",
                    "date_debut": "2021-03",
                    "date_fin": None,
                    "en_cours": True,
                    "taches": "Gestion des campagnes digitales, Stratégie social media, Analyse de performance"
                }
            ],
            "diplomes": [
                {
                    "id": str(uuid.uuid4()),
                    "nom": "Master Marketing Digital",
                    "etablissement": "ISM Dakar",
                    "annee": "2019",
                    "domaine": "Marketing & Communication"
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
                {"nom": "Google Ads", "niveau": "Expert"},
                {"nom": "Social Media", "niveau": "Expert"},
                {"nom": "Analytics", "niveau": "Avancé"}
            ]
        }
    ]
    
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
        
        print(f"  ✅ {cand['full_name']} - {cand['email']}")
    
    print("")
    
    # Offres d'emploi
    print("💼 Création des offres d'emploi...")
    jobs = [
        {
            "title": "Développeur Full Stack React/Node.js",
            "description": "Rejoignez notre équipe et travaillez sur des projets innovants",
            "contract_type": "CDI",
            "location": "Dakar",
            "salary": "800 000 - 1 200 000 FCFA",
            "education_required": "Master Informatique",
            "skills": "React, Node.js, PostgreSQL"
        },
        {
            "title": "Responsable Marketing Digital",
            "description": "Élaborez notre stratégie digitale",
            "contract_type": "CDI",
            "location": "Dakar",
            "salary": "1 000 000 - 1 500 000 FCFA",
            "education_required": "Master Marketing",
            "skills": "SEO, SEM, Social Media"
        },
        {
            "title": "Stagiaire Développement Web",
            "description": "Stage de 6 mois en développement web",
            "contract_type": "Stage",
            "location": "Dakar",
            "salary": "150 000 FCFA/mois",
            "education_required": "Licence Informatique",
            "skills": "HTML, CSS, JavaScript"
        },
        {
            "title": "Alternance - Assistant RH",
            "description": "Contrat d'alternance en ressources humaines",
            "contract_type": "Alternance",
            "location": "Dakar",
            "salary": "200 000 FCFA/mois",
            "education_required": "Master RH",
            "skills": "Communication, Organisation"
        }
    ]
    
    for i, job in enumerate(jobs):
        await db.job_offers.insert_one({
            "_id": str(uuid.uuid4()),
            "employer_id": employer_ids[i % len(employer_ids)],
            **job,
            "status": "active",
            "created_at": datetime.now(timezone.utc)
        })
        print(f"  ✅ {job['title']}")
    
    print("")
    
    # Bannières
    print("🎨 Création des bannières publicitaires...")
    banners = [
        {
            "titre": "Formation Développeur Web - Bootcamp 2025",
            "texte": "Devenez développeur web en 6 mois",
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
        }
    ]
    
    for banner in banners:
        await db.ad_banners.insert_one({
            "_id": str(uuid.uuid4()),
            **banner,
            "created_at": datetime.now(timezone.utc)
        })
    
    print(f"✅ {len(banners)} bannières créées\n")
    
    # Catégories forum
    print("💬 Création des catégories de forum...")
    categories = [
        {"name": "Offres & Demandes", "description": "Publiez vos offres"},
        {"name": "Conseils CV & Carrière", "description": "Conseils carrière"},
        {"name": "Tech & Innovation", "description": "Actualités tech"}
    ]
    
    for cat in categories:
        await db.forum_categories.insert_one({
            "_id": str(uuid.uuid4()),
            **cat,
            "created_at": datetime.now(timezone.utc)
        })
    
    print(f"✅ {len(categories)} catégories créées\n")
    
    print("="*70)
    print("✨ Initialisation terminée avec succès!")
    print("="*70)
    print("")
    print("📧 COMPTES CRÉÉS:")
    print("")
    print("👑 Super Admin:")
    print("   Email: jiby.njaay@gmail.com")
    print("   Pass:  M@indjibsoN7")
    print("")
    print("🏢 Employeurs (pass: employeur123):")
    print("   recrutement@tech-dakar.sn")
    print("   rh@afribank.sn")
    print("")
    print("👨‍💼 Candidats (pass: candidat123):")
    print("   amadou.diallo@gmail.com")
    print("   fatou.sall@gmail.com")
    print("")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_database())
