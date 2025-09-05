#!/usr/bin/env python3
"""
Slack MCP Server
"""
import os
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Slack client
slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    raise ValueError("SLACK_BOT_TOKEN environment variable is required")

slack_client = WebClient(token=slack_token)

# Create MCP server
server = Server("slack-mcp")

@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        {
            "name": "list_channels",
            "description": "List Slack channels",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        }
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls"""
    if name == "list_channels":
        try:
            response = slack_client.conversations_list()
            channels = response["channels"]
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Found {len(channels)} channels: " + ", ".join([c["name"] for c in channels[:10]])
                    }
                ]
            }
        except SlackApiError as e:
            return {
                "content": [
                    {
                        "type": "text", 
                        "text": f"Error: {e.response['error']}"
                    }
                ]
            }
    
    return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

async def main():
    """Main server function"""
    async with stdio_server() as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
