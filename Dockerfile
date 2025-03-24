# Use the official Python image as base
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Expose the application port
EXPOSE 8000

# Run Django development server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
