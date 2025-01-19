#imagen original con alpine es version ligera
FROM python:3.9.6-alpine
#set work directory,directorio
# de trabajo,crearemos carpeta app
WORKDIR /usr/src/app
#configurar variables entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps \
    mariadb-dev \
    gcc \
    musl-dev \
    && pip install mysqlclient==1.4.2.post1 \
    && apk del .build-deps \
    && apk add libffi-dev openssl-dev libgcc

#instalar dependencias recordar que
# en requirements.txt estan las dependencias
#al ponerlo . al final de .txt es que copiara
#el requirements a /app
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#copiamos todo el proyecto con COPY
COPY . .
#esto es para levantar python
#CMD python manage.py runserver
#y abrirlo en el puerto 8000 que localmente se abria 
#en este puerto
#EXPOSE 8000