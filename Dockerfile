# Base image
FROM python:3.11.9-slim AS python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev \
        gcc \
        git \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry using recommended method
RUN curl -sSL https://install.python-poetry.org | python3 -

# Verify Poetry installation
RUN poetry --version

# Set working directory
WORKDIR /app

# Copy dependency files first for caching
COPY poetry.lock pyproject.toml ./

# Install dependencies and ensure virtualenv is created
RUN poetry install --no-root

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Start the application and make sure the virtual environment is active
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
