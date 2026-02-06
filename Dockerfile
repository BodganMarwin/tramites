# Dockerfile for the Django project
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

# Add entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "tramites.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

###################################################################################
# Dockerfile for building a development environment
# Imagen base
# FROM python:3.10-slim

# # Evitar que Python genere archivos .pyc
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Crear directorio de trabajo
# WORKDIR /app

# # Instalar dependencias del sistema
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copiar requirements
# COPY requirements.txt /app/

# # Instalar dependencias Python
# RUN pip install --no-cache-dir -r requirements.txt

# # Copiar el proyecto completo
# COPY . /app/

# # Exponer el puerto
# EXPOSE 8000

# # Comando por defecto
# CMD ["python", "manage.py", "collectstatic", "--noinput"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
