# -*- docker-image-name: "fiuba/notas" -*-

FROM debian:8

# Dependencias.
RUN apt-get update && apt-get upgrade -y    && \
    apt-get install -y --no-install-recommends \
        python3-pip             \
        python3-flask           \
        python3-flaskext.wtf    \
        python3-oauth2client    \
        uwsgi-plugin-python3 && \
    pip3 install gspread==0.2.5 webargs==1.2.0

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
