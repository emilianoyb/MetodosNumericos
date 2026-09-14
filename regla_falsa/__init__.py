from flask import Blueprint, render_template, request

from .graficos import construir_grafico_convergencia, construir_grafico_funcion
from .metodos import ErrorReglaFalsa, construir_funcion, regla_falsa

regla_falsa_bp = Blueprint(
    'regla_falsa',
    __name__,
    template_folder='templates',
    static_folder='static',
)

VALORES_POR_DEFECTO = {
    'funcion': 'x**3 - x - 2',
    'a': '1',
    'b': '2',
    'tolerancia': '0.0001',
    'max_iter': '50',
}


@regla_falsa_bp.app_template_filter('fmt')
def formatear_numero(valor, decimales=6):
    """Filtro de Jinja para mostrar floats con formato fijo, o un guion si es None."""
    if valor is None:
        return "—"
    try:
        return f"{valor:.{decimales}f}"
    except (TypeError, ValueError):
        return str(valor)


@regla_falsa_bp.route('/', methods=['GET', 'POST'])
def index():
    contexto = {
        'valores': VALORES_POR_DEFECTO.copy(),
        'resultado': None,
        'error': None,
    }

    if request.method == 'POST':
        valores = {campo: request.form.get(campo, '').strip() for campo in VALORES_POR_DEFECTO}
        contexto['valores'] = valores

        try:
            if not valores['funcion']:
                raise ErrorReglaFalsa("Escribe una función f(x).")

            try:
                a = float(valores['a'])
                b = float(valores['b'])
                tol = float(valores['tolerancia'])
                max_iter = int(valores['max_iter'])
            except ValueError as exc:
                raise ErrorReglaFalsa(
                    "Revisa que a, b, la tolerancia y las iteraciones sean números válidos."
                ) from exc

            if a >= b:
                raise ErrorReglaFalsa("El extremo a debe ser menor que b.")
            if tol <= 0:
                raise ErrorReglaFalsa("La tolerancia debe ser un número positivo.")
            if not (1 <= max_iter <= 1000):
                raise ErrorReglaFalsa("Usa un número de iteraciones entre 1 y 1000.")

            f, expresion = construir_funcion(valores['funcion'])
            raiz, iteraciones, mensaje = regla_falsa(f, a, b, tol, max_iter)

            contexto['resultado'] = {
                'expresion': str(expresion),
                'raiz': raiz,
                'valor_f_raiz': f(raiz),
                'iteraciones': iteraciones,
                'mensaje': mensaje,
                'grafico': construir_grafico_convergencia(iteraciones),
                'grafico_funcion': construir_grafico_funcion(f, a, b, raiz),
                'a_inicial': a,
                'b_inicial': b,
            }

        except ErrorReglaFalsa as exc:
            contexto['error'] = str(exc)

    return render_template('regla_falsa/index.html', **contexto)
