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

RUN mkdir /codigo
RUN mkdir /start
RUN mkdir /codigo/bitacora

COPY ./inicioProyecto.sh /start
RUN useradd -s /bin/bash limitado
RUN chown -R limitado /codigo
RUN chown -R limitado /start
RUN chmod +x  /start/inicioProyecto.sh
USER limitado

WORKDIR /codigo
CMD /start/inicioProyecto.sh


