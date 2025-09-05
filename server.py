#!/usr/bin/env python3
"""
Simple HTTP MCP Server for Slack
"""
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = FastAPI()

# Initialize Slack client
slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    print("Warning: SLACK_BOT_TOKEN not found")
    slack_client = None
else:
    slack_client = WebClient(token=slack_token)

@app.get("/")
async def root():
    return {"message": "Slack MCP Server is running", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "slack-mcp-server"}

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    try:
        body = await request.json()
        method = body.get("method")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listTools": {},
                            "callTool": {}
                        }
                    },
                    "serverInfo": {
                        "name": "slack-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {
                    "tools": []
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {}
            }
            
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id", None),
            "error": {
                "code": -32600,
                "message": f"Invalid Request: {str(e)}"
            }
        }
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
