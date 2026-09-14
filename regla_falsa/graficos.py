"""
Genera las coordenadas de un pequeño gráfico SVG (error vs. iteración,
escala logarítmica en el error) a partir del resultado de regla_falsa().
No depende de Flask ni de librerías de gráficos externas.
"""
import math


def construir_grafico_convergencia(iteraciones, ancho=560, alto=190, pad=36):
    puntos = [(it['i'], it['error']) for it in iteraciones if it['error'] and it['error'] > 0]
    if len(puntos) < 2:
        return None

    xs = [p[0] for p in puntos]
    ys = [math.log10(p[1]) for p in puntos]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    if y_max == y_min:
        y_max += 1

    def esc_x(x):
        if x_max == x_min:
            return pad
        return pad + (x - x_min) / (x_max - x_min) * (ancho - 2 * pad)

    def esc_y(y):
        return pad + (y_max - y) / (y_max - y_min) * (alto - 2 * pad)

    coords = [(esc_x(x), esc_y(y)) for x, y in zip(xs, ys)]
    polyline = " ".join(f"{px:.1f},{py:.1f}" for px, py in coords)

    return {
        'ancho': ancho,
        'alto': alto,
        'pad': pad,
        'polyline': polyline,
        'puntos': list(zip(coords, [p[0] for p in puntos], [p[1] for p in puntos])),
        'y_min_label': f"{10 ** y_min:.1e}",
        'y_max_label': f"{10 ** y_max:.1e}",
        'x_min_label': x_min,
        'x_max_label': x_max,
    }


def construir_grafico_funcion(f, a, b, raiz, ancho=560, alto=230, pad=40, num_puntos=240):
    """
    Evalúa f(x) en muchos puntos alrededor de [a, b] y arma las coordenadas
    SVG para dibujar la curva real, la cuerda inicial (a, f(a))-(b, f(b))
    y la raíz encontrada. Si f(x) no está definida en algún tramo (dominio
    restringido), la curva se corta en varios segmentos en vez de romperse.
    """
    margen = (b - a) * 0.18 if b > a else 1.0
    x_ini = a - margen
    x_fin = b + margen
    paso = (x_fin - x_ini) / (num_puntos - 1)

    segmentos = []
    actual = []
    ys_validos = []

    for i in range(num_puntos):
        x = x_ini + i * paso
        try:
            y = f(x)
            if not math.isfinite(y):
                raise ValueError
        except Exception:
            if len(actual) >= 2:
                segmentos.append(actual)
            actual = []
            continue
        actual.append((x, y))
        ys_validos.append(y)
    if len(actual) >= 2:
        segmentos.append(actual)

    if not ys_validos:
        return None

    try:
        fa, fb = f(a), f(b)
        if not (math.isfinite(fa) and math.isfinite(fb)):
            fa = fb = None
    except Exception:
        fa = fb = None

    y_min, y_max = min(ys_validos), max(ys_validos)
    y_min, y_max = min(y_min, 0), max(y_max, 0)
    rango_y = y_max - y_min or 1.0
    y_min -= rango_y * 0.12
    y_max += rango_y * 0.12

    def esc_x(x):
        return pad + (x - x_ini) / (x_fin - x_ini) * (ancho - 2 * pad)

    def esc_y(y):
        return pad + (y_max - y) / (y_max - y_min) * (alto - 2 * pad)

    polilineas = [
        " ".join(f"{esc_x(x):.1f},{esc_y(y):.1f}" for x, y in seg)
        for seg in segmentos
    ]

    try:
        y_raiz = f(raiz)
        y_raiz = y_raiz if math.isfinite(y_raiz) else 0.0
    except Exception:
        y_raiz = 0.0

    cuerda = None
    if fa is not None and fb is not None:
        cuerda = (esc_x(a), esc_y(fa), esc_x(b), esc_y(fb))

    return {
        'ancho': ancho,
        'alto': alto,
        'pad': pad,
        'polilineas': polilineas,
        'y_cero': esc_y(0),
        'cuerda': cuerda,
        'punto_a': (esc_x(a), esc_y(fa)) if fa is not None else None,
        'punto_b': (esc_x(b), esc_y(fb)) if fb is not None else None,
        'punto_raiz': (esc_x(raiz), esc_y(y_raiz)),
        'x_min_label': f"{x_ini:.4g}",
        'x_max_label': f"{x_fin:.4g}",
        'y_min_label': f"{y_min:.3g}",
        'y_max_label': f"{y_max:.3g}",
    }
