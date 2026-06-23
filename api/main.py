import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .database import init_db, get_db, User, APIKey, UsageLog, Plan, AsyncSessionLocal
from .dependencies import get_current_user, verify_api_key, get_current_admin_user, check_and_increment_usage
from .models import (
    ClassifyRequest, ClassifyResponse,
    AdviceRequest, AdviceResponse,
    UserResponse, UserCreateRequest,
    APIKeyCreate, APIKeyResponse,
    PlanResponse, UserProfileResponse,
    AdminKeyResponse
)
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from jose import jwt
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from sentence_transformers import SentenceTransformer, util
import secrets

# ---------- Lifespan context manager ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await bootstrap_defaults()
    print("✅ Database ready. Models loaded.")
    yield
    # Shutdown (if needed)
    # await engine.dispose()

# ---------- FastAPI app ----------
app = FastAPI(
    title="AdaRSS API",
    version="2.0",
    description="Skill classification & career advice with JWT auth.",
    lifespan=lifespan
)

# ---------- CORS ----------
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Password hashing ----------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- Model loading ----------
MODEL_PATH = "./api/model/adarss-distilbert"
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------- Helper functions ----------
def classify_skill_text(text: str):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=64)
    with torch.no_grad():
        outputs = model(**inputs)
    pred = outputs.logits.argmax().item()
    mapping = {0: "Enduring", 1: "Emergent", 2: "Transient"}
    return pred, mapping[pred]

def generate_advice(history: str, target_skill: str):
    history_emb = similarity_model.encode(history, convert_to_tensor=True)
    target_emb = similarity_model.encode(target_skill, convert_to_tensor=True)
    sim = util.pytorch_cos_sim(history_emb, target_emb).item()
    _, durability = classify_skill_text(f"Generic Worker: {target_skill}")

    if sim >= 0.35:
        advice_type = "Continuous Upscaling"
        desc = "✅ Your background aligns well. You have relevant experience."
        roadmap = f"Advanced path: Deepen {target_skill} expertise through certifications and applied projects. Since {target_skill} is {durability}, it's a solid investment."
    elif sim >= 0.15:
        advice_type = "Career Broadening"
        desc = f"🌉 Your skills transfer to {target_skill}, though not directly. You can leverage your existing knowledge."
        roadmap = f"Consider a bridging course or project that connects your current expertise to {target_skill}. {target_skill} is {durability}."
    else:
        advice_type = "Change of Profession"
        desc = f"⚠️ {target_skill} represents a significant pivot from your current path."
        roadmap = f"Plan for 18-36 months of dedicated learning. Start with fundamentals, build portfolio, then pursue internships or entry-level roles. Note: {target_skill} is currently {durability}."

    return {
        "advice_type": advice_type,
        "description": desc,
        "roadmap": roadmap,
        "durability": durability,
        "similarity": sim
    }

# ---------- Bootstrap defaults ----------
async def bootstrap_defaults():
    async with AsyncSessionLocal() as db:
        # 1. Create default plans
        plans_data = [
            {"name": "Starter", "max_requests": 5000, "price": 1900},
            {"name": "Pro", "max_requests": 50000, "price": 4900},
            {"name": "Enterprise", "max_requests": 500000, "price": 19900},
        ]
        for p_data in plans_data:
            existing = await db.execute(select(Plan).where(Plan.name == p_data["name"]))
            if not existing.scalar_one_or_none():
                plan = Plan(**p_data)
                db.add(plan)
        await db.commit()

        # 2. Ensure admin exists and has a plan
        admin_email = "dev.abdulhakeem@gmail.com"
        result = await db.execute(select(User).where(User.email == admin_email))
        admin = result.scalar_one_or_none()
        
        if not admin:
            hashed = pwd_context.hash("Admin123")
            admin = User(
                email=admin_email,
                hashed_password=hashed,
                role="admin",
                is_active=True,
            )
            db.add(admin)
            await db.commit()
            print("✅ Admin user created: dev.abdulhakeem@gmail.com / Admin123")
        else:
            # Ensure the existing admin has the correct role
            if admin.role != "admin":
                admin.role = "admin"
                await db.commit()
                print("✅ Updated existing admin role to 'admin'.")
            else:
                print("ℹ️ Admin user already exists with correct role.")

        # Always assign Enterprise plan to admin if missing
        if admin.plan_id is None:
            plan_result = await db.execute(select(Plan).where(Plan.name == "Enterprise"))
            plan = plan_result.scalar_one_or_none()
            if plan:
                admin.plan_id = plan.id
                await db.commit()
                print("✅ Assigned Enterprise plan to admin.")
            else:
                print("⚠️ Enterprise plan not found.")

# ---------- Auth ----------
@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {
            "sub": user.email,
            "role": user.role,          
            "exp": datetime.utcnow() + access_token_expires
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ---------- User Profile ----------
@app.get("/me", response_model=UserProfileResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    plan = None
    max_requests = 0
    if current_user.plan_id:
        plan_result = await db.execute(select(Plan).where(Plan.id == current_user.plan_id))
        plan = plan_result.scalar_one_or_none()
        if plan:
            max_requests = plan.max_requests
    
    usage_percentage = 0
    if max_requests > 0:
        usage_percentage = (current_user.monthly_usage / max_requests) * 100
    
    return UserProfileResponse(
        email=current_user.email,
        role=current_user.role,
        plan=plan.name if plan else None,
        max_requests=max_requests,
        usage=current_user.monthly_usage,
        usage_percentage=usage_percentage
    )

@app.post("/me/password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not pwd_context.verify(old_password, current_user.hashed_password):
        raise HTTPException(401, "Incorrect current password")
    current_user.hashed_password = pwd_context.hash(new_password)
    await db.commit()
    return {"status": "password updated"}

# ---------- Plans ----------
@app.get("/plans", response_model=list[PlanResponse])
async def get_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plan).where(Plan.is_active == True))
    plans = result.scalars().all()
    return plans

@app.post("/me/plan")
async def change_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    plan = await db.get(Plan, plan_id)
    if not plan:
        raise HTTPException(404, "Plan not found")
    current_user.plan_id = plan_id
    current_user.monthly_usage = 0
    await db.commit()
    return {"status": "updated", "plan": plan.name}

# ---------- Protected Endpoints ----------
@app.post("/classify", response_model=ClassifyResponse)
async def classify(
    req: ClassifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await check_and_increment_usage(current_user, db, "/classify")
    text = f"{req.job_title}: {req.skill}"
    _, classification = classify_skill_text(text)
    pred, _ = classify_skill_text(text)
    return {"classification": classification, "label": pred}

@app.post("/advice", response_model=AdviceResponse)
async def advice(
    req: AdviceRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await check_and_increment_usage(current_user, db, "/advice")
    result = generate_advice(req.history, req.target_skill)
    return {
        "classification": result["durability"],
        "advice_type": result["advice_type"],
        "description": result["description"],
        "roadmap": result["roadmap"],
        "similarity": result["similarity"]
    }

# ---------- API Key Management ----------
@app.get("/api-keys", response_model=list[APIKeyResponse])
async def get_api_keys(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role == "admin":
        result = await db.execute(select(APIKey))
    else:
        result = await db.execute(select(APIKey).where(APIKey.user_id == current_user.id))
    
    keys = result.scalars().all()
    response = []
    for key in keys:
        usage_result = await db.execute(
            select(func.count(UsageLog.id)).where(UsageLog.api_key == key.key)
        )
        count = usage_result.scalar() or 0
        response.append(APIKeyResponse(
            key=key.key,
            name=key.name,
            is_active=key.is_active,
            created_at=key.created_at,
            usage_count=count
        ))
    return response

@app.post("/api-keys", response_model=APIKeyResponse)
async def create_api_key(
    req: APIKeyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_key = "adarss_" + secrets.token_urlsafe(32)
    api_key = APIKey(
        key=new_key,
        name=req.name,
        is_active=True,
        user_id=current_user.id
    )
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)
    return APIKeyResponse(
        key=api_key.key,
        name=api_key.name,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        usage_count=0
    )

@app.delete("/api-keys/{key_id}")
async def revoke_api_key(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(APIKey).where(APIKey.key == key_id))
    key_obj = result.scalar_one_or_none()
    if not key_obj:
        raise HTTPException(status_code=404, detail="Key not found")
    if current_user.role != "admin" and key_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your key")
    key_obj.is_active = False
    await db.commit()
    return {"status": "revoked"}

@app.get("/api-keys/{key_id}/usage")
async def get_key_usage(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UsageLog)
        .where(UsageLog.api_key == key_id)
        .order_by(UsageLog.request_time.desc())
        .limit(100)
    )
    logs = result.scalars().all()
    return logs

# ---------- Admin Endpoints ----------
@app.get("/admin/users", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.post("/admin/users", response_model=UserResponse)
async def create_client(
    req: UserCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    result = await db.execute(select(User).where(User.email == req.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = pwd_context.hash(req.password)
    user = User(
        email=req.email,
        hashed_password=hashed,
        role="client",
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.patch("/admin/users/{user_id}/toggle")
async def toggle_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    await db.commit()
    return {"status": "updated", "is_active": user.is_active}

@app.post("/admin/users/{user_id}/plan")
async def set_user_plan(
    user_id: int,
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    plan = await db.get(Plan, plan_id)
    if not plan:
        raise HTTPException(404, "Plan not found")
    user.plan_id = plan_id
    user.monthly_usage = 0
    await db.commit()
    return {"status": "updated", "plan": plan.name}

@app.post("/admin/generate-key")
async def admin_create_api_key(
    name: str,
    user_email: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    user_id = None
    if user_email:
        result = await db.execute(select(User).where(User.email == user_email))
        user = result.scalar_one_or_none()
        if user:
            user_id = user.id
    
    new_key = "adarss_" + secrets.token_urlsafe(32)
    api_key = APIKey(
        key=new_key,
        name=name,
        is_active=True,
        user_id=user_id
    )
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)
    return {
        "api_key": api_key.key,
        "name": api_key.name,
        "user_id": api_key.user_id
    }

# ---------- Admin: Manage All Keys ----------
@app.get("/admin/keys", response_model=list[AdminKeyResponse])
async def admin_get_keys(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    # Join APIKey with User to get owner email
    result = await db.execute(
        select(APIKey, User.email)
        .join(User, APIKey.user_id == User.id, isouter=True)
        .order_by(APIKey.created_at.desc())
    )
    rows = result.all()
    response = []
    for key, email in rows:
        usage_result = await db.execute(
            select(func.count(UsageLog.id)).where(UsageLog.api_key == key.key)
        )
        count = usage_result.scalar() or 0
        response.append({
            "key": key.key,
            "name": key.name,
            "is_active": key.is_active,
            "created_at": key.created_at,
            "usage_count": count,
            "owner_email": email or "Unassigned"
        })
    return response

# ---------- Root ----------
@app.get("/")
def root():
    return {"message": "AdaRSS API is running. Use /classify or /advice endpoints."}