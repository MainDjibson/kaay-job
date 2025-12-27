from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
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

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================

# Experience Model
class Experience(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    poste: str
    entreprise: str
    date_debut: str
    date_fin: Optional[str] = None
    en_cours: bool = False
    taches: Optional[str] = None
    
# Diplome Model
class Diplome(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nom: str
    etablissement: str
    annee: str
    domaine: Optional[str] = None

# Certification Model  
class Certification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nom: str
    organisme: str
    date_obtention: str
    validite: Optional[str] = None

# Competence Model
class Competence(BaseModel):
    nom: str
    niveau: str  # Débutant, Intermédiaire, Avancé, Expert

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

# Profile Models
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
    # Pour candidats
    experiences: Optional[List[Experience]] = []
    diplomes: Optional[List[Diplome]] = []
    certifications: Optional[List[Certification]] = []
    competences: Optional[List[Competence]] = []
    # Pour entreprises
    company_sector: Optional[str] = None
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    domaine_expertise: Optional[str] = None
    chiffre_affaires: Optional[str] = None
    date_creation: Optional[str] = None
    effectif: Optional[str] = None

# Job Offer Models
class JobOfferCreate(BaseModel):
    title: str
    description: str
    contract_type: str
    location: str
    salary: Optional[str] = None
    education_required: Optional[str] = None
    skills: Optional[str] = None

# Application Models
class ApplicationCreate(BaseModel):
    job_offer_id: str
    message: Optional[str] = None

# Message Models
class MessageCreate(BaseModel):
    receiver_id: str
    content: str

# Forum Models
class ForumTopicCreate(BaseModel):
    category_id: str
    title: str
    content: str

class ForumPostCreate(BaseModel):
    topic_id: str
    content: str

# Ad Banner Models
class AdBannerCreate(BaseModel):
    titre: str
    texte: str
    image: str
    telephone: str
    mail: str
    url: str
    is_active: Optional[bool] = True

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
        
        user = await db.users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "Bienvenue sur l'API kaay-job (MongoDB)"}

# ========== AUTH ROUTES ==========

@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    # Check if user exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    # Create user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    user = {
        "_id": user_id,
        "email": user_data.email,
        "password": hashed_password,
        "role": user_data.role,
        "created_at": datetime.now(timezone.utc)
    }
    
    await db.users.insert_one(user)
    
    # Create profile
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
    user = await db.users.find_one({"email": user_data.email})
    
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    if not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = create_access_token(data={"sub": user["_id"], "role": user["role"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user["_id"],
        "role": user["role"]
    }

@api_router.get("/auth/me")
async def get_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["_id"],
        "email": current_user["email"],
        "role": current_user["role"],
        "created_at": current_user["created_at"].isoformat() if isinstance(current_user["created_at"], datetime) else current_user["created_at"]
    }

# Continue dans la partie 2...
