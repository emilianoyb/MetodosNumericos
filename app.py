from flask import Flask, render_template

from regla_falsa import regla_falsa_bp
from gauss_jordan import gauss_jordan_bp

app = Flask(__name__)

app.register_blueprint(regla_falsa_bp, url_prefix='/regla-falsa')
app.register_blueprint(gauss_jordan_bp, url_prefix='/gauss-jordan')


@app.route('/')
def menu():
    return render_template('menu.html')


if __name__ == '__main__':
    app.run(debug=True)
