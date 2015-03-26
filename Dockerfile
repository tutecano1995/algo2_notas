# -*- docker-image-name: "fiuba/notas" -*-

# Debian stable (wheezy).
FROM debian:7

# Dependencias.
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive \
      apt-get install -y python python-webpy python-gdata

# Copiar la applicación (menos los ficheros en .dockerfile).
COPY . /app/
WORKDIR /app

# Por omisión, web.py usa el puerto 8080.
EXPOSE 8080

ENTRYPOINT ["python", "notasweb.py"]
