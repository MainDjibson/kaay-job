from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Supabase connection
supabase_url = os.environ['SUPABASE_URL']
supabase_key = os.environ['SUPABASE_KEY']
supabase: Client = create_client(supabase_url, supabase_key)

# JWT configuration
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['JWT_ACCESS_TOKEN_EXPIRE_MINUTES'])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================

class UserRole(str):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"
    ADMIN = "admin"

class ContractType(str):
    CDI = "CDI"
    CDD = "CDD"
    STAGE = "Stage"
    ALTERNANCE = "Alternance"
    FREELANCE = "Freelance"
    INTERIM = "Interim"

class ApplicationStatus(str):
    EN_COURS = "en_cours"
    ACCEPTE = "accepte"
    REFUSE = "refuse"

# Auth Models
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

class User(BaseModel):
    id: str
    email: str
    role: str
    created_at: str

# Profile Models
class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    profile_title: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    education_level: Optional[str] = None
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    company_sector: Optional[str] = None
    phone: Optional[str] = None
    social_links: Optional[str] = None
    bio: Optional[str] = None
    cv_url: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    date_of_birth: Optional[str] = None
    is_active: Optional[bool] = True
    diplomas: Optional[str] = None
    certifications: Optional[str] = None

class Profile(ProfileBase):
    id: str
    user_id: str
    created_at: str

# Job Offer Models
class JobOfferCreate(BaseModel):
    title: str
    description: str
    contract_type: str
    location: str
    salary: Optional[str] = None
    education_required: Optional[str] = None
    skills: Optional[str] = None

class JobOffer(JobOfferCreate):
    id: str
    employer_id: str
    created_at: str
    status: str = "active"

# Application Models
class ApplicationCreate(BaseModel):
    job_offer_id: str
    message: Optional[str] = None

class Application(BaseModel):
    id: str
    job_offer_id: str
    candidate_id: str
    message: Optional[str] = None
    status: str
    created_at: str

# Message Models
class MessageCreate(BaseModel):
    receiver_id: str
    content: str

class Message(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    content: str
    is_read: bool
    created_at: str

# Forum Models
class ForumCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ForumCategory(ForumCategoryCreate):
    id: str
    created_at: str

class ForumTopicCreate(BaseModel):
    category_id: str
    title: str
    content: str

class ForumTopic(ForumTopicCreate):
    id: str
    author_id: str
    created_at: str
    posts_count: int = 0

class ForumPostCreate(BaseModel):
    topic_id: str
    content: str

class ForumPost(ForumPostCreate):
    id: str
    author_id: str
    created_at: str

# Ad Banner Models
class AdBannerCreate(BaseModel):
    titre: str
    texte: str
    image: str
    telephone: str
    mail: str
    url: str
    is_active: Optional[bool] = True

class AdBanner(AdBannerCreate):
    id: str
    created_at: str

# ==================== HELPER FUNCTIONS ====================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=401, detail="User not found")
        
        return response.data[0]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "Bienvenue sur l'API kaay-job"}

# ========== AUTH ROUTES ==========

@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    # Check if user exists
    existing = supabase.table("users").select("*").eq("email", user_data.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    # Create user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    user = {
        "id": user_id,
        "email": user_data.email,
        "password": hashed_password,
        "role": user_data.role,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    supabase.table("users").insert(user).execute()
    
    # Create profile
    profile = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "full_name": user_data.full_name or "",
        "company_name": user_data.company_name or "",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    supabase.table("profiles").insert(profile).execute()
    
    # Create token
    access_token = create_access_token(data={"sub": user_id, "role": user_data.role})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "role": user_data.role
    }

@api_router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    # Find user
    response = supabase.table("users").select("*").eq("email", user_data.email).execute()
    
    if not response.data:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    user = response.data[0]
    
    # Verify password
    if not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Create token
    access_token = create_access_token(data={"sub": user["id"], "role": user["role"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user["id"],
        "role": user["role"]
    }

@api_router.get("/auth/me", response_model=User)
async def get_me(current_user = Depends(get_current_user)):
    return User(
        id=current_user["id"],
        email=current_user["email"],
        role=current_user["role"],
        created_at=current_user["created_at"]
    )

# ========== PROFILE ROUTES ==========

@api_router.get("/profiles/me", response_model=Profile)
async def get_my_profile(current_user = Depends(get_current_user)):
    response = supabase.table("profiles").select("*").eq("user_id", current_user["id"]).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Profil non trouvé")
    return response.data[0]

@api_router.get("/profiles/{user_id}", response_model=Profile)
async def get_profile(user_id: str):
    response = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Profil non trouvé")
    return response.data[0]

@api_router.put("/profiles/me", response_model=Profile)
async def update_profile(profile_data: ProfileBase, current_user = Depends(get_current_user)):
    update_data = profile_data.model_dump(exclude_unset=True)
    
    response = supabase.table("profiles").update(update_data).eq("user_id", current_user["id"]).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Profil non trouvé")
    
    return response.data[0]

@api_router.post("/profiles/upload-cv")
async def upload_cv(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    try:
        # Read file content
        content = await file.read()
        file_extension = file.filename.split('.')[-1]
        file_name = f"{current_user['id']}_cv_{uuid.uuid4()}.{file_extension}"
        
        # Upload to Supabase Storage
        response = supabase.storage.from_("cvs").upload(file_name, content, {"content-type": file.content_type})
        
        # Get public URL
        public_url = supabase.storage.from_("cvs").get_public_url(file_name)
        
        # Update profile with CV URL
        supabase.table("profiles").update({
            "cv_url": public_url,
            "cv_updated_at": datetime.now(timezone.utc).isoformat()
        }).eq("user_id", current_user["id"]).execute()
        
        return {"cv_url": public_url, "message": "CV uploadé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

@api_router.post("/profiles/upload-avatar")
async def upload_avatar(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    try:
        content = await file.read()
        file_extension = file.filename.split('.')[-1]
        file_name = f"{current_user['id']}_avatar_{uuid.uuid4()}.{file_extension}"
        
        response = supabase.storage.from_("avatars").upload(file_name, content, {"content-type": file.content_type})
        public_url = supabase.storage.from_("avatars").get_public_url(file_name)
        
        supabase.table("profiles").update({
            "avatar_url": public_url
        }).eq("user_id", current_user["id"]).execute()
        
        return {"avatar_url": public_url, "message": "Avatar uploadé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

# ========== JOB OFFERS ROUTES ==========

@api_router.post("/jobs", response_model=JobOffer)
async def create_job_offer(job_data: JobOfferCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Seuls les employeurs peuvent créer des offres")
    
    job = {
        "id": str(uuid.uuid4()),
        "employer_id": current_user["id"],
        "title": job_data.title,
        "description": job_data.description,
        "contract_type": job_data.contract_type,
        "location": job_data.location,
        "salary": job_data.salary,
        "education_required": job_data.education_required,
        "skills": job_data.skills,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    response = supabase.table("job_offers").insert(job).execute()
    return response.data[0]

@api_router.get("/jobs", response_model=List[JobOffer])
async def get_job_offers(
    search: Optional[str] = None,
    location: Optional[str] = None,
    contract_type: Optional[str] = None
):
    query = supabase.table("job_offers").select("*").eq("status", "active")
    
    if search:
        query = query.ilike("title", f"%{search}%")
    if location:
        query = query.ilike("location", f"%{location}%")
    if contract_type:
        query = query.eq("contract_type", contract_type)
    
    response = query.order("created_at", desc=True).execute()
    return response.data

@api_router.get("/jobs/{job_id}", response_model=JobOffer)
async def get_job_offer(job_id: str):
    response = supabase.table("job_offers").select("*").eq("id", job_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return response.data[0]

@api_router.get("/jobs/employer/me", response_model=List[JobOffer])
async def get_my_job_offers(current_user = Depends(get_current_user)):
    response = supabase.table("job_offers").select("*").eq("employer_id", current_user["id"]).order("created_at", desc=True).execute()
    return response.data

@api_router.put("/jobs/{job_id}", response_model=JobOffer)
async def update_job_offer(job_id: str, job_data: JobOfferCreate, current_user = Depends(get_current_user)):
    # Check ownership
    job = supabase.table("job_offers").select("*").eq("id", job_id).execute()
    if not job.data or job.data[0]["employer_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    update_data = job_data.model_dump(exclude_unset=True)
    response = supabase.table("job_offers").update(update_data).eq("id", job_id).execute()
    return response.data[0]

@api_router.delete("/jobs/{job_id}")
async def delete_job_offer(job_id: str, current_user = Depends(get_current_user)):
    # Check ownership
    job = supabase.table("job_offers").select("*").eq("id", job_id).execute()
    if not job.data or job.data[0]["employer_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    supabase.table("job_offers").update({"status": "archived"}).eq("id", job_id).execute()
    return {"message": "Offre archivée avec succès"}

# ========== APPLICATIONS ROUTES ==========

@api_router.post("/applications", response_model=Application)
async def apply_to_job(app_data: ApplicationCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "job_seeker":
        raise HTTPException(status_code=403, detail="Seuls les chercheurs d'emploi peuvent postuler")
    
    # Check if already applied
    existing = supabase.table("applications").select("*").eq("job_offer_id", app_data.job_offer_id).eq("candidate_id", current_user["id"]).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Vous avez déjà postulé à cette offre")
    
    application = {
        "id": str(uuid.uuid4()),
        "job_offer_id": app_data.job_offer_id,
        "candidate_id": current_user["id"],
        "message": app_data.message,
        "status": "en_cours",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    response = supabase.table("applications").insert(application).execute()
    return response.data[0]

@api_router.get("/applications/me", response_model=List[Application])
async def get_my_applications(current_user = Depends(get_current_user)):
    response = supabase.table("applications").select("*").eq("candidate_id", current_user["id"]).order("created_at", desc=True).execute()
    return response.data

@api_router.get("/applications/job/{job_id}")
async def get_job_applications(job_id: str, current_user = Depends(get_current_user)):
    # Check if user owns this job
    job = supabase.table("job_offers").select("*").eq("id", job_id).execute()
    if not job.data or job.data[0]["employer_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    response = supabase.table("applications").select("*").eq("job_offer_id", job_id).order("created_at", desc=True).execute()
    return response.data

@api_router.put("/applications/{app_id}/status")
async def update_application_status(app_id: str, status: str, current_user = Depends(get_current_user)):
    # Get application
    app = supabase.table("applications").select("*").eq("id", app_id).execute()
    if not app.data:
        raise HTTPException(status_code=404, detail="Candidature non trouvée")
    
    # Check if user owns the job
    job = supabase.table("job_offers").select("*").eq("id", app.data[0]["job_offer_id"]).execute()
    if not job.data or job.data[0]["employer_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    response = supabase.table("applications").update({"status": status}).eq("id", app_id).execute()
    return response.data[0]

# ========== MESSAGES ROUTES ==========

@api_router.post("/messages", response_model=Message)
async def send_message(msg_data: MessageCreate, current_user = Depends(get_current_user)):
    message = {
        "id": str(uuid.uuid4()),
        "sender_id": current_user["id"],
        "receiver_id": msg_data.receiver_id,
        "content": msg_data.content,
        "is_read": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    response = supabase.table("messages").insert(message).execute()
    return response.data[0]

@api_router.get("/messages/conversations")
async def get_conversations(current_user = Depends(get_current_user)):
    # Get all messages where user is sender or receiver
    sent = supabase.table("messages").select("receiver_id").eq("sender_id", current_user["id"]).execute()
    received = supabase.table("messages").select("sender_id").eq("receiver_id", current_user["id"]).execute()
    
    # Get unique user IDs
    user_ids = set()
    for msg in sent.data:
        user_ids.add(msg["receiver_id"])
    for msg in received.data:
        user_ids.add(msg["sender_id"])
    
    # Get profiles for these users
    conversations = []
    for user_id in user_ids:
        profile = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
        user_data = supabase.table("users").select("email, role").eq("id", user_id).execute()
        
        if profile.data and user_data.data:
            # Get unread count
            unread = supabase.table("messages").select("id", count="exact").eq("sender_id", user_id).eq("receiver_id", current_user["id"]).eq("is_read", False).execute()
            
            conversations.append({
                "user_id": user_id,
                "profile": profile.data[0],
                "email": user_data.data[0]["email"],
                "role": user_data.data[0]["role"],
                "unread_count": unread.count if unread.count else 0
            })
    
    return conversations

@api_router.get("/messages/{other_user_id}")
async def get_messages_with_user(other_user_id: str, current_user = Depends(get_current_user)):
    # Get all messages between current user and other user
    messages1 = supabase.table("messages").select("*").eq("sender_id", current_user["id"]).eq("receiver_id", other_user_id).execute()
    messages2 = supabase.table("messages").select("*").eq("sender_id", other_user_id).eq("receiver_id", current_user["id"]).execute()
    
    all_messages = messages1.data + messages2.data
    all_messages.sort(key=lambda x: x["created_at"])
    
    # Mark messages as read
    supabase.table("messages").update({"is_read": True}).eq("sender_id", other_user_id).eq("receiver_id", current_user["id"]).eq("is_read", False).execute()
    
    return all_messages

@api_router.get("/messages/unread/count")
async def get_unread_count(current_user = Depends(get_current_user)):
    response = supabase.table("messages").select("id", count="exact").eq("receiver_id", current_user["id"]).eq("is_read", False).execute()
    return {"count": response.count if response.count else 0}

# ========== FORUM ROUTES ==========

@api_router.post("/forum/categories", response_model=ForumCategory)
async def create_forum_category(cat_data: ForumCategoryCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seuls les admins peuvent créer des catégories")
    
    category = {
        "id": str(uuid.uuid4()),
        "name": cat_data.name,
        "description": cat_data.description,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    response = supabase.table("forum_categories").insert(category).execute()
    return response.data[0]

@api_router.get("/forum/categories", response_model=List[ForumCategory])
async def get_forum_categories():
    response = supabase.table("forum_categories").select("*").order("name").execute()
    return response.data

@api_router.post("/forum/topics", response_model=ForumTopic)
async def create_forum_topic(topic_data: ForumTopicCreate, current_user = Depends(get_current_user)):
    topic = {
        "id": str(uuid.uuid4()),
        "category_id": topic_data.category_id,
        "author_id": current_user["id"],
        "title": topic_data.title,
        "content": topic_data.content,
        "posts_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    response = supabase.table("forum_topics").insert(topic).execute()
    return response.data[0]

@api_router.get("/forum/topics")
async def get_forum_topics(category_id: Optional[str] = None):
    query = supabase.table("forum_topics").select("*")
    
    if category_id:
        query = query.eq("category_id", category_id)
    
    response = query.order("created_at", desc=True).execute()
    return response.data

@api_router.get("/forum/topics/{topic_id}")
async def get_forum_topic(topic_id: str):
    response = supabase.table("forum_topics").select("*").eq("id", topic_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Sujet non trouvé")
    return response.data[0]

@api_router.post("/forum/posts", response_model=ForumPost)
async def create_forum_post(post_data: ForumPostCreate, current_user = Depends(get_current_user)):
    post = {
        "id": str(uuid.uuid4()),
        "topic_id": post_data.topic_id,
        "author_id": current_user["id"],
        "content": post_data.content,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    response = supabase.table("forum_posts").insert(post).execute()
    
    # Update topic posts count
    topic = supabase.table("forum_topics").select("posts_count").eq("id", post_data.topic_id).execute()
    if topic.data:
        new_count = topic.data[0]["posts_count"] + 1
        supabase.table("forum_topics").update({"posts_count": new_count}).eq("id", post_data.topic_id).execute()
    
    return response.data[0]

@api_router.get("/forum/posts/{topic_id}")
async def get_forum_posts(topic_id: str):
    response = supabase.table("forum_posts").select("*").eq("topic_id", topic_id).order("created_at").execute()
    return response.data

# ========== AD BANNER ROUTES ==========

@api_router.post("/banners", response_model=AdBanner)
async def create_ad_banner(banner_data: AdBannerCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seuls les admins peuvent créer des bannières")
    
    banner = {
        "id": str(uuid.uuid4()),
        "titre": banner_data.titre,
        "texte": banner_data.texte,
        "image": banner_data.image,
        "telephone": banner_data.telephone,
        "mail": banner_data.mail,
        "url": banner_data.url,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    response = supabase.table("ad_banners").insert(banner).execute()
    return response.data[0]

@api_router.get("/banners", response_model=List[AdBanner])
async def get_ad_banners():
    response = supabase.table("ad_banners").select("*").execute()
    return response.data

@api_router.get("/banners/random", response_model=AdBanner)
async def get_random_banner():
    response = supabase.table("ad_banners").select("*").execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Aucune bannière disponible")
    return random.choice(response.data)

@api_router.put("/banners/{banner_id}", response_model=AdBanner)
async def update_ad_banner(banner_id: str, banner_data: AdBannerCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seuls les admins peuvent modifier des bannières")
    
    update_data = banner_data.model_dump()
    response = supabase.table("ad_banners").update(update_data).eq("id", banner_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Bannière non trouvée")
    
    return response.data[0]

@api_router.delete("/banners/{banner_id}")
async def delete_ad_banner(banner_id: str, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seuls les admins peuvent supprimer des bannières")
    
    supabase.table("ad_banners").delete().eq("id", banner_id).execute()
    return {"message": "Bannière supprimée avec succès"}

# ========== ADMIN ROUTES ==========

@api_router.get("/admin/stats")
async def get_admin_stats(current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    
    users = supabase.table("users").select("id", count="exact").execute()
    job_seekers = supabase.table("users").select("id", count="exact").eq("role", "job_seeker").execute()
    employers = supabase.table("users").select("id", count="exact").eq("role", "employer").execute()
    jobs = supabase.table("job_offers").select("id", count="exact").execute()
    applications = supabase.table("applications").select("id", count="exact").execute()
    topics = supabase.table("forum_topics").select("id", count="exact").execute()
    
    return {
        "total_users": users.count or 0,
        "job_seekers": job_seekers.count or 0,
        "employers": employers.count or 0,
        "total_jobs": jobs.count or 0,
        "total_applications": applications.count or 0,
        "total_topics": topics.count or 0
    }

@api_router.get("/admin/users")
async def get_all_users(current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    
    users = supabase.table("users").select("id, email, role, created_at").order("created_at", desc=True).execute()
    return users.data

@api_router.delete("/admin/users/{user_id}")
async def delete_user(user_id: str, current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    
    # Delete user's profile
    supabase.table("profiles").delete().eq("user_id", user_id).execute()
    # Delete user
    supabase.table("users").delete().eq("id", user_id).execute()
    
    return {"message": "Utilisateur supprimé avec succès"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down kaay-job API")