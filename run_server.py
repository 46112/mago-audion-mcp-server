#!/usr/bin/env python3
"""Development script to run the Audion MCP Server."""

import asyncio
from src.audion_mcp_server.server import main

if __name__ == "__main__":
    asyncio.run(main())