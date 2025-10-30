# --- Build Stage ---
# Use Python 3.10 as a stable, modern base.
FROM python:3.10-slim-bullseye AS builder

# Set environment variables for Python
# Fixed syntax: ENV KEY=VALUE
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
# libpq-dev is required to build psycopg2 (in your requirements.txt)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy requirements.txt first to leverage Docker layer caching
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# --- Final Stage ---
FROM python:3.10-slim-bullseye

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app

# Set the working directory
WORKDIR /app

# Copy installed wheels from the builder stage
COPY --from=builder /app/wheels /wheels

# Install dependencies from wheels (this is faster)
RUN pip install --no-cache /wheels/*

# Copy your entire Django project code into the container
COPY . .

# Run collectstatic
# This uses your settings.py to find STATIC_ROOT and collect files
# This will now use the dummy SQLite DB (from the settings.py fix) and succeed
RUN python manage.py collectstatic --no-input

# Change ownership of the app directory to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port Gunicorn will run on
# 8080 is the default port Cloud Run expects
EXPOSE 8080

# Run the app
# This is specialized for your project's WSGI application path
#
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "laboratory_sample_tracker.wsgi:application"]