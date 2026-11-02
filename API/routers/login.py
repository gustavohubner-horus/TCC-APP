from fastapi import APIRouter

router = APIRouter(prefix="/login" tags=["LOGIN"])

@router.get("/login")