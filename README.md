Pequeño sitio web que permite que los alumnos puedan consultar sus notas.

Los datos se obtienen de un google spreadsheet. El alumno especifica su padrón y e-mail, y si la dirección está asociada a ese padrón en el doc, se le envía un mail con un link exclusivo para que pueda consultar sus notas.

**Requerimientos:** webpy, gdata

Configuración y ejecución
-------------------------

Crear un archivo llamado `env`:

```bash
export NOTAS_TITLE="Notas de Algoritmos I"
export NOTAS_ACCOUNT='xxxx@gmail.com'
export NOTAS_PASSWORD='****'
export NOTAS_SPREADSHEET_KEY='*****'
export NOTAS_SECRET='*****'
```

Ejecutar el servidor web:

```bash
$ . ./env
$ python notasweb.py
```

Alternativamente, mediante contenedores de [Docker][], completar las credenciales en el archivo `docker.auth`, y ejecutar:

```bash
$ docker build -t fiuba/notas .
$ docker run --env-file docker.auth -p 8080:8080 --name notas.run fiuba/notas
```

  [docker]: https://www.docker.com
