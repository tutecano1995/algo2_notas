# -*- docker-image-name: "fiuba/notas" -*-

FROM debian:8

# Dependencias.
RUN apt-get update && apt-get upgrade -y    && \
    apt-get install -y --no-install-recommends \
        python-pip             \
        python-webpy           \
        python-oauth2client    \
        uwsgi-plugin-python && \
    pip install gspread==0.2.5

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
