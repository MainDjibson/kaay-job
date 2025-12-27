from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import random
import base64

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'kaay_job'
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# JWT configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'kaay-job-secret-key-2025')
JWT_ALGORITHM = 'HS256'
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 10080

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

app = FastAPI()
api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================

class Experience(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    poste: str
    entreprise: str
    date_debut: str
    date_fin: Optional[str] = None
    en_cours: bool = False
    taches: Optional[str] = None
    
class Diplome(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nom: str
    etablissement: str
    annee: str
    domaine: Optional[str] = None

class Certification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nom: str
    organisme: str
    date_obtention: str
    validite: Optional[str] = None

class Competence(BaseModel):
    nom: str
    niveau: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    role: str

class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    profile_title: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    education_level: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    cv_url: Optional[str] = None
    date_of_birth: Optional[str] = None
    is_active: Optional[bool] = True
    experiences: Optional[List[Experience]] = []
    diplomes: Optional[List[Diplome]] = []
    certifications: Optional[List[Certification]] = []
    competences: Optional[List[Competence]] = []
    company_sector: Optional[str] = None
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    domaine_expertise: Optional[str] = None
    chiffre_affaires: Optional[str] = None
    date_creation: Optional[str] = None
    effectif: Optional[str] = None

class JobOfferCreate(BaseModel):
    title: str
    description: str
    contract_type: str
    location: str
    salary: Optional[str] = None
    education_required: Optional[str] = None
    skills: Optional[str] = None

class ApplicationCreate(BaseModel):
    job_offer_id: str
    message: Optional[str] = None

class MessageCreate(BaseModel):
    receiver_id: str
    content: str

class ForumTopicCreate(BaseModel):
    category_id: str
    title: str
    content: str

class ForumPostCreate(BaseModel):
    topic_id: str
    content: str

class AdBannerCreate(BaseModel):
    titre: str
    texte: str
    image: str
    telephone: str
    mail: str
    url: str
    is_active: Optional[bool] = True

# ==================== HELPERS ====================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        
        user = await db.users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if key == '_id':
                result['id'] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, list):
                result[key] = serialize_doc(value)
            elif isinstance(value, dict):
                result[key] = serialize_doc(value)
            else:
                result[key] = value
        return result
    return doc

# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "Bienvenue sur l'API kaay-job (MongoDB)"}

# AUTH
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    user_id = str(uuid.uuid4())
    user = {
        "_id": user_id,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "role": user_data.role,
        "created_at": datetime.now(timezone.utc)
    }
    await db.users.insert_one(user)
    
    profile = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "full_name": user_data.full_name or "",
        "company_name": user_data.company_name or "",
        "experiences": [],
        "diplomes": [],
        "certifications": [],
        "competences": [],
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
    await db.profiles.insert_one(profile)
    
    access_token = create_access_token(data={"sub": user_id, "role": user_data.role})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user_id, "role": user_data.role}

@api_router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await db.users.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = create_access_token(data={"sub": user["_id"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user["_id"], "role": user["role"]}

@api_router.get("/auth/me")
async def get_me(current_user = Depends(get_current_user)):
    return serialize_doc(current_user)

# PROFILES
@api_router.get("/profiles/me")
async def get_my_profile(current_user = Depends(get_current_user)):
    profile = await db.profiles.find_one({"user_id": current_user["_id"]})
    if not profile:
        raise HTTPException(status_code=404, detail="Profil non trouvé")
    return serialize_doc(profile)

@api_router.put("/profiles/me")
async def update_profile(profile_data: ProfileBase, current_user = Depends(get_current_user)):
    update_data = profile_data.model_dump(exclude_unset=True, exclude_none=True)
    await db.profiles.update_one({"user_id": current_user["_id"]}, {"$set": update_data})
    profile = await db.profiles.find_one({"user_id": current_user["_id"]})
    return serialize_doc(profile)

@api_router.get("/profiles/{user_id}")
async def get_profile(user_id: str):
    profile = await db.profiles.find_one({"user_id": user_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profil non trouvé")
    return serialize_doc(profile)

# JOBS
@api_router.post("/jobs")
async def create_job(job_data: JobOfferCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Seuls les employeurs peuvent créer des offres")
    
    job = {
        "_id": str(uuid.uuid4()),
        "employer_id": current_user["_id"],
        **job_data.model_dump(),
        "status": "active",
        "created_at": datetime.now(timezone.utc)
    }
    await db.job_offers.insert_one(job)
    return serialize_doc(job)

@api_router.get("/jobs")
async def get_jobs(search: Optional[str] = None, location: Optional[str] = None, contract_type: Optional[str] = None):
    query = {"status": "active"}
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if contract_type:
        query["contract_type"] = contract_type
    
    jobs = await db.job_offers.find(query).sort("created_at", -1).to_list(100)
    return serialize_doc(jobs)

@api_router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await db.job_offers.find_one({"_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return serialize_doc(job)

# APPLICATIONS
@api_router.post("/applications")
async def apply_to_job(app_data: ApplicationCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "job_seeker":
        raise HTTPException(status_code=403, detail="Seuls les chercheurs d'emploi peuvent postuler")
    
    existing = await db.applications.find_one({"job_offer_id": app_data.job_offer_id, "candidate_id": current_user["_id"]})
    if existing:
        raise HTTPException(status_code=400, detail="Vous avez déjà postulé")
    
    application = {
        "_id": str(uuid.uuid4()),
        "job_offer_id": app_data.job_offer_id,
        "candidate_id": current_user["_id"],
        "message": app_data.message,
        "status": "en_cours",
        "created_at": datetime.now(timezone.utc)
    }
    await db.applications.insert_one(application)
    return serialize_doc(application)

@api_router.get("/applications/me")
async def get_my_applications(current_user = Depends(get_current_user)):
    apps = await db.applications.find({"candidate_id": current_user["_id"]}).sort("created_at", -1).to_list(100)
    return serialize_doc(apps)

# MESSAGES
@api_router.post("/messages")
async def send_message(msg_data: MessageCreate, current_user = Depends(get_current_user)):
    message = {
        "_id": str(uuid.uuid4()),
        "sender_id": current_user["_id"],
        "receiver_id": msg_data.receiver_id,
        "content": msg_data.content,
        "is_read": False,
        "created_at": datetime.now(timezone.utc)
    }
    await db.messages.insert_one(message)
    return serialize_doc(message)

@api_router.get("/messages/unread/count")
async def get_unread_count(current_user = Depends(get_current_user)):
    count = await db.messages.count_documents({"receiver_id": current_user["_id"], "is_read": False})
    return {"count": count}

# FORUM
@api_router.get("/forum/categories")
async def get_forum_categories():
    categories = await db.forum_categories.find().to_list(100)
    return serialize_doc(categories)

@api_router.post("/forum/topics")
async def create_topic(topic_data: ForumTopicCreate, current_user = Depends(get_current_user)):
    topic = {
        "_id": str(uuid.uuid4()),
        "category_id": topic_data.category_id,
        "author_id": current_user["_id"],
        "title": topic_data.title,
        "content": topic_data.content,
        "posts_count": 0,
        "created_at": datetime.now(timezone.utc)
    }
    await db.forum_topics.insert_one(topic)
    return serialize_doc(topic)

@api_router.get("/forum/topics")
async def get_topics(category_id: Optional[str] = None):
    query = {}
    if category_id:
        query["category_id"] = category_id
    topics = await db.forum_topics.find(query).sort("created_at", -1).to_list(100)
    return serialize_doc(topics)

@api_router.get("/forum/topics/{topic_id}")
async def get_topic(topic_id: str):
    topic = await db.forum_topics.find_one({"_id": topic_id})
    if not topic:
        raise HTTPException(status_code=404, detail="Sujet non trouvé")
    return serialize_doc(topic)

@api_router.post("/forum/posts")
async def create_post(post_data: ForumPostCreate, current_user = Depends(get_current_user)):
    post = {
        "_id": str(uuid.uuid4()),
        "topic_id": post_data.topic_id,
        "author_id": current_user["_id"],
        "content": post_data.content,
        "created_at": datetime.now(timezone.utc)
    }
    await db.forum_posts.insert_one(post)
    await db.forum_topics.update_one({"_id": post_data.topic_id}, {"$inc": {"posts_count": 1}})
    return serialize_doc(post)

@api_router.get("/forum/posts/{topic_id}")
async def get_posts(topic_id: str):
    posts = await db.forum_posts.find({"topic_id": topic_id}).sort("created_at", 1).to_list(100)
    return serialize_doc(posts)

# BANNERS
@api_router.get("/banners/active")
async def get_active_banners():
    banners = await db.ad_banners.find({"is_active": True}).to_list(100)
    return serialize_doc(banners)

@api_router.get("/banners")
async def get_all_banners():
    banners = await db.ad_banners.find().to_list(100)
    return serialize_doc(banners)

@api_router.post("/banners")
async def create_banner(banner_data: AdBannerCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seuls les admins peuvent créer des bannières")
    
    banner = {
        "_id": str(uuid.uuid4()),
        **banner_data.model_dump(),
        "created_at": datetime.now(timezone.utc)
    }
    await db.ad_banners.insert_one(banner)
    return serialize_doc(banner)

@api_router.put("/banners/{banner_id}")
async def update_banner(banner_id: str, banner_data: AdBannerCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seuls les admins peuvent modifier des bannières")
    
    await db.ad_banners.update_one({"_id": banner_id}, {"$set": banner_data.model_dump()})
    banner = await db.ad_banners.find_one({"_id": banner_id})
    return serialize_doc(banner)

@api_router.patch("/banners/{banner_id}/toggle")
async def toggle_banner(banner_id: str, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seuls les admins peuvent modifier des bannières")
    
    banner = await db.ad_banners.find_one({"_id": banner_id})
    if not banner:
        raise HTTPException(status_code=404, detail="Bannière non trouvée")
    
    new_status = not banner.get("is_active", True)
    await db.ad_banners.update_one({"_id": banner_id}, {"$set": {"is_active": new_status}})
    return {"message": f"Bannière {'activée' if new_status else 'désactivée'}", "is_active": new_status}

@api_router.delete("/banners/{banner_id}")
async def delete_banner(banner_id: str, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seuls les admins peuvent supprimer des bannières")
    
    await db.ad_banners.delete_one({"_id": banner_id})
    return {"message": "Bannière supprimée"}

# ADMIN
@api_router.get("/admin/stats")
async def get_stats(current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    
    stats = {
        "total_users": await db.users.count_documents({}),
        "job_seekers": await db.users.count_documents({"role": "job_seeker"}),
        "employers": await db.users.count_documents({"role": "employer"}),
        "total_jobs": await db.job_offers.count_documents({}),
        "total_applications": await db.applications.count_documents({}),
        "total_topics": await db.forum_topics.count_documents({})
    }
    return stats

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown():
    client.close()

# ==================== ROUTES RÉSEAU SOCIAL ====================

# Posts
class PostCreate(BaseModel):
    content: str
    media_url: Optional[str] = None

@api_router.post("/social/posts")
async def create_post(post_data: PostCreate, current_user = Depends(get_current_user)):
    post = {
        "_id": str(uuid.uuid4()),
        "author_id": current_user["_id"],
        **post_data.model_dump(),
        "likes_count": 0,
        "comments_count": 0,
        "created_at": datetime.now(timezone.utc)
    }
    await db.social_posts.insert_one(post)
    return serialize_doc(post)

@api_router.get("/social/posts")
async def get_posts(skip: int = 0, limit: int = 20):
    posts = await db.social_posts.find().sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    return serialize_doc(posts)

@api_router.delete("/social/posts/{post_id}")
async def delete_post(post_id: str, current_user = Depends(get_current_user)):
    post = await db.social_posts.find_one({"_id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    if post["author_id"] != current_user["_id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Non autorisé")
    await db.social_posts.delete_one({"_id": post_id})
    return {"message": "Post supprimé"}

# Comments
class CommentCreate(BaseModel):
    post_id: str
    content: str

@api_router.post("/social/comments")
async def create_comment(comment_data: CommentCreate, current_user = Depends(get_current_user)):
    comment = {
        "_id": str(uuid.uuid4()),
        "post_id": comment_data.post_id,
        "author_id": current_user["_id"],
        "content": comment_data.content,
        "likes_count": 0,
        "created_at": datetime.now(timezone.utc)
    }
    await db.social_comments.insert_one(comment)
    await db.social_posts.update_one({"_id": comment_data.post_id}, {"$inc": {"comments_count": 1}})
    return serialize_doc(comment)

@api_router.get("/social/comments/{post_id}")
async def get_comments(post_id: str):
    comments = await db.social_comments.find({"post_id": post_id}).sort("created_at", 1).to_list(100)
    return serialize_doc(comments)

@api_router.delete("/social/comments/{comment_id}")
async def delete_comment(comment_id: str, current_user = Depends(get_current_user)):
    comment = await db.social_comments.find_one({"_id": comment_id})
    if not comment:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    if comment["author_id"] != current_user["_id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Non autorisé")
    await db.social_comments.delete_one({"_id": comment_id})
    await db.social_posts.update_one({"_id": comment["post_id"]}, {"$inc": {"comments_count": -1}})
    return {"message": "Commentaire supprimé"}

# Reactions
class ReactionCreate(BaseModel):
    target_id: str
    target_type: str  # "post" or "comment"
    reaction_type: str  # "like", "love", "support", "celebrate"

@api_router.post("/social/reactions")
async def toggle_reaction(reaction_data: ReactionCreate, current_user = Depends(get_current_user)):
    # Check if reaction exists
    existing = await db.social_reactions.find_one({
        "user_id": current_user["_id"],
        "target_id": reaction_data.target_id,
        "target_type": reaction_data.target_type
    })
    
    if existing:
        # Remove reaction
        await db.social_reactions.delete_one({"_id": existing["_id"]})
        collection = db.social_posts if reaction_data.target_type == "post" else db.social_comments
        await collection.update_one({"_id": reaction_data.target_id}, {"$inc": {"likes_count": -1}})
        return {"action": "removed"}
    else:
        # Add reaction
        reaction = {
            "_id": str(uuid.uuid4()),
            "user_id": current_user["_id"],
            **reaction_data.model_dump(),
            "created_at": datetime.now(timezone.utc)
        }
        await db.social_reactions.insert_one(reaction)
        collection = db.social_posts if reaction_data.target_type == "post" else db.social_comments
        await collection.update_one({"_id": reaction_data.target_id}, {"$inc": {"likes_count": 1}})
        return {"action": "added", "reaction": serialize_doc(reaction)}

@api_router.get("/social/reactions/{target_id}")
async def get_reactions(target_id: str):
    reactions = await db.social_reactions.find({"target_id": target_id}).to_list(100)
    return serialize_doc(reactions)

# ==================== ROUTES ADMIN ENRICHIES ====================

@api_router.delete("/admin/users/{user_id}")
async def admin_delete_user(user_id: str, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    
    # Delete user profile
    await db.profiles.delete_one({"user_id": user_id})
    # Delete user
    await db.users.delete_one({"_id": user_id})
    # Delete related data
    await db.applications.delete_many({"candidate_id": user_id})
    await db.job_offers.delete_many({"employer_id": user_id})
    await db.social_posts.delete_many({"author_id": user_id})
    await db.social_comments.delete_many({"author_id": user_id})
    
    return {"message": "Utilisateur supprimé avec succès"}

@api_router.get("/admin/users")
async def admin_get_users(current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    
    users = await db.users.find({}, {"password": 0}).sort("created_at", -1).to_list(100)
    return serialize_doc(users)

# ==================== RÉFÉRENTIEL COMPÉTENCES ====================

@api_router.get("/competences")
async def get_competences():
    competences = await db.competences_ref.find().sort("nom", 1).to_list(1000)
    return serialize_doc(competences)

@api_router.post("/competences")
async def add_competence(nom: str, categorie: str = "Autre", current_user = Depends(get_current_user)):
    # Check if exists
    existing = await db.competences_ref.find_one({"nom": nom})
    if existing:
        return serialize_doc(existing)
    
    competence = {
        "_id": str(uuid.uuid4()),
        "nom": nom,
        "categorie": categorie,
        "created_at": datetime.now(timezone.utc)
    }
    await db.competences_ref.insert_one(competence)
    return serialize_doc(competence)
