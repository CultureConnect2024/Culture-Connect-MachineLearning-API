FROM python:3.12.0

# Set working directory
WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

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
