#!/usr/bin/env python3
"""
HTTP-based Slack MCP Server for Railway deployment
"""
import os
import sys
from slack_mcp_server_stateless import main

if __name__ == "__main__":
    # Set default port for Railway
    port = int(os.environ.get("PORT", 8080))
    sys.argv = ["server.py", "--port", str(port)]
    main()
