(function () {
    const inputN = document.getElementById("n");
    const btnMenos = document.getElementById("btn-menos");
    const btnMas = document.getElementById("btn-mas");
    const btnGenerar = document.getElementById("btn-generar");
    const btnEjemplo = document.getElementById("btn-ejemplo");
    const btnLimpiar = document.getElementById("btn-limpiar");
    const btnResolver = document.getElementById("btn-resolver");
    const contenedorMatriz = document.getElementById("matriz-inputs");
    const mensajeError = document.getElementById("mensaje-error");

    const panelResultado = document.getElementById("panel-resultado");
    const listaSolucion = document.getElementById("lista-solucion");

    const MIN_N = 2;
    const MAX_N = 9;

    // ---------- Construcción de la matriz de entrada ----------

    function construirMatriz(n, valores) {
        contenedorMatriz.innerHTML = "";
        contenedorMatriz.style.gridTemplateColumns = `repeat(${n}, 58px) 14px 58px`;

        for (let i = 0; i < n; i++) {
            for (let j = 0; j <= n; j++) {
                if (j === n) {
                    const sep = document.createElement("div");
                    sep.className = "celda-separador";
                    contenedorMatriz.appendChild(sep);
                }
                const input = document.createElement("input");
                input.type = "text";
                input.inputMode = "decimal";
                input.dataset.fila = i;
                input.dataset.col = j;
                input.placeholder = j < n ? `x${j + 1}` : `b${i + 1}`;
                if (j === n) input.classList.add("col-independiente");
                if (valores && valores[i] && valores[i][j] !== undefined) {
                    input.value = valores[i][j];
                }
                contenedorMatriz.appendChild(input);
            }
        }
    }

    function leerN() {
        let n = parseInt(inputN.value, 10);
        if (isNaN(n)) n = 3;
        n = Math.max(MIN_N, Math.min(MAX_N, n));
        inputN.value = n;
        return n;
    }

    function leerMatrizActual(n) {
        const matriz = [];
        for (let i = 0; i < n; i++) matriz.push(new Array(n + 1).fill(""));
        contenedorMatriz.querySelectorAll("input").forEach((inp) => {
            const i = parseInt(inp.dataset.fila, 10);
            const j = parseInt(inp.dataset.col, 10);
            matriz[i][j] = inp.value;
        });
        return matriz;
    }

    // ---------- Eventos de configuración ----------

    btnMenos.addEventListener("click", () => {
        inputN.value = Math.max(MIN_N, leerN() - 1);
        construirMatriz(leerN());
        ocultarResultado();
    });

    btnMas.addEventListener("click", () => {
        inputN.value = Math.min(MAX_N, leerN() + 1);
        construirMatriz(leerN());
        ocultarResultado();
    });

    btnGenerar.addEventListener("click", () => {
        construirMatriz(leerN());
        ocultarResultado();
        ocultarError();
    });

    btnLimpiar.addEventListener("click", () => {
        contenedorMatriz.querySelectorAll("input").forEach((inp) => (inp.value = ""));
        ocultarResultado();
        ocultarError();
    });

    btnEjemplo.addEventListener("click", () => {
        const ejemplo = [
            [2, 1, -1, 8],
            [-3, -1, 2, -11],
            [-2, 1, 2, -3],
        ];
        inputN.value = 3;
        construirMatriz(3, ejemplo);
        ocultarResultado();
        ocultarError();
    });

    // ---------- Resolver ----------

    btnResolver.addEventListener("click", async () => {
        ocultarError();
        const n = leerN();
        const matriz = leerMatrizActual(n);

        const vacias = matriz.some((fila) => fila.some((v) => v === "" || v === null));
        if (vacias) {
            mostrarError("Completa todas las celdas antes de resolver (usa 0 si aplica).");
            return;
        }

        btnResolver.disabled = true;
        btnResolver.textContent = "Resolviendo…";

        try {
            const resp = await fetch(window.RESOLVER_URL || "/resolver", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ matriz }),
            });
            const datos = await resp.json();

            if (!resp.ok) {
                mostrarError(datos.error || "Ocurrió un error al resolver el sistema.");
                return;
            }

            if (datos.error) {
                mostrarError(datos.error);
                return;
            }

            mostrarResultado(datos);
        } catch (e) {
            mostrarError("No se pudo conectar con el servidor. Intenta de nuevo.");
        } finally {
            btnResolver.disabled = false;
            btnResolver.textContent = "Resolver sistema";
        }
    });

    function mostrarError(texto) {
        mensajeError.textContent = texto;
        mensajeError.hidden = false;
    }
    function ocultarError() {
        mensajeError.hidden = true;
    }
    function ocultarResultado() {
        panelResultado.hidden = true;
    }

    // ---------- Resultado ----------

    function mostrarResultado(datos) {
        listaSolucion.innerHTML = "";
        if (datos.solucion) {
            datos.solucion.forEach((valor, idx) => {
                const li = document.createElement("li");
                li.textContent = `x${idx + 1} = ${formatearNumero(valor)}`;
                listaSolucion.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "Sin solución única";
            listaSolucion.appendChild(li);
        }

        panelResultado.hidden = false;
        panelResultado.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function formatearNumero(valor) {
        const redondeado = Math.round(valor * 10000) / 10000;
        return Object.is(redondeado, -0) ? "0" : redondeado.toString();
    }

    // ---------- Inicialización ----------
    construirMatriz(leerN());
})();