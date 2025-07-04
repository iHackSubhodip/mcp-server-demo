# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_TRANSPORT=sse \
    MCP_HOST=0.0.0.0 \
    PYTHONPATH=/app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Debug: List what's available in build context
RUN echo "=== Build context contents ===" && ls -la

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (current directory is already ios_mcp_server)
COPY . .

# Create non-root user
RUN useradd -m -u 1000 fastmcp && \
    chown -R fastmcp:fastmcp /app
USER fastmcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start command - Railway will provide PORT env var
CMD ["python", "fastmcp_server.py"] 