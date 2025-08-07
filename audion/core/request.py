#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

import requests
from typing import Optional, Dict, Any

from .config import PRODUCTION_URL, TIMEOUT


class Request:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.base_url = base_url or PRODUCTION_URL
        self.timeout = time

    def __call__(
        self,
        flow: str,
        input_type: str,
        input: str,
    ):