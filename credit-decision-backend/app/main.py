from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.routes import auth, loan, transaction, bank, user
from app.middleware.error_handler import error_handler_middleware, setup_exception_handlers

# Create FastAPI app
app = FastAPI(
    title="Adaptive Credit Decisioning System",
    description="Advanced credit evaluation for underbanked users",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup exception handlers
setup_exception_handlers(app)

# Custom error handling middleware
app.middleware("http")(error_handler_middleware)


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(loan.router, prefix="/api/loans", tags=["Loans"])
app.include_router(transaction.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(bank.router, prefix="/api/banks", tags=["Banks"])
app.include_router(user.router, prefix="/api/user", tags=["User"])

@app.get("/")
async def root():
    return {
        "message": "Adaptive Credit Decisioning System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
