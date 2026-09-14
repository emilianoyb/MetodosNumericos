(function () {
  'use strict';

  // ---------- Teclado matemático ----------
  const input = document.getElementById('funcion');
  const teclado = document.getElementById('teclado');

  if (input && teclado) {
    // Evita que al hacer click en el teclado el input pierda el foco/cursor.
    teclado.addEventListener('mousedown', (e) => e.preventDefault());

    function posicionCursor() {
      const val = input.value;
      return {
        start: input.selectionStart ?? val.length,
        end: input.selectionEnd ?? val.length,
      };
    }

    function insertarTexto(texto) {
      const val = input.value;
      const { start, end } = posicionCursor();
      input.value = val.slice(0, start) + texto + val.slice(end);
      const nuevaPos = start + texto.length;
      input.focus();
      input.setSelectionRange(nuevaPos, nuevaPos);
    }

    function borrarUnCaracter() {
      const val = input.value;
      let { start, end } = posicionCursor();
      if (start === end && start > 0) start -= 1;
      input.value = val.slice(0, start) + val.slice(end);
      input.focus();
      input.setSelectionRange(start, start);
    }

    teclado.querySelectorAll('.tecla[data-insert]').forEach((boton) => {
      boton.addEventListener('click', () => insertarTexto(boton.dataset.insert));
    });

    const btnBorrar = document.getElementById('btn-borrar');
    const btnLimpiar = document.getElementById('btn-limpiar');
    if (btnBorrar) btnBorrar.addEventListener('click', borrarUnCaracter);
    if (btnLimpiar) btnLimpiar.addEventListener('click', () => {
      input.value = '';
      input.focus();
    });

    teclado.querySelectorAll('.tab-btn').forEach((tab) => {
      tab.addEventListener('click', () => {
        teclado.querySelectorAll('.tab-btn').forEach((t) => {
          t.classList.remove('activo');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('activo');
        tab.setAttribute('aria-selected', 'true');
        const nombre = tab.dataset.tab;
        teclado.querySelectorAll('.panel-teclas').forEach((panel) => {
          panel.classList.toggle('oculto', panel.dataset.panel !== nombre);
        });
      });
    });
  }

  // ---------- Chips de ejemplo ----------
  const campoA = document.getElementById('a');
  const campoB = document.getElementById('b');
  document.querySelectorAll('.chip-ejemplo').forEach((chip) => {
    chip.addEventListener('click', () => {
      if (input) input.value = chip.dataset.funcion;
      if (campoA && chip.dataset.a !== undefined) campoA.value = chip.dataset.a;
      if (campoB && chip.dataset.b !== undefined) campoB.value = chip.dataset.b;
      if (input) input.focus();
    });
  });

  // ---------- Estado de carga del botón ----------
  const form = document.querySelector('form.calculo');
  const btnCalcular = document.getElementById('btn-calcular');
  if (form && btnCalcular) {
    form.addEventListener('submit', () => {
      btnCalcular.setAttribute('disabled', 'true');
      btnCalcular.textContent = 'Calculando…';
    });
  }

  // ---------- Copiar raíz ----------
  const btnCopiar = document.getElementById('btn-copiar-raiz');
  const valorRaiz = document.getElementById('valor-raiz');
  if (btnCopiar && valorRaiz) {
    btnCopiar.addEventListener('click', async () => {
      const texto = valorRaiz.textContent.trim();
      try {
        await navigator.clipboard.writeText(texto);
      } catch (e) {
        const area = document.createElement('textarea');
        area.value = texto;
        document.body.appendChild(area);
        area.select();
        document.execCommand('copy');
        document.body.removeChild(area);
      }
      const original = btnCopiar.textContent;
      btnCopiar.textContent = 'Copiado ✓';
      btnCopiar.dataset.copiado = 'true';
      setTimeout(() => {
        btnCopiar.textContent = original;
        btnCopiar.dataset.copiado = 'false';
      }, 1800);
    });
  }

  // ---------- Tabla de iteraciones colapsable ----------
  const btnMostrarTodas = document.getElementById('btn-mostrar-todas');
  const cuerpoIteraciones = document.getElementById('cuerpo-iteraciones');
  if (btnMostrarTodas && cuerpoIteraciones) {
    let expandido = false;
    btnMostrarTodas.addEventListener('click', () => {
      expandido = !expandido;
      cuerpoIteraciones.querySelectorAll('tr.fila-oculta').forEach((fila) => {
        fila.style.display = expandido ? 'table-row' : 'none';
      });
      btnMostrarTodas.textContent = expandido
        ? btnMostrarTodas.dataset.menos
        : btnMostrarTodas.dataset.mas;
    });
  }

  // ---------- Enfoque tras enviar el formulario ----------
  window.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    if (body.dataset.tieneResultado === 'true') {
      const resultado = document.getElementById('resultado');
      if (resultado) {
        resultado.scrollIntoView({ behavior: 'smooth', block: 'start' });
        resultado.focus({ preventScroll: true });
      }
    } else {
      const aviso = document.getElementById('aviso-error');
      if (aviso) aviso.focus();
    }
  });
})();
