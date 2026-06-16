FROM python:3.10-slim

WORKDIR /app

# system dependencies (IMPORTANT for OpenCV + TF stability)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip (CRITICAL FIX)
RUN pip install --upgrade pip

COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
