#!/usr/bin/env python3
"""
Simple script to test SITAC credentials
Run this to verify your credentials before using the Django integration
"""
import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sitac_credentials():
    """Test SITAC credentials with basic authentication"""
    
    # Get credentials from environment
    username = os.getenv('SITAC_USERNAME', '')
    password = os.getenv('SITAC_PASSWORD', '')
    base_url = os.getenv('SITAC_BASE_URL', 'https://crea-to.sitac.com.br/app/webservices')
    
    if not username or not password:
        print("❌ SITAC_USERNAME and SITAC_PASSWORD must be set in .env file")
        return False
    
    print(f"🔐 Testing credentials for user: {username}")
    print(f"🔗 URL: {base_url}/auth/login")
    print(f"📝 Password length: {len(password)} characters")
    print(f"🔍 Password contains special chars: {any(c in password for c in '()[]{}!@#$%^&*')}")
    
    # Create basic auth header
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    print(f"🔑 Encoded credentials (first 20 chars): {encoded_credentials[:20]}...")
    
    # Make request
    url = f"{base_url}/auth/login"
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none'
    }
    
    try:
        print("🚀 Making request...")
        response = requests.post(url, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Credentials are valid")
            try:
                data = response.json()
                print(f"🎫 Access Token: {data.get('access_token', 'N/A')[:20]}...")
                print(f"⏰ Expires In: {data.get('expires_in', 'N/A')} seconds")
                return True
            except:
                print("⚠️  Response is not JSON")
                print(f"📄 Response content: {response.text[:200]}...")
                return True
        elif response.status_code == 401:
            print("❌ UNAUTHORIZED - Invalid credentials")
            print(f"📄 Response: {response.text}")
            return False
        elif response.status_code == 403:
            print("❌ FORBIDDEN - Credentials might be correct but access denied")
            print(f"📄 Response: {response.text}")
            return False
        else:
            print(f"❌ ERROR - Unexpected status code: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 SITAC Credentials Test")
    print("=" * 50)
    
    success = test_sitac_credentials()
    
    print("=" * 50)
    if success:
        print("🎉 Test completed successfully!")
    else:
        print("💥 Test failed. Check your credentials and try again.")
        print("\n💡 Tips:")
        print("   - Make sure your .env file is in the project root")
        print("   - Check that SITAC_USERNAME and SITAC_PASSWORD are correct")
        print("   - Special characters in passwords should work fine")
        print("   - Contact SITAC support if credentials are correct but access is denied")
