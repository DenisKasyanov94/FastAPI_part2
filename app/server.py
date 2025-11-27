from fastapi import FastAPI
from app.lifespan import lifespan
from app.routers import auth, users, advertisements

app = FastAPI(lifespan=lifespan)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(advertisements.router)

@app.get("/")
def read_root():
    return {"message": "Advertisement Service with Auth is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}