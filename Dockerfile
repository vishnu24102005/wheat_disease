<<<<<<< HEAD
# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run app using gunicorn (production server)
=======
# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run app using gunicorn (production server)
>>>>>>> d2683fb (full version)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]