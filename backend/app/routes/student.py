from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.crud import create_student, get_students, get_student_by_id, update_student, delete_student
from app.auth_utils import SECRET_KEY, ALGORITHM   # ✅ import this

router = APIRouter()

#  JWT setup
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------- CREATE ----------------
@router.post("/students")
def add_student(name: str, age: int, user: str = Depends(get_current_user)):
    student = create_student(name, age)
    return {"message": "Student created", "data": student}


# ---------------- READ ALL ----------------
@router.get("/students")
def read_students(user: str = Depends(get_current_user)):
    return get_students()


# ---------------- READ ONE ----------------
@router.get("/students/{student_id}")
def read_student(student_id: int, user: str = Depends(get_current_user)):
    return get_student_by_id(student_id)


# ---------------- UPDATE ----------------
@router.put("/students/{student_id}")
def update_student_data(student_id: int, name: str, age: int, user: str = Depends(get_current_user)):
    student = update_student(student_id, name, age)

    if not student:
        return {"message": "Student not found"}

    return {"message": "Student updated", "data": student}


# ---------------- DELETE ----------------
@router.delete("/students/{student_id}")
def delete_student_data(student_id: int, user: str = Depends(get_current_user)):
    student = delete_student(student_id)

    if not student:
        return {"message": "Student not found"}

    return {"message": "Student deleted"}