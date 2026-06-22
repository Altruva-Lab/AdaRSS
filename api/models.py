from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ClassifyRequest(BaseModel):
    job_title: str
    skill: str

class ClassifyResponse(BaseModel):
    classification: str
    label: int

class AdviceRequest(BaseModel):
    history: str
    target_skill: str

class AdviceResponse(BaseModel):
    classification: str
    advice_type: str
    description: str
    roadmap: str
    similarity: Optional[float] = 0.0

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
    created_at: datetime
    plan_id: Optional[int] = None  # <-- add this

class UserCreateRequest(BaseModel):
    email: str
    password: str

class APIKeyCreate(BaseModel):
    name: str

class APIKeyResponse(BaseModel):
    key: str
    name: str
    is_active: bool
    created_at: datetime
    usage_count: Optional[int] = 0

class PlanResponse(BaseModel):
    id: int
    name: str
    max_requests: int
    price: int
    is_active: bool

class UserProfileResponse(BaseModel):
    email: str
    role: str
    plan: Optional[str] = None
    max_requests: Optional[int] = 0
    usage: Optional[int] = 0
    usage_percentage: Optional[float] = 0.0

# Add after APIKeyResponse
class AdminKeyResponse(BaseModel):
    key: str
    name: str
    is_active: bool
    created_at: datetime
    usage_count: int
    owner_email: Optional[str] = None