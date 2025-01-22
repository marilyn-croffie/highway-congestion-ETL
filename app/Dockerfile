# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY scripts/ ./scripts/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set entry point (modify as needed)
CMD ["python", "scripts/your_script.py"]
