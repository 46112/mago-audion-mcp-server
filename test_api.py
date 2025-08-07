#!/usr/bin/env python3
"""
Test script for Audion MCP Server API
"""

import os
from audion.client import AudionClient

def test_api_connection():
    """Test basic API connection"""
    # API 키는 환경변수에서 가져오거나 직접 설정
    # api_key = os.getenv('AUDION_API_KEY', 'mk-h19xW7wb_tjMyja8OpOYeGgjWtzSnGajtRSF55yH7L-qvYes')
    api_key = os.getenv('AUDION_API_KEY', 'mk-vFT4wbUKFOTIKV15I4t1-lgflpk1lpjvGcVrd71jPNGRbsWl')
    
    try:
        # 클라이언트 초기화
        client = AudionClient(api_key=api_key)
        print("✅ AudionClient 초기화 성공")
        
        return True
        
    except Exception as e:
        print(f"❌ API 연결 실패: {e}")
        return False

def test_url_processing():
    """Test URL-based audio processing"""
    api_key = os.getenv('AUDION_API_KEY', 'mk-h19xW7wb_tjMyja8OpOYeGgjWtzSnGajtRSF55yH7L-qvYes')
    
    try:
        client = AudionClient(api_key=api_key)
        
        # YouTube URL 테스트 (예시)
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll
        
        print(f"🔗 URL 처리 테스트: {test_url}")
        result = client.flow(
            flow="audion_vu",
            input_type="url",
            input=test_url
        )
        
        print(f"✅ URL 처리 결과: {result}")
        return True
        
    except Exception as e:
        print(f"❌ URL 처리 실패: {e}")
        return False

def main():
    print("🎵 Audion MCP Server API 테스트 시작\n")
    
    # 1. 기본 연결 테스트
    print("1. 기본 API 연결 테스트")
    connection_ok = test_api_connection()
    
    if connection_ok:
        print("\n2. URL 처리 테스트")
        url_ok = test_url_processing()
        
        if url_ok:
            print("\n🎉 모든 테스트 통과!")
        else:
            print("\n⚠️ URL 처리 테스트 실패")
    else:
        print("\n❌ API 연결 테스트 실패")

if __name__ == "__main__":
    main() 