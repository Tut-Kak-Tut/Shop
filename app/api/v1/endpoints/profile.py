from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.profile import PasswordUpdate, ProfileOut, ProfileUpdate

router = APIRouter()


@router.get("", response_model=ProfileOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("", response_model=ProfileOut)
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.user.update_profile(db, current_user, data)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def update_password(
    data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = crud.user.update_password(db, current_user, data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
