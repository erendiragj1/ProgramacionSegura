import psutil
import sys


def dar_uso_memoria():
    # Descrićión: Función que se encarga de regresar el uso en porcentaje de
    # el uso de memoria RAM.
    # JBarradas (23-04-2020): Generó función
    return dict(psutil.virtual_memory()._asdict())['percent']


def dar_uso_cpu():
    # Descrićión: Función que se encarga de regresar el uso en porcentaje de
    # la suma total de uso de los cpu.
    # JBarradas (23-04-2020): Generó función
    return psutil.cpu_percent(interval=1)


def dar_uso_disco():
    # Descrićión: Función que se encarga de regresar el uso en porcentaje de
    # espacio del disco principal del dispositivo.
    # JBarradas (23-04-2020): Generó función
    return psutil.disk_usage('/').percent

