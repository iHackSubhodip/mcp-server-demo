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

# Debug: List what's available in build context
RUN echo "=== Build context contents ===" && ls -la

# Copy project files from root directory (build context should be set to root)
COPY pyproject.toml ./
COPY uv.lock* ./
RUN uv sync --frozen --no-dev --no-cache

# Copy application code from ios_mcp_server directory
COPY ios_mcp_server/ ./

# Create non-root user
RUN useradd -m -u 1000 fastmcp && \
    chown -R fastmcp:fastmcp /app
USER fastmcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start command - Railway will provide PORT env var
CMD ["uv", "run", "python", "fastmcp_server.py"] 