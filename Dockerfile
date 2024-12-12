FROM python:3.12.0

# Set working directory
WORKDIR /app

# Upgrade pip, setuptools, and wheel to the latest versions
RUN pip install --upgrade pip setuptools wheel

# Install build tools
RUN apt-get update && apt-get install -y build-essential libffi-dev libssl-dev python3-dev cargo

# Copy requirements file
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port that your app will run on
EXPOSE 8080

# Start the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
