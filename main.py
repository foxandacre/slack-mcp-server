#!/usr/bin/env python3
import os
import sys

# Try to import the slack-mcp-server package
try:
    from slack_mcp_server import main
    if __name__ == "__main__":
        main()
except ImportError:
    print("Error: slack-mcp-server package not found")
    print("Make sure it's installed via: pip install slack-mcp-server")
    sys.exit(1)
