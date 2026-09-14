"""
Módulo que implementa el método de Gauss-Jordan para resolver
sistemas de ecuaciones lineales de n incógnitas.

"""


def resolver_gauss_jordan(matriz):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Jordan.

    Parámetros:
        matriz: lista de listas (matriz aumentada). Cada fila tiene
                los coeficientes seguidos del término independiente.

    Retorna un dict con:
        'solucion' : lista con los valores de las incógnitas (o None)
        'error'    : mensaje de error, o None si no hubo error
    """
    # Copiamos la matriz para no modificar la que nos pasaron
    m = [fila[:] for fila in matriz]
    n = len(m)

    # d = índice de la diagonal
    for d in range(n):

        # --- Pivoteo parcial: buscamos la fila con mayor valor absoluto
        #     en la columna d, entre la fila d y las de abajo ---
        max_fila = max(range(d, n), key=lambda r: abs(m[r][d]))

        # Si incluso el valor más grande es (prácticamente) cero,
        # no hay forma de resolver el sistema de manera única.
        if abs(m[max_fila][d]) < 1e-12:
            return {
                'solucion': None,
                'error': 'El sistema no tiene solución única '
                         '(se encontró un pivote igual a cero; '
                         'puede no tener solución o tener infinitas soluciones).'
            }

        if max_fila != d:
            m[d], m[max_fila] = m[max_fila], m[d]

        # --- Normalizar la fila pivote ---
        pivote = m[d][d]
        m[d] = [x / pivote for x in m[d]]

        # --- Eliminar las demás filas ---
        for i in range(n):
            if i != d:
                factor = m[i][d]
                for x in range(n + 1):
                    m[i][x] = m[i][x] - factor * m[d][x]

    # r de resultados 
    solucion = [m[r][n] for r in range(n)]

    return {
        'solucion': solucion,
        'error': None
    }

