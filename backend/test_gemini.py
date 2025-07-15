#!/usr/bin/env python3
"""
Test script for Gemini AI integration
"""

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_import():
    """Test that Gemini SDK can be imported"""
    try:
        from google import genai
        print("✓ Google Gemini SDK imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import Google Gemini SDK: {e}")
        return False

def test_gemini_client():
    """Test Gemini client initialization"""
    try:
        from services.gemini_client import GeminiClient
        
        # Check if API key is set
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠ GEMINI_API_KEY not set in environment")
            print("  Please set GEMINI_API_KEY in your .env file")
            return False
        
        # Initialize client
        client = GeminiClient()
        print("✓ Gemini client initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to initialize Gemini client: {e}")
        return False

def test_gemini_connection():
    """Test Gemini API connection"""
    try:
        from services.gemini_client import GeminiClient
        
        client = GeminiClient()
        is_connected = client.test_connection()
        
        if is_connected:
            print("✓ Gemini API connection successful")
            return True
        else:
            print("✗ Gemini API connection failed")
            return False
            
    except Exception as e:
        print(f"✗ Gemini connection test error: {e}")
        return False

def test_evaluation_prompt():
    """Test evaluation prompt creation"""
    try:
        from services.gemini_client import GeminiClient
        
        client = GeminiClient()
        
        # Sample resume data
        resume_data = {
            "candidate_name": "John Doe",
            "skills": ["Python", "FastAPI", "MongoDB"],
            "education": [
                {
                    "degree": "Bachelor of Science in Computer Science",
                    "institution": "University of Technology",
                    "year": 2020,
                    "gpa": 3.8
                }
            ],
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "start_date": "2020-06",
                    "end_date": "Present",
                    "description": "Developed web applications using Python and FastAPI"
                }
            ],
            "raw_text": "John Doe is a software engineer with 3 years of experience..."
        }
        
        jd_text = "We are looking for a Python developer with experience in FastAPI and MongoDB..."
        
        prompt = client._create_evaluation_prompt(resume_data, jd_text)
        
        if "John Doe" in prompt and "Python" in prompt and "FastAPI" in prompt:
            print("✓ Evaluation prompt creation successful")
            return True
        else:
            print("✗ Evaluation prompt creation failed")
            return False
            
    except Exception as e:
        print(f"✗ Evaluation prompt test error: {e}")
        return False

def test_evaluation_service():
    """Test evaluation service integration"""
    try:
        from services.evaluation_service import EvaluationService
        
        service = EvaluationService()
        print("✓ Evaluation service initialized successfully")
        
        # Test Gemini connection through service
        connection_test = service.test_gemini_connection()
        print(f"  Gemini connection status: {connection_test['status']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Evaluation service test error: {e}")
        return False

def main():
    """Run all Gemini tests"""
    print("Testing Gemini AI Integration...")
    print("=" * 50)
    
    tests = [
        ("Gemini SDK Import", test_gemini_import),
        ("Gemini Client Initialization", test_gemini_client),
        ("Gemini API Connection", test_gemini_connection),
        ("Evaluation Prompt Creation", test_evaluation_prompt),
        ("Evaluation Service Integration", test_evaluation_service),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All Gemini tests passed! AI evaluation is ready to use.")
        print("\nTo test the evaluation endpoint:")
        print("1. Start the server: python main.py")
        print("2. Create a job description and upload a resume")
        print("3. Call POST /api/evaluations/evaluate with resume_id and jd_id")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        if not any(name == "Gemini API Connection" and result for name, result in results):
            print("\n💡 Make sure to:")
            print("  1. Set GEMINI_API_KEY in your .env file")
            print("  2. Get a valid API key from Google AI Studio")
            print("  3. Ensure you have internet connectivity")
        sys.exit(1)

if __name__ == "__main__":
    main() 