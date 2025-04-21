import os
from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import io
import re
import base64
from tensorflow.keras.models import load_model

# Ruta base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Configuración Flask
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# Cargar modelo
try:
    modelo = load_model(os.path.join(BASE_DIR, "modelo", "modelo_digitos.h5"))
    print("✅ Modelo cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predecir", methods=["POST"])
def predecir():
    try:
        data = request.get_json()
        imagen_base64 = data["imagen"]
        imagen_base64 = re.sub("^data:image/.+;base64,", "", imagen_base64)
        imagen_bytes = base64.b64decode(imagen_base64)

        # Convertir a imagen PIL
        imagen = Image.open(io.BytesIO(imagen_bytes)).convert("L")
        imagen = imagen.resize((280, 280))  # Tamaño del canvas original

        # Convertir a array e invertir colores
        imagen_array = 255 - np.array(imagen)

        # Binarizar
        binaria = (imagen_array > 10).astype(np.uint8) * 255

        # Encontrar límites del trazo
        coords = np.argwhere(binaria > 0)
        if coords.size == 0:
            return jsonify({"prediccion": "Nada dibujado"})

        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0)

        # Recortar
        recorte = imagen_array[y0:y1 + 1, x0:x1 + 1]

        # Centrar en lienzo cuadrado
        alto, ancho = recorte.shape
        lado = max(alto, ancho)
        canvas = np.zeros((lado, lado), dtype=np.uint8)
        y_offset = (lado - alto) // 2
        x_offset = (lado - ancho) // 2
        canvas[y_offset:y_offset + alto, x_offset:x_offset + ancho] = recorte

        # Redimensionar a 28x28
        final = Image.fromarray(canvas).resize((28, 28))

        # (Opcional) Guardar imagen procesada para depuración
        final.save(os.path.join(BASE_DIR, "ver_dibujo.png"))

        # Preparar imagen para el modelo
        entrada = np.array(final) / 255.0
        entrada = entrada.reshape(1, 28, 28)

        # Predecir
        prediccion = modelo.predict(entrada)
        resultado = int(np.argmax(prediccion))

        return jsonify({"prediccion": resultado})
    
    except Exception as e:
        print(f"🔥 Error en /predecir: {e}")
        return jsonify({"error": "Error interno al predecir"}), 500

if __name__ == "__main__":
    app.run(debug=True)
