from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_google_id(db: Session, google_id: str):
    return db.query(User).filter(User.google_id == google_id).first()

def create_user(db: Session, user_info: dict):
    db_user = User(
        email=user_info.get("email"),
        name=user_info.get("name"),
        google_id=user_info.get("sub")
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: User, user_info: dict):
    user.email = user_info.get("email")
    user.name = user_info.get("name")
    db.commit()
    db.refresh(user)
    return user
