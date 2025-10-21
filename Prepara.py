# crear_bd.py
import sqlite3

# Conexión (crea el archivo si no existe)
conn = sqlite3.connect("invitados.db")
cursor = conn.cursor()

# Crear tabla de invitados
cursor.execute("""
CREATE TABLE IF NOT EXISTS invitados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    telefono TEXT,
    correo TEXT,
    asistira TEXT CHECK(asistira IN ('Sí', 'No', 'No ha confirmado')) DEFAULT 'No ha confirmado',
    acompanantes INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Base de datos 'invitados.db' creada correctamente 🎉")