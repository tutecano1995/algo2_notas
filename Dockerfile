# -*- docker-image-name: "fiuba/notas" -*-

FROM debian:8

# Dependencias.
RUN apt-get update && env DEBIAN_FRONTEND=noninteractive \
    apt-get install --assume-yes --no-install-recommends \
        python-webpy        \
        python-gdata        \
        python-oauth2client \
        uwsgi-plugin-python

# Copiar la applicación (menos los ficheros en .dockerignore).
COPY . /app/
WORKDIR /app

# Ejecutar sin privilegios, no como root.
USER nobody

# Por omisión, usamos el puerto 3031 para el socket de uWSGI. Para realizar
# pruebas por HTTP se puede pasar `--http-socket :8080` al ejecutar el
# container.
EXPOSE 3031

ENTRYPOINT ["uwsgi", "notas.ini"]
