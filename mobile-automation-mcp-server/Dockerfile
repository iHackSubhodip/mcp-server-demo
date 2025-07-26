# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_TRANSPORT=sse \
    MCP_HOST=0.0.0.0 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv

# Copy project files
COPY . .

# Install dependencies with uv (no package building)
RUN uv venv && \
    uv pip install --no-cache \
    "fastmcp>=2.9.2" \
    "starlette>=0.27.0" \
    "uvicorn>=0.23.0" \
    "mcp>=1.0.0" \
    "aiohttp>=3.9.0" \
    "appium-python-client>=3.0.0" \
    "selenium>=4.15.0" \
    "pillow>=10.0.0" \
    "requests>=2.31.0" \
    "pydantic>=2.4.0" \
    "pydantic-settings>=2.0.0"

# Create non-root user
RUN useradd -m -u 1000 fastmcp && \
    chown -R fastmcp:fastmcp /app
USER fastmcp

# Activate virtual environment for CMD
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start command
CMD ["python", "fastmcp_server.py"] 