FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (incluyendo libpq para PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando por defecto (Railway usa startCommand de railway.json)
CMD ["bash", "start.sh"]
