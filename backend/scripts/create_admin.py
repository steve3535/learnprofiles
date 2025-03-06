import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_admin(email: str, password: str):
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User {email} already exists.")
            # Update to admin if not already
            if not user.is_admin:
                user.is_admin = True
                user.hashed_password = get_password_hash(password)
                db.commit()
                print(f"User {email} updated to admin.")
            return
        
        # Create new admin user
        admin_user = User(
            email=email,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin user {email} created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    create_admin(email, password) 