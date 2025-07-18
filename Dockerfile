# Use official Python image on Bullseye
FROM python:3.8-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y libsndfile1

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
