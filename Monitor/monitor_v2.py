import psutil
import sys


def imprimir_ayuda():
    print('Este es un script para monitorizar servicio.')
    print('Nota: Hay que tener instalado la paqueteria de psutil')
    print('Ejemplo uso:')
    print('\t\t./monitor.py PARAMETROS')
    print('Parametros:')
    print('\t-c : Se obtiene valor de uso de cpu')
    print('\t-d : Se obtiene valor de uso de disco')
    print('\t-m : Se obtiene valor de uso de memoria')


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


if __name__ == "__main__":
    # JBarradas (23-04-2020): Creó función main.
    # Se declaran variables
    opciones = []
    try:
        # JBarradas Se almacenan todas los parametros ingresados por el usuario
        opciones = sys.argv[1:]
        if (opciones):  # JBarradas: Si el usuario ingreso opciones...
            # JBarradas:... Se valida que las opciones correspondientes se encuentren
            # dentro de las opciones correspondientes, para agregar más agregarlas aquí
            # y a función imprimir_ayuda()

            if ('-c' in opciones):
                print('Uso CPU: %s' % dar_uso_cpu())
            if ('-d' in opciones):
                print('Uso Disco: %s' % dar_uso_disco())
            if ('-m' in opciones):
                print('Uso Memoria: %s' % dar_uso_memoria())
        else:  # JBarradas: El usuario no ingreso opciones
            imprimir_ayuda()
    except Exception as msj_error:
        print(msj_error)
