
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy-amd64
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --python-preference only-system && \
    uv run playwright install --with-deps
COPY . .
RUN chmod -R 777 /app
#CMD ["uv", "run", "pytest", "-m", "debug"]


