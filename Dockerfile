# Use an official, lightweight Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy just the requirements first (this makes future builds faster)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our application code into the container
COPY . .

# Expose port 8000 so the outside world can talk to our app
EXPOSE 8000

# The command to run when the container starts
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]