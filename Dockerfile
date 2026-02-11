FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps required by reportlab/pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

# Ensure data and storage dirs exist
RUN mkdir -p /app/data /app/storage/payslips /app/storage/exports

ENV PORT=10000
EXPOSE 10000

CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker src.app.main:app --bind 0.0.0.0:${PORT} --workers 1"]
