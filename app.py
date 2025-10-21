# app_invitados.py
import streamlit as st
import sqlite3
import pandas as pd

# --- Configuración ---
st.set_page_config(page_title="Gestión de Invitados", page_icon="🎉", layout="wide")

# --- Conexión a la base de datos ---
def conectar():
    return sqlite3.connect("invitados.db")

# --- Funciones CRUD ---
def agregar_invitado(nombre, apellidos, telefono, correo, asistira, acompanantes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO invitados (nombre, apellidos, telefono, correo, asistira, acompanantes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, apellidos, telefono, correo, asistira, acompanantes))
    conn.commit()
    conn.close()

def obtener_invitados():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM invitados", conn)
    conn.close()
    return df

def actualizar_invitado(id, nombre, apellidos, telefono, correo, asistira, acompanantes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE invitados
        SET nombre=?, apellidos=?, telefono=?, correo=?, asistira=?, acompanantes=?
        WHERE id=?
    """, (nombre, apellidos, telefono, correo, asistira, acompanantes, id))
    conn.commit()
    conn.close()

def eliminar_invitado(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM invitados WHERE id=?", (id,))
    conn.commit()
    conn.close()

# --- Interfaz ---
st.title("🎉 Gestor de Invitados - Aniversario")

menu = st.sidebar.radio("Menú", ["Agregar Invitado", "Ver/Editar Invitados"])

if menu == "Agregar Invitado":
    st.subheader("➕ Agregar nuevo invitado")

    with st.form("form_invitado"):
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo electrónico")
        asistira = st.selectbox("¿Asistirá?", ["No ha confirmado", "Sí", "No"])
        acompanantes = st.number_input("Número de acompañantes", min_value=0, step=1)
        submitted = st.form_submit_button("Guardar")

        if submitted:
            if nombre and apellidos:
                agregar_invitado(nombre, apellidos, telefono, correo, asistira, acompanantes)
                st.success(f"✅ Invitado {nombre} {apellidos} agregado correctamente.")
            else:
                st.error("Por favor, ingresa al menos nombre y apellidos.")

elif menu == "Ver/Editar Invitados":
    st.subheader("📋 Lista de invitados")
    df = obtener_invitados()

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.markdown("---")

        st.subheader("✏️ Editar o eliminar invitado")
        ids = df["id"].tolist()
        id_seleccionado = st.selectbox("Selecciona un invitado por ID", ids)

        invitado = df[df["id"] == id_seleccionado].iloc[0]

        with st.form("editar_invitado"):
            nombre = st.text_input("Nombre", invitado["nombre"])
            apellidos = st.text_input("Apellidos", invitado["apellidos"])
            telefono = st.text_input("Teléfono", invitado["telefono"])
            correo = st.text_input("Correo", invitado["correo"])
            asistira = st.selectbox("¿Asistirá?", ["No ha confirmado", "Sí", "No"], index=["No ha confirmado", "Sí", "No"].index(invitado["asistira"]))
            acompanantes = st.number_input("Número de acompañantes", min_value=0, step=1, value=int(invitado["acompanantes"]))

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Actualizar"):
                    actualizar_invitado(id_seleccionado, nombre, apellidos, telefono, correo, asistira, acompanantes)
                    st.success("✅ Invitado actualizado correctamente.")
            with col2:
                if st.form_submit_button("🗑️ Eliminar"):
                    eliminar_invitado(id_seleccionado)
                    st.warning("⚠️ Invitado eliminado.")
    else:
        st.info("No hay invitados registrados aún.")
