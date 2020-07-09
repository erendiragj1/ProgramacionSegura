FROM python:3.8

RUN mkdir /dependencias
COPY requirements.txt /dependencias
RUN pip install -r /dependencias/requirements.txt

ENV SECRET_KEY=""
ENV DB_NAME=""
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DB_HOST=""
ENV DB_PORT=3306

RUN mkdir '/codigo'
COPY inicioProyecto.sh '/codigo'
RUN chmod 755  '/codigo/inicioProyecto.sh'
WORKDIR /codigo
CMD /bin/bash -c 'inicioProyecto.sh'


