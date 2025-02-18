from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from app.models.file import File
import pytz

from datetime import datetime, timezone
from app.utils.hashid import encode_id

KST = pytz.timezone('Asia/Seoul')

def create_file(db: Session, request: Request):
    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M")

    user_id = request.session.get("user").get("id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="사용자 인증이 필요합니다.")
    
    db_file = File(
        title="string",
        content="content",
        created_at=now,
        updated_at=now,
        user_id=user_id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    # 해시화된 ID가 없으면 생성 후 업데이트
    if not db_file.hashed_id:
        db_file.hashed_id = encode_id(db_file.id)
        db.commit()
        db.refresh(db_file)
    return db_file.hashed_id

def get_file(db: Session, request: Request, hashed_id):
    user_id = request.session.get("user").get("id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="사용자 인증이 필요합니다.")
    
    db_file = db.query(File).filter(File.hashed_id == hashed_id).first()
    
    if db_file.user_id != user_id:
        raise HTTPException(status_code=403, detail="파일에 대한 권한이 없습니다.")
    
    return db_file
    

def get_files(db: Session, request: Request, skip: int = 0, limit: int = 100):
    user_id = request.session.get("user").get("id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="사용자 인증이 필요합니다.")
    
    return db.query(File).filter(File.user_id == user_id).offset(skip).limit(limit).all()

def save_file(db: Session, hashed_id: str, file_data: dict, request: Request):
    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    
    user_id = request.session.get("user").get("id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="사용자 인증이 필요합니다.")
    
    db_file = db.query(File).filter(File.hashed_id == hashed_id).first()
    
    if db_file.user_id != user_id:
        raise HTTPException(status_code=403, detail="파일에 대한 권한이 없습니다.")
    
    db_file.title = file_data["title"]
    db_file.content = file_data["content"]
    db_file.updated_at = now
    
    db.commit()
    db.refresh(db_file)
    
    return db_file
    
    