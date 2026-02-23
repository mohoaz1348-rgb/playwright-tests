
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy-amd64
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV UV_CACHE_DIR=/tmp/uv_cache

RUN uv sync --frozen --no-install-project --python-preference only-system && \
    rm -rf /tmp/uv_cache
#RUN uv sync --frozen --python-preference only-system
COPY . .
#RUN chmod -R 777 /app
#CMD ["uv", "run", "pytest", "-m", "debug"]


