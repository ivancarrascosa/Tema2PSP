import multiprocessing


def sumarNumeros(num1, num2):
    suma = 0
    if (num1 >= num2):
        for i in range(num2, num1 + 1):
            suma += i
    else:
        for i in range(num1, num2 + 1):
            suma += i
    print (f"La suma total es {suma}")


if __name__ == '__main__':
    numeros = [(1,5),(1,9),(4,5),(8,2),(10,5),(1,5)]
    procesos = []
    for i in numeros:
        p = multiprocessing.Process(target=sumarNumeros, args=i)
        procesos.append(p)
    
    # Iniciar todos
    for p in procesos:
        p.start()
    
    # Esperar a todos
    for p in procesos:
        p.join()

        