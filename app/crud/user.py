from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.schemas.profile import PasswordUpdate, ProfileUpdate


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def create(db: Session, data: RegisterRequest) -> User:
    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_profile(db: Session, user: User, data: ProfileUpdate) -> User:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def update_password(db: Session, user: User, data: PasswordUpdate) -> bool:
    if not verify_password(data.current_password, user.hashed_password):
        return False
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    return True
