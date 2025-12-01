from fastapi import FastAPI
from app.lifespan import lifespan
from app.routers.users import router as users_router
from app.routers.advertisements import router as ads_router
from app.routers.login import router as login_router

app = FastAPI(lifespan=lifespan)

app.include_router(login_router)
app.include_router(users_router)
app.include_router(ads_router)

@app.get("/")
def read_root():
    return {"message": "Advertisement Service with Auth is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}