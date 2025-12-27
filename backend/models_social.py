"""Modèles pour le réseau social"""

from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

# Publication/Post
class PostCreate(BaseModel):
    content: str
    media_url: Optional[str] = None
    media_type: Optional[str] = None  # image, video, document

class Post(PostCreate):
    id: str
    author_id: str
    likes_count: int = 0
    comments_count: int = 0
    created_at: str

# Commentaire
class CommentCreate(BaseModel):
    post_id: str
    content: str

class Comment(CommentCreate):
    id: str
    author_id: str
    likes_count: int = 0
    created_at: str

# Réaction
class ReactionCreate(BaseModel):
    target_id: str  # post_id ou comment_id
    target_type: str  # "post" ou "comment"
    reaction_type: str  # "like", "love", "support", "celebrate"
