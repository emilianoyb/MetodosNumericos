from flask import Blueprint, render_template, request, jsonify

from .nucleo import resolver_gauss_jordan

gauss_jordan_bp = Blueprint(
    'gauss_jordan',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@gauss_jordan_bp.route('/')
def index():
    return render_template('gauss_jordan/index.html')


@gauss_jordan_bp.route('/resolver', methods=['POST'])
def resolver():
    """
    Recibe un JSON con la matriz aumentada y devuelve la solución
    junto con los pasos del proceso. Se usa vía fetch() desde el JS
    del frontend, así la página nunca se recarga.
    """
    datos = request.get_json(silent=True)

    if not datos or "matriz" not in datos:
        return jsonify({"error": "No se recibió una matriz válida."}), 400

    matriz_cruda = datos["matriz"]

    # Validar y convertir todo a float
    try:
        matriz = [[float(val) for val in fila] for fila in matriz_cruda]
    except (ValueError, TypeError):
        return jsonify({"error": "Todas las celdas deben contener números válidos."}), 400

    if len(matriz) == 0 or any(len(fila) != len(matriz) + 1 for fila in matriz):
        return jsonify({"error": "La matriz aumentada no tiene el tamaño correcto (n x n+1)."}), 400

    resultado = resolver_gauss_jordan(matriz)
    return jsonify(resultado)
