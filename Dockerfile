
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy-amd64
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_SYSTEM_PYTHON=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
#RUN chmod -R 777 /app
#CMD ["uv", "run", "pytest", "-m", "debug"]


