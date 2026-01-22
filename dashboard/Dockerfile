FROM python:3.12-slim-bookworm

WORKDIR /app

# Install uv and curl in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Use uv's built-in caching and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy application code (this layer changes most frequently)
COPY . .

# Environment variables with defaults
ENV DATA_DIR=/data
ENV REFRESH_INTERVAL_SECONDS=60

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit directly from venv (no uv sync at runtime)
ENTRYPOINT [".venv/bin/python", "-m", "streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
