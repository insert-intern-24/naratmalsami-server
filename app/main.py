import os
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.logging import setup_logging
from app.utils.lifespan import lifespan
from app.routes import ai, auth as auth_router, files

IS_DEV = os.environ.get("IS_DEV", "false").lower() == "true"

setup_logging()
app = FastAPI(lifespan=lifespan)

if IS_DEV:
    cors_allow_origins = ["*"]
    session_domain = None
    session_same_site = "lax"
    print("개발 환경 설정 적용")
else:
    cors_allow_origins = ["https://프로덕션프론트엔드.com"]
    session_domain = ".madac.me"
    session_same_site = "none"
    print("프로덕션 환경 설정 적용")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    domain=session_domain,
    same_site=session_same_site,
)

app.include_router(ai.router, prefix="/ai")
app.include_router(auth_router.router, prefix="/auth")
app.include_router(files.router, prefix="/files")


@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if user:
        print(user.get('id'))
        return {"message": f"Welcome, {user.get('name')}"}
    return {"message": "Hello, please login."}
