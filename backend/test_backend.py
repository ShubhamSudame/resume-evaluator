#!/usr/bin/env python3
"""
Simple test script to verify backend functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from fastapi import FastAPI
        print("✓ FastAPI imported successfully")
        
        from pymongo import MongoClient
        print("✓ PyMongo imported successfully")
        
        from schemas.base import PyObjectId
        print("✓ PyObjectId imported successfully")
        
        from schemas.job_description import JobDescriptionCreate
        print("✓ JobDescription schemas imported successfully")
        
        from schemas.resume import ResumeCreate, ResumeUploadRequest
        print("✓ Resume schemas imported successfully")
        
        from utils.pdf_parser import PDFTextExtractor
        print("✓ PDF parser imported successfully")
        
        from services.job_description_service import JobDescriptionService
        print("✓ JobDescription service imported successfully")
        
        from services.resume_service import ResumeService
        print("✓ Resume service imported successfully")
        
        from routes.job_descriptions import router as jd_router
        print("✓ Job descriptions router imported successfully")
        
        from routes.resumes import router as resume_router
        print("✓ Resumes router imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_schemas():
    """Test schema validation"""
    try:
        from schemas.job_description import JobDescriptionCreate
        
        # Test job description creation
        jd_data = {
            "title": "Software Engineer",
            "jd_text": "We are looking for a skilled software engineer..."
        }
        jd = JobDescriptionCreate(**jd_data)
        print("✓ Job description schema validation passed")
        
        from schemas.resume import ResumeUploadRequest
        
        # Test resume upload request
        upload_data = {
            "jd_id": "507f1f77bcf86cd799439011",
            "candidate_name": "John Doe",
            "email": "john.doe@example.com"
        }
        upload_req = ResumeUploadRequest(**upload_data)
        print("✓ Resume upload request schema validation passed")
        
        return True
        
    except Exception as e:
        print(f"✗ Schema validation error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Resume Evaluator Backend...")
    print("=" * 40)
    
    # Test imports
    print("\n1. Testing imports...")
    imports_ok = test_imports()
    
    # Test schemas
    print("\n2. Testing schemas...")
    schemas_ok = test_schemas()
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY:")
    print(f"Imports: {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"Schemas: {'✓ PASS' if schemas_ok else '✗ FAIL'}")
    
    if imports_ok and schemas_ok:
        print("\n🎉 All tests passed! Backend is ready to use.")
        print("\nTo start the server, run:")
        print("  source venv/bin/activate")
        print("  python main.py")
        print("\nOr use uvicorn:")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 