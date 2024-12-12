FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Debug step: verify files copied into container
RUN ls -la /app

# Copy the rest of the application code
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8080

# Set the entrypoint to run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
