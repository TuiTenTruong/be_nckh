import os
from app import create_app, db
from sqlalchemy import text

def main():
    print("=" * 60)
    print(" UPDATING DATABASE SCHEMA FOR SCAN_SESSIONS")
    print("=" * 60)
    
    app = create_app('development')
    with app.app_context():
        try:
            # Drop the scan_sessions table if it exists to force recreate with correct schema
            print(" Dropping existing scan_sessions table...")
            db.session.execute(text("DROP TABLE IF EXISTS scan_sessions"))
            db.session.commit()
            print(" Table dropped successfully.")
            
            # Recreate tables
            print(" Recreating scan_sessions table via SQLAlchemy create_all()...")
            db.create_all()
            print(" Table recreated successfully with all current model columns!")
            
        except Exception as e:
            print(f" ERROR updating database schema: {e}")
            db.session.rollback()

if __name__ == '__main__':
    main()
