"""
Método de la Regla Falsa (Falsa Posición) para encontrar raíces de f(x) = 0.

Este módulo es Python puro: no depende de Flask. Se encarga de:
  1) convertir el texto que escribe el usuario (ej. "x**3 - x - 2") en una
     función evaluable, usando sympy para el parseo (evita usar eval crudo
     sobre lo que escribe el usuario), y
  2) ejecutar el algoritmo de la regla falsa devolviendo la raíz y el
     detalle de cada iteración.
"""
import math

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

# Permite notación "de calculadora": 8x^2 en vez de 8*x**2, 2sin(x) en vez de 2*sin(x), etc.
TRANSFORMACIONES = standard_transformations + (implicit_multiplication_application, convert_xor)


class ErrorReglaFalsa(Exception):
    """Error controlado del método (entrada inválida, intervalo malo, etc.)."""


def construir_funcion(expresion_str):
    """
    Convierte una cadena como 'x**3 - x - 2', '8x^2 + 3x + 2' o 'sin(x) - x/2'
    en una función f(x) evaluable numéricamente. Acepta tanto notación de
    Python (**, *) como notación de calculadora (^, multiplicación implícita).

    Retorna (f, expresion_sympy).
    """
    x = sp.symbols('x')

    if expresion_str.count('(') != expresion_str.count(')'):
        raise ErrorReglaFalsa(
            f"Los paréntesis en «{expresion_str}» no están balanceados: "
            "revisa que cada '(' tenga su ')'."
        )

    try:
        expresion = parse_expr(expresion_str, transformations=TRANSFORMACIONES)
    except Exception as exc:
        raise ErrorReglaFalsa(
            f"No se pudo interpretar «{expresion_str}» como una función de x. "
            "Ejemplos válidos: x**3 - x - 2 , 8x^2 + 3x + 2 , sin(x) - x/2"
        ) from exc

    variables_libres = expresion.free_symbols
    if variables_libres - {x}:
        raise ErrorReglaFalsa(
            "La función solo puede depender de la variable x "
            f"(se encontró también: {', '.join(str(v) for v in variables_libres - {x})})."
        )

    f = sp.lambdify(x, expresion, modules=['math'])

    try:
        f(0.0)
    except Exception:
        pass  # 0.0 puede estar fuera del dominio (ej. log(x)); no es un error real

    return f, expresion


def regla_falsa(f, a, b, tol=1e-6, max_iter=100):
    """
    Ejecuta el método de la Regla Falsa en el intervalo [a, b].

    Retorna (raiz, iteraciones, mensaje):
      - raiz: mejor aproximación encontrada
      - iteraciones: lista de dicts con i, a, b, xr, f(xr), error, error_rel
      - mensaje: texto explicando por qué se detuvo el método
    """
    try:
        fa = f(a)
        fb = f(b)
    except Exception as exc:
        raise ErrorReglaFalsa(f"No se pudo evaluar f(x) en los extremos del intervalo: {exc}")

    if not (math.isfinite(fa) and math.isfinite(fb)):
        raise ErrorReglaFalsa("f(a) o f(b) no es un número finito; revisa el intervalo.")

    if fa == 0:
        return a, [], f"a = {a} ya es raíz exacta: f(a) = 0."
    if fb == 0:
        return b, [], f"b = {b} ya es raíz exacta: f(b) = 0."

    if fa * fb > 0:
        raise ErrorReglaFalsa(
            "f(a) y f(b) deben tener signos opuestos para asegurar una raíz en el "
            f"intervalo [{a}, {b}]. Aquí f(a) = {fa:.6g} y f(b) = {fb:.6g}, mismo signo."
        )

    iteraciones = []
    xr_anterior = None
    xr = a

    for i in range(1, max_iter + 1):
        denominador = fa - fb
        if denominador == 0:
            raise ErrorReglaFalsa(
                f"f(a) y f(b) resultaron iguales en la iteración {i}; "
                "el método no puede seguir dividiendo por cero con esta función/intervalo."
            )

        xr = b - fb * (a - b) / denominador

        try:
            fxr = f(xr)
        except Exception as exc:
            raise ErrorReglaFalsa(
                f"No se pudo evaluar f(x) en x = {xr:.6g} (iteración {i}): {exc}"
            )

        if not math.isfinite(fxr):
            raise ErrorReglaFalsa(
                f"f(x) dejó de ser un número finito en x = {xr:.6g} (iteración {i}); "
                "prueba con otro intervalo o revisa el dominio de la función."
            )

        error = abs(xr - xr_anterior) if xr_anterior is not None else None
        error_rel = (abs(error / xr) * 100) if (error is not None and xr != 0) else None

        iteraciones.append({
            'i': i, 'a': a, 'b': b, 'fa': fa, 'fb': fb,
            'xr': xr, 'fxr': fxr, 'error': error, 'error_rel': error_rel,
        })

        if fxr == 0:
            return xr, iteraciones, f"Raíz exacta encontrada en la iteración {i}."

        if error is not None and error < tol:
            return xr, iteraciones, (
                f"Convergencia alcanzada en la iteración {i} "
                f"(|Δx| = {error:.2e} < tol = {tol:.2e})."
            )

        if fa * fxr < 0:
            b, fb = xr, fxr
        else:
            a, fa = xr, fxr

        xr_anterior = xr

    return xr, iteraciones, (
        f"Se llegó al máximo de {max_iter} iteraciones sin bajar de la tolerancia pedida."
    )
