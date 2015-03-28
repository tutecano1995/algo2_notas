# -*- docker-image-name: "fiuba/notas" -*-

# Debian jessie porque wheezy no tiene python-oauth2client.
FROM debian:8

# Dependencias.
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive \
      apt-get install -y python python-webpy python-gdata python-oauth2client

# Copiar la applicación (menos los ficheros en .dockerfile).
COPY . /app/
WORKDIR /app

# Ejecutar sin privilegios, no como root.
USER nobody

# Por omisión, web.py usa el puerto 8080.
EXPOSE 8080

ENTRYPOINT ["python", "notasweb.py"]
