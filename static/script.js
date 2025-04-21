const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let painting = false;

// Estado del juego
let numeroObjetivo = "";
let posicionActual = 0;
let resultadoFinal = "";

// Inicializar canvas con fondo blanco
function inicializarCanvas() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
}
inicializarCanvas();

// Eventos de mouse para dibujar
canvas.addEventListener("mousedown", (e) => {
    painting = true;
    ctx.beginPath();
});

canvas.addEventListener("mouseup", () => {
    painting = false;
    ctx.beginPath();
});

canvas.addEventListener("mouseout", () => {
    painting = false;
    ctx.beginPath();
});

canvas.addEventListener("mousemove", dibujar);

// Dibujo libre
function dibujar(e) {
    if (!painting) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    ctx.lineWidth = 30;
    ctx.lineCap = "round";
    ctx.strokeStyle = "black";
    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Limpiar el canvas
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    inicializarCanvas();
    document.getElementById("resultado").innerText = "Resultado: ";
}

// Generar un número aleatorio de 4 cifras
function generarNumeroObjetivo() {
    numeroObjetivo = "";
    for (let i = 0; i < 4; i++) {
        numeroObjetivo += Math.floor(Math.random() * 10);
    }
    posicionActual = 0;
    resultadoFinal = "";
    document.getElementById("objetivo").innerText = numeroObjetivo;
    document.getElementById("avance").innerText = "0";
    document.getElementById("resultado").innerText = "Resultado: ";
    clearCanvas();
}

// Enviar la imagen al backend
function enviarImagen() {
    if (!numeroObjetivo) {
        alert("Primero debes generar un número objetivo.");
        return;
    }

    if (posicionActual >= 4) {
        alert("Ya completaste los 4 dígitos. Genera uno nuevo.");
        return;
    }

    const dataURL = canvas.toDataURL("image/png", 1.0);
    fetch("/predecir", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ imagen: dataURL })
    })
    .then(response => response.json())
    .then(data => {
        const predicho = data.prediccion;
        resultadoFinal += predicho;

        posicionActual++;
        document.getElementById("avance").innerText = posicionActual;
        clearCanvas();

        if (posicionActual === 4) {
            const correcto = resultadoFinal === numeroObjetivo;
            document.getElementById("resultado").innerText = correcto
                ? `✅ Correcto: ${resultadoFinal}`
                : `❌ Incorrecto. Dibujaste: ${resultadoFinal}`;
        }
    })
    .catch(error => {
        alert("❌ Error al predecir el número.");
        console.error("Error:", error);
    });
}
