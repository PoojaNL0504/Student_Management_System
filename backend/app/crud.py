from app.models import Student, User
from app.database import SessionLocal

def create_student(name: str, age: int):
    db = SessionLocal()
    try:
        new_student = Student(name=name, age=age)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except Exception as e:
        db.rollback()
        print("Error:", e)
    finally:
        db.close()



def get_students():
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        return students
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()



def get_student_by_id(student_id: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        return student
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()


def update_student(student_id: int, name: str, age: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return None

        student.name = name
        student.age = age

        db.commit()
        db.refresh(student)
        return student

    except Exception as e:
        db.rollback()
        print("Error:", e)
    finally:
        db.close()



def delete_student(student_id: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return None

        db.delete(student)
        db.commit()
        return student

    except Exception as e:
        db.rollback()
        print("Error:", e)
    finally:
        db.close()





# 

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    password = password[:72]   # ✅ truncate
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain[:72], hashed)

def create_user(username: str, password: str):
    db = SessionLocal()
    try:
        hashed_pw = hash_password(password)

        user = User(
            username=username,
            password=hashed_pw
        )

        db.add(user)        # ✅ add to session
        db.commit()         # ✅ SAVE to DB
        db.refresh(user)    # ✅ optional

        return user

    except Exception as e:
        db.rollback()
        print("ERROR:", e)  # 🔥 check console
        return None

    finally:
        db.close()
def authenticate_user(username: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        print("User from DB:", user)
        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user
    finally:
        db.close()