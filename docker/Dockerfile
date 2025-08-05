# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r django && useradd -r -g django django

# Copy requirements and install Python dependencies
COPY backend/requirements-prod.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY backend/ /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /var/log/django \
    && chown -R django:django /app /var/log/django

# Collect static files
RUN python manage.py collectstatic --noinput --settings=accessibility_api.prod_settings

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python manage.py check --deploy --settings=accessibility_api.prod_settings || exit 1

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "accessibility_api.wsgi:application"]
