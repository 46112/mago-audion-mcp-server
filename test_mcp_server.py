#!/usr/bin/env python3
"""Test script for Audion MCP Server."""

import asyncio
import json
import os
from src.audion_mcp_server.server import audion_vu_process, audion_vh_process


async def test_voice_understanding():
    """Test voice understanding with YouTube URL."""
    print("🎵 Testing Voice Understanding (audion_vu)")
    
    # Test with YouTube URL
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        result = await audion_vu_process(
            input_source=test_url,
            language="ko",
            format="json"
        )
        
        print("✅ Voice Understanding Test Result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Test SRT format
        srt_result = await audion_vu_process(
            input_source=test_url,
            format="srt"
        )
        
        print("\n📝 SRT Format Test:")
        if "srt_content" in srt_result:
            print(srt_result["srt_content"])
        else:
            print("No SRT content available")
            
    except Exception as e:
        print(f"❌ Voice Understanding Test Failed: {e}")


async def test_voice_highlighting():
    """Test voice highlighting with YouTube URL."""
    print("\n🎯 Testing Voice Highlighting (audion_vh)")
    
    # Test with YouTube URL
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    keywords = ["교육", "퀴즈", "중간고사"]
    
    try:
        result = await audion_vh_process(
            input_source=test_url,
            highlight_keywords=keywords,
            language="ko",
            format="json"
        )
        
        print("✅ Voice Highlighting Test Result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Test HTML format
        html_result = await audion_vh_process(
            input_source=test_url,
            highlight_keywords=keywords,
            format="html"
        )
        
        print("\n🌐 HTML Format Test:")
        if "html_content" in html_result:
            print(html_result["html_content"])
        else:
            print("No HTML content available")
            
    except Exception as e:
        print(f"❌ Voice Highlighting Test Failed: {e}")


async def main():
    """Main test function."""
    print("🚀 Audion MCP Server Test Suite")
    print("=" * 50)
    
    # Set API key if not already set
    if not os.getenv("AUDION_API_KEY"):
        os.environ["AUDION_API_KEY"] = "mk-vFT4wbUKFOTIKV15I4t1-lgflpk1lpjvGcVrd71jPNGRbsWl"
    
    # Run tests
    await test_voice_understanding()
    await test_voice_highlighting()
    
    print("\n🎉 Test Suite Completed!")


if __name__ == "__main__":
    asyncio.run(main()) 