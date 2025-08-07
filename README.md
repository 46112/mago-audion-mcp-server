# Audion MCP Server

음성 이해 및 하이라이트 기능을 제공하는 MCP (Model Context Protocol) 서버입니다.

## 기능

### 1. Audion VU (Voice Understanding)
- 오디오/비디오 파일 또는 URL에서 음성을 텍스트로 변환
- 지원 입력: 로컬 파일 경로, HTTP/HTTPS URL
- 지원 출력 형식: JSON, 텍스트, SRT 자막

### 2. Audion VH (Voice Highlighting)  
- 오디오/비디오에서 특정 키워드 하이라이트 및 시간 추출
- 지원 입력: 로컬 파일 경로, HTTP/HTTPS URL
- 지원 출력 형식: JSON, 텍스트, HTML

## 4가지 사용 케이스

1. **파일 + VU**: 로컬 오디오 파일의 음성을 텍스트로 변환
2. **파일 + VH**: 로컬 오디오 파일에서 키워드 하이라이트
3. **URL + VU**: 온라인 오디오/비디오의 음성을 텍스트로 변환  
4. **URL + VH**: 온라인 오디오/비디오에서 키워드 하이라이트

## 설치 및 실행

```bash
# 의존성 설치 (uv 사용)
uv sync

# 서버 실행
python run_server.py
```

## MCP 도구 사용법

### audion_vu (음성 이해)
```json
{
  "input_source": "/path/to/audio.mp3" or "https://example.com/audio.mp3",
  "language": "ko",
  "format": "json"
}
```

### audion_vh (음성 하이라이트)
```json
{
  "input_source": "/path/to/audio.mp3" or "https://example.com/audio.mp3", 
  "highlight_keywords": ["키워드1", "키워드2"],
  "language": "ko",
  "format": "json"
}
```

## 개발 환경

- Python ≥ 3.11
- uv 패키지 관리
- MCP 1.1.0+

## 실제 API 연동

✅ **완료**: 실제 Audion API와 연동되어 있습니다!

- **Voice Understanding**: YouTube URL 및 로컬 파일에서 음성 인식
- **Voice Highlighting**: 키워드 기반 음성 하이라이트 및 시간 추출
- **다양한 출력 형식**: JSON, 텍스트, SRT, HTML 지원

## 테스트

```bash
# MCP 서버 테스트
uv run python test_mcp_server.py

# 서버 실행
uv run python run_server.py
```

## 환경 변수

```bash
export AUDION_API_KEY="your-api-key-here"
```