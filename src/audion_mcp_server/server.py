#!/usr/bin/env python3
"""Audion MCP Server - Voice understanding and highlighting tools."""

import asyncio
import json
import os
from typing import Any, Dict, Optional

from mcp.server.models import InitializationOptions
from mcp.server import Server, NotificationOptions
from mcp.types import Tool
import mcp.server.stdio
import mcp.types as types
from pydantic import BaseModel, Field
from pathlib import Path
from datetime import datetime

from .audion_client import AudionClient


server = Server("audion-mcp-server")

# Initialize Audion client with API key from environment
AUDION_API_KEY = os.getenv("AUDION_API_KEY", "mk-vFT4wbUKFOTIKV15I4t1-lgflpk1lpjvGcVrd71jPNGRbsWl")
audion_client = AudionClient(api_key=AUDION_API_KEY)


class AudionVuInput(BaseModel):
    """Input parameters for Audion Voice Understanding."""
    input_source: str = Field(description="File path or URL to audio/video content")
    language: Optional[str] = Field(default=None, description="Language code (e.g., 'ko', 'en')")
    format: Optional[str] = Field(default="json", description="Output format: json, text, srt")


class AudionSubtitleInput(BaseModel):
    """Input parameters for Audion Subtitle Download."""
    input_source: str = Field(description="File path or URL to audio/video content")
    output_path: Optional[str] = Field(default=None, description="Output path for subtitle file (defaults to ./subtitles/)")
    language: Optional[str] = Field(default=None, description="Language code (e.g., 'ko', 'en')")
    format: Optional[str] = Field(default="srt", description="Subtitle format: srt, vtt, txt")


class AudionVhInput(BaseModel):
    """Input parameters for Audion Voice Highlighting."""
    input_source: str = Field(description="File path or URL to audio/video content")
    highlight_keywords: list[str] = Field(description="Keywords to highlight in the transcript")
    language: Optional[str] = Field(default=None, description="Language code (e.g., 'ko', 'en')")
    format: Optional[str] = Field(default="json", description="Output format: json, text, html")


async def audion_vu_process(input_source: str, language: Optional[str] = None, format: str = "json") -> Dict[str, Any]:
    """Process voice understanding using Audion VU API."""
    try:
        # Use the actual Audion client to process voice understanding
        result = audion_client.process_voice_understanding(
            input_source=input_source,
            language=language,
            format=format
        )
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process voice understanding: {str(e)}",
            "source": input_source
        }


async def audion_vh_process(input_source: str, highlight_keywords: list[str], language: Optional[str] = None, format: str = "json") -> Dict[str, Any]:
    """Process voice highlighting using Audion VH API."""
    try:
        # Use the actual Audion client to process voice highlighting
        result = audion_client.process_voice_highlighting(
            input_source=input_source,
            highlight_keywords=highlight_keywords,
            language=language,
            format=format
        )
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process voice highlighting: {str(e)}",
            "source": input_source,
            "highlight_keywords": highlight_keywords
        }


async def audion_subtitle_download(input_source: str, output_path: Optional[str] = None, language: Optional[str] = None, format: str = "srt") -> Dict[str, Any]:
    """Generate and download subtitle file from audio/video content."""
    try:
        # Get the transcription in the requested subtitle format
        result = audion_client.process_voice_understanding(
            input_source=input_source,
            language=language,
            format=format
        )
        
        # Determine output path
        if output_path is None:
            # Create default subtitles directory
            subtitle_dir = Path("./subtitles")
            subtitle_dir.mkdir(exist_ok=True)
            
            # Generate filename based on source
            if input_source.startswith(('http://', 'https://')):
                # Extract video ID or title from URL
                filename_base = input_source.split('/')[-1].split('?')[0].split('.')[0]
                if not filename_base:
                    filename_base = f"subtitle_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            else:
                # Use input filename without extension
                filename_base = Path(input_source).stem
            
            output_path = subtitle_dir / f"{filename_base}.{format}"
        else:
            output_path = Path(output_path)
            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Extract subtitle content based on format
        subtitle_content = ""
        if format == "srt" and "srt_content" in result:
            subtitle_content = result["srt_content"]
        elif format == "vtt" and "srt_content" in result:
            # Convert SRT to VTT format
            srt_content = result["srt_content"]
            subtitle_content = "WEBVTT\n\n" + srt_content.replace(',', '.')
        elif format == "txt" and "transcript" in result:
            subtitle_content = result["transcript"]
        elif "srt_content" in result:
            subtitle_content = result["srt_content"]
        else:
            # Fallback to raw JSON if format not recognized
            subtitle_content = json.dumps(result, indent=2, ensure_ascii=False)
        
        # Write subtitle file
        output_path.write_text(subtitle_content, encoding='utf-8')
        
        return {
            "status": "success",
            "message": f"Subtitle file saved successfully",
            "output_path": str(output_path.absolute()),
            "format": format,
            "size": len(subtitle_content),
            "source": input_source
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to generate subtitle file: {str(e)}",
            "source": input_source
        }


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="audion_vu",
            description="Voice Understanding - Transcribe audio/video content from file or URL",
            inputSchema=AudionVuInput.model_json_schema(),
        ),
        Tool(
            name="audion_vh",
            description="Voice Highlighting - Find and highlight specific keywords in audio/video content",
            inputSchema=AudionVhInput.model_json_schema(),
        ),
        Tool(
            name="audion_subtitle",
            description="Download subtitle file - Generate and save subtitle file from audio/video content",
            inputSchema=AudionSubtitleInput.model_json_schema(),
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool execution."""
    if arguments is None:
        raise ValueError("Arguments are required")

    try:
        if name == "audion_vu":
            input_data = AudionVuInput(**arguments)
            result = await audion_vu_process(
                input_data.input_source,
                input_data.language,
                input_data.format
            )
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "audion_vh":
            input_data = AudionVhInput(**arguments)
            result = await audion_vh_process(
                input_data.input_source,
                input_data.highlight_keywords,
                input_data.language,
                input_data.format
            )
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "audion_subtitle":
            input_data = AudionSubtitleInput(**arguments)
            result = await audion_subtitle_download(
                input_data.input_source,
                input_data.output_path,
                input_data.language,
                input_data.format
            )
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point for the server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="audion-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())