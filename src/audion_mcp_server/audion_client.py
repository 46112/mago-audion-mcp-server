#!/usr/bin/env python3
"""Audion API Client for MCP Server."""

import json
import requests
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AudionConfig(BaseModel):
    """Configuration for Audion API client."""
    api_key: str = Field(..., description="The API key for Audion service")
    base_url: str = Field(default="https://audion.magovoice.com/go-framework/v1/go", description="The base URL of the server")
    timeout: int = Field(default=300, description="The timeout of the server")


class AudionClient:
    """Audion API client for voice processing."""
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """Initialize the Audion client."""
        if not api_key:
            raise ValueError("api_key is required")
        
        self.config = AudionConfig(
            api_key=api_key,
            base_url=base_url or "https://audion.magovoice.com/go-framework/v1/go",
            timeout=timeout or 300
        )
    
    def flow(
        self,
        flow: str,
        input_type: str,
        input: str,
    ) -> Dict[str, Any]:
        """
        Call the Audion API with the given flow, input type, and input.

        Args:
            flow: The flow to call (audion_vu or audion_vh)
            input_type: The type of the input ("file" or "url")
            input: The input to the flow (file path or URL)

        Returns:
            Dict containing the API response
        """
        headers = {
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        url = f"{self.config.base_url}/flow"
        
        try:
            if input_type == "file":
                # File upload
                with open(input, "rb") as f:
                    files = {"file": (input, f, "application/octet-stream")}
                    data = {
                        "flow": flow,
                        "input_type": input_type,
                        "input": input,
                    }
                    
                    response = requests.post(
                        url,
                        headers=headers,
                        data=data,
                        files=files,
                        timeout=self.config.timeout
                    )
            
            elif input_type == "url":
                # URL processing
                data = {
                    "flow": flow,
                    "input_type": input_type,
                    "input": input,
                }
                
                response = requests.post(
                    url,
                    headers=headers,
                    data=data,
                    timeout=self.config.timeout
                )
            
            else:
                raise ValueError(f"Unsupported input type: {input_type}")
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
            return response.json()
            
        except Exception as e:
            raise Exception(f"Failed to call Audion API: {str(e)}")
    
    def process_voice_understanding(
        self,
        input_source: str,
        language: Optional[str] = None,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Process voice understanding using audion_vu flow.
        
        Args:
            input_source: File path or URL
            language: Language code (optional)
            format: Output format (json, text, srt)
            
        Returns:
            Dict containing the processing result
        """
        # Determine input type
        input_type = "url" if self._is_url(input_source) else "file"
        
        # Call the API
        result = self.flow("audion_vu", input_type, input_source)
        
        # Format the response based on requested format
        return self._format_vu_response(result, format)
    
    def process_voice_highlighting(
        self,
        input_source: str,
        highlight_keywords: list[str],
        language: Optional[str] = None,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Process voice highlighting using audion_vh flow.
        
        Args:
            input_source: File path or URL
            highlight_keywords: List of keywords to highlight
            language: Language code (optional)
            format: Output format (json, text, html)
            
        Returns:
            Dict containing the processing result
        """
        # Determine input type
        input_type = "url" if self._is_url(input_source) else "file"
        
        # Call the API
        result = self.flow("audion_vh", input_type, input_source)
        
        # Format the response based on requested format
        return self._format_vh_response(result, highlight_keywords, format)
    
    def _is_url(self, source: str) -> bool:
        """Check if the input source is a URL."""
        return source.startswith(('http://', 'https://', 'youtu.be', 'www.youtube.com'))
    
    def _format_vu_response(self, result: Dict[str, Any], format: str) -> Dict[str, Any]:
        """Format voice understanding response."""
        if format == "json":
            return result
        elif format == "text":
            # Extract transcript text
            transcript = ""
            if "content" in result and "output" in result["content"]:
                output = result["content"]["output"]
                if "utterances" in output:
                    for utterance in output["utterances"]:
                        transcript += utterance.get("text", "") + " "
            return {"transcript": transcript.strip()}
        elif format == "srt":
            # Generate SRT format
            srt_content = ""
            if "content" in result and "output" in result["content"]:
                output = result["content"]["output"]
                if "utterances" in output:
                    for i, utterance in enumerate(output["utterances"], 1):
                        start_time = utterance.get("start", 0)
                        end_time = utterance.get("end", 0)
                        text = utterance.get("text", "")
                        
                        # Convert to SRT time format
                        start_srt = self._seconds_to_srt_time(start_time)
                        end_srt = self._seconds_to_srt_time(end_time)
                        
                        srt_content += f"{i}\n{start_srt} --> {end_srt}\n{text}\n\n"
            
            return {"srt_content": srt_content.strip()}
        else:
            return result
    
    def _format_vh_response(self, result: Dict[str, Any], keywords: list[str], format: str) -> Dict[str, Any]:
        """Format voice highlighting response."""
        if format == "json":
            return result
        elif format == "text":
            # Extract highlighted text
            highlighted_text = ""
            if "content" in result and "output" in result["content"]:
                output = result["content"]["output"]
                if "utterances" in output:
                    for utterance in output["utterances"]:
                        text = utterance.get("text", "")
                        # Highlight keywords in text
                        for keyword in keywords:
                            if keyword.lower() in text.lower():
                                text = text.replace(keyword, f"**{keyword}**")
                        highlighted_text += text + " "
            return {"highlighted_text": highlighted_text.strip()}
        elif format == "html":
            # Generate HTML with highlights
            html_content = "<div class='transcript'>"
            if "content" in result and "output" in result["content"]:
                output = result["content"]["output"]
                if "utterances" in output:
                    for utterance in output["utterances"]:
                        text = utterance.get("text", "")
                        start_time = utterance.get("start", 0)
                        
                        # Highlight keywords
                        for keyword in keywords:
                            if keyword.lower() in text.lower():
                                text = text.replace(keyword, f"<mark class='highlight'>{keyword}</mark>")
                        
                        html_content += f"<p data-time='{start_time}'>{text}</p>"
            html_content += "</div>"
            return {"html_content": html_content}
        else:
            return result
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}" 