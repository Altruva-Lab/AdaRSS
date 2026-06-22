from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .database import get_db, User, APIKey, UsageLog, Plan
from .config import SECRET_KEY, ALGORITHM, RATE_LIMIT
import secrets

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Token decoded: {payload}") 
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise credentials_exception
    return user

# For API key auth (external clients)
async def verify_api_key(request: Request, db: AsyncSession = Depends(get_db)):
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    
    # 1. Get the API key object
    result = await db.execute(select(APIKey).where(APIKey.key == api_key, APIKey.is_active == True))
    key_obj = result.scalar_one_or_none()
    if not key_obj:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")
    
    # 2. Get the user linked to this key
    if key_obj.user_id is None:
        # For backward compatibility – if no user linked, find by email or create default
        raise HTTPException(status_code=403, detail="API key not linked to a user")
    
    user_result = await db.execute(select(User).where(User.id == key_obj.user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive or not found")
    
    # 3. Check/reset monthly usage
    current_month = int(datetime.now().strftime("%Y%m"))
    if user.last_reset_month != current_month:
        user.monthly_usage = 0
        user.last_reset_month = current_month
        await db.commit()
    
    # 4. Check plan
    if user.plan_id is None:
        raise HTTPException(status_code=403, detail="No active plan")
    
    plan_result = await db.execute(select(Plan).where(Plan.id == user.plan_id))
    plan = plan_result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=403, detail="Plan not found")
    
    if user.monthly_usage >= plan.max_requests:
        raise HTTPException(status_code=429, detail=f"Monthly request limit exceeded ({plan.max_requests} requests)")
    
    # 5. Increment usage and log
    user.monthly_usage += 1
    log = UsageLog(api_key=api_key, endpoint=request.url.path, user_id=user.id)
    db.add(log)
    await db.commit()
    
    return api_key

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user