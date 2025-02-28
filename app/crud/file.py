from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, Depends
from app.models.file import File
from app.utils.authValidator import AuthValidator
from app.utils import datetime_now

from app.utils.hashid import encode_id


def create_file(db: Session, request: Request, user_id: int = Depends(AuthValidator.get_user_id)):
    print(0)
    now = datetime_now()
    print(1)
    db_file = File(
        title="string",
        content="content",
        created_at=now,
        updated_at=now,
        user_id=user_id,
        hashed_id=None
    )
    print(2)
    db.add(db_file)
    print(3)
    db.commit()
    print(4)
    db.refresh(db_file)
    print(5)
    # 해시화된 ID가 없으면 생성 후 업데이트
    if not db_file.hashed_id:
        print(6)
        db_file.hashed_id = encode_id(db_file.id)
        print(7)
        db.commit()
        print(8)
        db.refresh(db_file)
        print(9)
    return db_file.hashed_id


def get_file(db: Session, request: Request, hashed_id, user_id: int = Depends(AuthValidator.get_user_id)):
    db_file = db.query(File).filter(File.hashed_id == hashed_id).first()

    if db_file.user_id != user_id:
        raise HTTPException(status_code=403, detail="파일에 대한 권한이 없습니다.")

    return db_file


def get_files(db: Session, request: Request, skip: int = 0, limit: int = 100, user_id: int = Depends(AuthValidator.get_user_id)):
    return db.query(File).filter(File.user_id == user_id).offset(skip).limit(limit).all()


def save_file(db: Session, hashed_id: str, file_data: dict, request: Request, user_id: int = Depends(AuthValidator.get_user_id)):
    now = datetime_now()

    db_file = db.query(File).filter(File.hashed_id == hashed_id).first()

    if db_file.user_id != user_id:
        raise HTTPException(status_code=403, detail="파일에 대한 권한이 없습니다.")

    db_file.title = file_data["title"]
    db_file.content = file_data["content"]
    db_file.updated_at = now

    db.commit()
    db.refresh(db_file)

    return db_file
