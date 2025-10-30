# --- Build Stage ---
# Use an official Python runtime as a parent image
# Using 3.10 as a stable, modern choice.
FROM python:3.10-slim-bullseye AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# libpq-dev is required for psycopg2 (which you use)
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

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Set the working directory
WORKDIR /app

# Copy installed wheels from the builder stage
COPY --from=builder /app/wheels /wheels

# Install dependencies from wheels (faster)
# Gunicorn is our production server
RUN pip install --no-cache /wheels/*

# Copy the rest of your Django project code
COPY . .

# Run collectstatic
# This finds your manage.py and collects static files into STATIC_ROOT
RUN python manage.py collectstatic --no-input

# Change ownership to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port Gunicorn will run on
# 8080 is the default port Cloud Run listens to
EXPOSE 8080

# Run the app
# This is now specialized for your project's 'laboratory_sample_tracker.wsgi' file
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "laboratory_sample_tracker.wsgi:application"]

