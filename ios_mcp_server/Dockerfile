# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_TRANSPORT=sse \
    MCP_HOST=0.0.0.0 \
    PYTHONPATH=/app

# Install dependencies with retry and optimization
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install uv using the installer script (more reliable)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv

# Copy pyproject.toml first for dependency caching
COPY pyproject.toml .

# Install dependencies only (no editable install)
RUN uv pip install --system --no-cache-dir \
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

# Copy application code
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