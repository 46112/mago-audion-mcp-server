#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

from pathlib import Path
from .constants import AUDIO_FILE_EXTENSION, VIDEO_FILE_EXTENSION

def get_media_type(file_path: str) -> str:
    """
    Get the media type of the file.
    """
    extension = Path(file_path).suffix.lower()
    if extension in AUDIO_FILE_EXTENSION:
        return "audio/wav"
    elif extension in VIDEO_FILE_EXTENSION:
        return "video/mp4"
    else:
        raise ValueError(f"Unsupported file extension: {extension}")