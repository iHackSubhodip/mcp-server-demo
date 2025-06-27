#!/bin/bash

# iOS MCP Server Startup Script
# This script ensures Appium is running and starts the MCP server

# Set paths
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
cd "$(dirname "$0")"

# Function to check if Appium is running
check_appium() {
    curl -s http://localhost:4723/status > /dev/null 2>&1
    return $?
}

# Start Appium if not running
if ! check_appium; then
    echo "Starting Appium server..." >&2
    appium server --port 4723 > appium.log 2>&1 &
    
    # Wait for Appium to start
    for i in {1..10}; do
        if check_appium; then
            echo "Appium server started successfully" >&2
            break
        fi
        echo "Waiting for Appium to start... ($i/10)" >&2
        sleep 2
    done
    
    if ! check_appium; then
        echo "Failed to start Appium server" >&2
        exit 1
    fi
else
    echo "Appium server is already running" >&2
fi

# Activate virtual environment and start the iOS MCP server
echo "Starting iOS MCP Server..." >&2
source ios_mcp_env/bin/activate
exec python3 -m ios_mcp_server.main 