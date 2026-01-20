import multiprocessing


def sumarNumeros(rango):
    num1, num2 = rango
    suma = 0
    if num1 >= num2:
        for i in range(num2, num1 + 1):
            suma += i
    else:
        for i in range(num1, num2 + 1):
            suma += i
    return f"Rango ({num1}, {num2}): La suma total es {suma}"


if __name__ == '__main__':
    numeros = [(1, 5), (1, 9), (4, 5), (8, 2), (10, 5), (1, 5)]

    with multiprocessing.Pool(processes=4) as pool:
        resultados = pool.map(sumarNumeros, numeros)

    for resultado in resultados:
        print(resultado)
