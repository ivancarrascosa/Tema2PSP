import multiprocessing

SENAL_FIN = None


def leerNumeros(fichero, conexion_envio):
    """Lee pares de números de un fichero y los envía por la tubería."""
    with open(fichero, 'r') as f:
        for linea in f:
            partes = linea.strip().split()
            if len(partes) == 2:
                num1, num2 = int(partes[0]), int(partes[1])
                conexion_envio.send((num1, num2))
    conexion_envio.send(SENAL_FIN)
    conexion_envio.close()


def sumarNumeros(conexion_recepcion, conexion_resultados):
    """Recibe pares de números de la tubería y calcula la suma del rango."""
    datos = conexion_recepcion.recv()
    while datos is not SENAL_FIN:
        num1, num2 = datos
        inicio, fin = min(num1, num2), max(num1, num2)
        suma = sum(range(inicio, fin + 1))
        conexion_resultados.send(f"Rango ({num1}, {num2}): La suma total es {suma}")
        datos = conexion_recepcion.recv()
    conexion_recepcion.close()
    conexion_resultados.send(SENAL_FIN)
    conexion_resultados.close()


if __name__ == '__main__':
    recepcion_numeros, envio_numeros = multiprocessing.Pipe(duplex=False)
    recepcion_resultados, envio_resultados = multiprocessing.Pipe(duplex=False)

    proceso_lector = multiprocessing.Process(target=leerNumeros, args=('Parte1/numeros.txt', envio_numeros))
    proceso_sumador = multiprocessing.Process(target=sumarNumeros, args=(recepcion_numeros, envio_resultados))

    proceso_lector.start()
    proceso_sumador.start()

    proceso_lector.join()
    proceso_sumador.join()

    resultado = recepcion_resultados.recv()
    while resultado is not SENAL_FIN:
        print(resultado)
        resultado = recepcion_resultados.recv()
