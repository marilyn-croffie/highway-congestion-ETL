# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY scripts/ ./scripts/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Submit dags to airflow
FROM apache/airflow:2.7.2
USER airflow
COPY dags/ /opt/airflow/dags/
RUN pip install kafka-python

# Set entry point (modify as needed)
CMD ["python", "scripts/your_script.py"]
