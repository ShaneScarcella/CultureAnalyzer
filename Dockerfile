# Stage 1: Build the frontend
# We use a specific version of Node.js for reproducibility.
# The 'alpine' variant is smaller and a good choice for build stages.
FROM node:18-alpine AS frontend-builder

# Set the working directory for the frontend inside the container
WORKDIR /app/frontend

# Copy package.json and package-lock.json (or yarn.lock) first.
# This leverages Docker's layer caching. Dependencies are only re-installed
# if these files change, which speeds up subsequent builds.
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ ./

# Build the frontend application for production.
# This command might be different for your project (e.g., 'npm run build:prod').
# Check your package.json "scripts" section.
RUN npm run build


# Stage 2: Build and run the backend (Final Image)
# Use a slim Python image for a smaller final image size.
FROM python:3.10-slim

# Set environment variables to ensure logs are sent straight to the terminal
# and to prevent Python from writing .pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory for the application
WORKDIR /app

# Before copying code, install Python dependencies.
# This also takes advantage of Docker's layer caching.
# You'll need to create a requirements.txt file for this to work.
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY backend/ .

# Copy the built frontend from the 'frontend-builder' stage.
# This assumes your backend serves static files from a 'static' directory.
# Adjust the destination path (e.g., './public', './build') based on your backend framework (Flask, Django, etc.).
COPY --from=frontend-builder /app/frontend/build ./static

# Expose the port the backend server will run on.
# This should match the port your application listens on.
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]