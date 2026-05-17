# Student Management System

## Overview
This project is a full-stack Student Management System that allows users to perform CRUD (Create, Read, Update, Delete) operations on student records. It includes user authentication with signup and login functionality, secured using JWT tokens.

The frontend is built using Streamlit, and the backend is developed using FastAPI.

---

## Features

### Authentication
- User Signup
- User Login
- JWT-based authentication
- Protected API routes

### Student Management
- Create new student records
- View all students in table format
- Update existing student details
- Delete student records

### Dashboard
- Total number of students
- Average age calculation
- Search functionality

---

## Tech Stack

### Frontend
- Streamlit
- Pandas
- Requests

### Backend
- FastAPI
- SQLAlchemy
- Passlib
- Python-JOSE

### Database
- SQLite

---

## Project Structure

backend/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── crud.py
│   ├── auth_utils.py
│   └── routes/
│       ├── auth.py
│       └── students.py
│
frontend/
│
└── app.py

---

## Setup Instructions

### 1. Clone the Repository

git clone <your-repo-url>  
cd Student_Management_System  

---

### 2. Backend Setup

cd backend  
python -m venv venv  

venv\Scripts\activate   (Windows)  
# source venv/bin/activate  (Linux/Mac)

pip install -r requirements.txt  

Run backend:

uvicorn app.main:app --reload  

Backend runs at:  
http://127.0.0.1:8000  

---

### 3. Frontend Setup

cd frontend  
pip install streamlit pandas requests  

Run frontend:

streamlit run app.py  

Frontend runs at:  
http://localhost:8501  

---

## API Endpoints

### Authentication

POST /signup  
POST /login  

### Students

POST   /students  
GET    /students  
GET    /students/{id}  
PUT    /students/{id}  
DELETE /students/{id}  

---

## Authentication Flow

1. User signs up with username and password  
2. User logs in using credentials  
3. Backend returns JWT token  
4. Token is stored in frontend session  
5. All requests include:

Authorization: Bearer <token>  

---

## How It Works

- Streamlit frontend sends requests to FastAPI backend  
- Backend validates JWT token for protected routes  
- Database stores user and student data  
- Session state manages login flow in frontend  

---

## Future Improvements

- Role-based access control  
- Pagination  
- Data visualization  
- Deployment  
- Docker support  
- CI/CD integration  

---

## Notes

- Start backend before frontend  
- Token is required for protected APIs  
- Database is auto-created  

---

## Author

Developed as part of a full-stack project using FastAPI and Streamlit.