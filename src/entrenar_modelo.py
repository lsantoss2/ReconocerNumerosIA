import tensorflow as tf
import os

# Obtener ruta absoluta del proyecto (carpeta raíz)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUTA_MODELO = os.path.join(BASE_DIR, "modelo", "modelo_digitos.h5")

# Crear carpeta "modelo" si no existe
os.makedirs(os.path.dirname(RUTA_MODELO), exist_ok=True)

# 1. Cargar dataset MNIST
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 2. Normalizar imágenes (0 a 1)
x_train = x_train / 255.0
x_test = x_test / 255.0

# 3. Redefinir forma para CNN (agregar canal)
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

# 4. Crear modelo CNN
modelo = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(10, activation='softmax')
])

# 5. Compilar modelo
modelo.compile(optimizer='adam',
               loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])

# 6. Entrenar
modelo.fit(x_train, y_train, epochs=10, validation_split=0.1)

# 7. Evaluar
loss, acc = modelo.evaluate(x_test, y_test)
print(f"\n✅ Precisión del modelo en prueba: {acc * 100:.2f}%")

# 8. Guardar modelo
modelo.save(RUTA_MODELO)
print(f"✅ Modelo guardado en: {RUTA_MODELO}")
