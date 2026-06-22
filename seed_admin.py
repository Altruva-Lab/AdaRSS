# import asyncio
# from api.database import AsyncSessionLocal, User
# from passlib.context import CryptContext
# from sqlalchemy import select

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# async def seed_admin():
#     async with AsyncSessionLocal() as db:
#         # Check if admin already exists
#         result = await db.execute(select(User).where(User.email == "dev.abdulhakeem@gmail.com"))
#         admin = result.scalar_one_or_none()
#         if not admin:
#             hashed = pwd_context.hash("Admin123")  # To change this in prod!

#             # seed the default plan for the admin user
#             admin = User(
#                 email="dev.abdulhakeem@gmail.com",
#                 hashed_password=hashed,
#                 role="admin",
#                 is_active=True,
#                 plan_id=1,
#                 max_requests=10000000000,
#             )
#             db.add(admin)
#             await db.commit()
#             print("✅ Admin user created: dev.abdulhakeem@gmail.com / Admin123")
#         else:
#             print("ℹ️ Admin user already exists.")

# if __name__ == "__main__":
#     asyncio.run(seed_admin())