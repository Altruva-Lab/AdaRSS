# import asyncio
# from api.database import AsyncSessionLocal, Plan

# async def seed():
#     async with AsyncSessionLocal() as db:
#         plans = [
#             Plan(name="Default", price=0, max_requests=1000000000),  # For admin user
#             Plan(name="Starter", max_requests=100, price=0),
#             Plan(name="Pro", max_requests=50000, price=4900),   # $49
#             Plan(name="Enterprise", max_requests=500000, price=19900)
#         ]
#         for p in plans:
#             db.add(p)
#         await db.commit()

# asyncio.run(seed())