#!/usr/bin/env python
"""
Reset database - delete old database and recreate with new schema
"""

import os
import sys

db_path = "instance/ocr_compliance.db"

print("🔄 Resetting database...")
print(f"📁 Database path: {db_path}")

# Check if database exists
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"✅ Deleted old database: {db_path}")
    except Exception as e:
        print(f"❌ Error deleting database: {str(e)}")
        print("   Make sure no processes are using the database")
        sys.exit(1)
else:
    print(f"ℹ️  Database doesn't exist: {db_path}")

# Initialize new database
print("\n🔄 Creating new database with updated schema...")

try:
    from database import db
    from app import app
    
    with app.app_context():
        db.create_all()
        print("✅ Database created successfully with new schema!")
        print("\n📊 Tables created:")
        print("   - documents")
        print("   - ocr_results (with ocr_engine, model_name, ocr_metadata columns)")
        print("   - compliance_checks")
        print("   - error_detections")
        print("   - compliance_rules")
        print("   - audit_logs")
        
except Exception as e:
    print(f"❌ Error creating database: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Database reset complete!")
print("You can now start the backend server: python app.py")
