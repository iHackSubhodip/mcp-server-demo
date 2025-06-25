#!/bin/bash
# iOS MCP Server Launcher
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Starting iOS MCP Server..."
echo "📁 Project: $SCRIPT_DIR"

# Change to the project directory
cd "$SCRIPT_DIR"

# Activate virtual environment and start server
source "./ios_mcp_env/bin/activate"
python3 ios_mcp_server.py

echo "✅ Server started successfully!"
