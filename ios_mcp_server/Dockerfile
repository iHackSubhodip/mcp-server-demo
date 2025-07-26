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

# Create a minimal pyproject.toml for uv to work
RUN echo '[project]' > pyproject.toml && \
    echo 'name = "ios-mcp-server"' >> pyproject.toml && \
    echo 'version = "1.0.0"' >> pyproject.toml && \
    echo 'requires-python = ">=3.11"' >> pyproject.toml && \
    echo 'dependencies = [' >> pyproject.toml && \
    echo '    "fastmcp>=2.9.2",' >> pyproject.toml && \
    echo '    "starlette>=0.27.0",' >> pyproject.toml && \
    echo '    "uvicorn>=0.23.0",' >> pyproject.toml && \
    echo '    "mcp>=1.0.0",' >> pyproject.toml && \
    echo '    "aiohttp>=3.9.0",' >> pyproject.toml && \
    echo '    "appium-python-client>=3.0.0",' >> pyproject.toml && \
    echo '    "selenium>=4.15.0",' >> pyproject.toml && \
    echo '    "pillow>=10.0.0",' >> pyproject.toml && \
    echo '    "requests>=2.31.0",' >> pyproject.toml && \
    echo '    "pydantic>=2.4.0",' >> pyproject.toml && \
    echo '    "pydantic-settings>=2.0.0",' >> pyproject.toml && \
    echo ']' >> pyproject.toml

# Install dependencies
RUN uv sync --no-dev --no-cache

# Copy application code (we're already in ios_mcp_server context)
COPY . .

# Create non-root user
RUN useradd -m -u 1000 fastmcp && \
    chown -R fastmcp:fastmcp /app
USER fastmcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start command - Railway will provide PORT env var
CMD ["uv", "run", "python", "fastmcp_server.py"] 