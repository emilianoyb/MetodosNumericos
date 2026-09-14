# Métodos Numéricos — proyecto combinado

Une dos apps Flask independientes en una sola, cada una como un
[Blueprint](https://flask.palletsprojects.com/en/latest/blueprints/) que
conserva su propio código, plantillas y estáticos:

```
proyecto_combinado/
├── app.py                      # crea la app, registra los blueprints y sirve el menú
├── templates/
│   └── menu.html                # pantalla de selección
├── regla_falsa/                 # Blueprint 1: Regla Falsa (búsqueda de raíces)
│   ├── __init__.py               # rutas (antes app.py)
│   ├── metodos.py
│   ├── graficos.py
│   ├── templates/regla_falsa/index.html
│   └── static/
└── gauss_jordan/                # Blueprint 2: Gauss-Jordan (sistemas de ecuaciones)
    ├── __init__.py               # rutas (antes app.py)
    ├── nucleo.py                  # antes gauss_jordan.py
    ├── templates/gauss_jordan/index.html
    └── static/
```

## Rutas

| Ruta                    | Qué hace                                   |
|--------------------------|---------------------------------------------|
| `/`                      | Menú para elegir entre los dos proyectos    |
| `/regla-falsa/`          | Calculadora de raíces por Regla Falsa       |
| `/gauss-jordan/`         | Resolutor de sistemas por Gauss-Jordan      |
| `/gauss-jordan/resolver` | Endpoint JSON usado por el JS del front     |

Cada proyecto conserva sus propios `static/` y `templates/` sin chocar
entre sí (Flask los aísla por blueprint), así que **ambos pueden seguir
creciendo por separado** sin pisarse archivos.

## Ejecutar

```bash
pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000/` y elige el proyecto desde el menú. Cada
página interna tiene un enlace "← Menú de proyectos" para volver.
