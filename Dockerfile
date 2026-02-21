
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy-amd64
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --python-preference only-system && \
    uv run playwright install-deps
COPY . .
RUN chmod -R 777 /app
#CMD ["uv", "run", "pytest", "-m", "debug"]


