# app.py
import streamlit as st
import pandas as pd
import os

# ==============================
# Verificación de dependencias
# ==============================
try:
    import openpyxl
except ImportError:
    st.error("El paquete 'openpyxl' no está instalado. Instálalo con 'pip install openpyxl' antes de ejecutar la app.")
    st.stop()

# ==============================
# Configuración inicial
# ==============================
st.set_page_config(
    page_title="Resultados test de Movilidad",
    layout="wide"
)

st.title("Resultados test de Movilidad")

# ==============================
# Ruta del archivo Excel
# ==============================
# Detecta automáticamente si está en local o en Streamlit Cloud
local_path = r"C:\Users\Daniel\Desktop\score_tscore\PRUEBAS MOVILIDAD.xlsx"
repo_path = "PRUEBAS MOVILIDAD.xlsx"

if os.path.exists(local_path):
    EXCEL_FILE = local_path
elif os.path.exists(repo_path):
    EXCEL_FILE = repo_path
else:
    st.error("❌ No se encontró el archivo 'PRUEBAS MOVILIDAD.xlsx'.")
    st.stop()

# ==============================
# Función para cargar datos
# ==============================
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel(EXCEL_FILE)
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        return pd.DataFrame()

df = cargar_datos()

# ==============================
# Botón de refrescar
# ==============================
if st.button("🔄 Refrescar datos"):
    df = cargar_datos()

if df.empty:
    st.stop()

# ==============================
# Columnas prioritarias de identificación
# ==============================
id_cols_prioritarias = ["JUGADOR", "ID", "NOMBRE", "APELLIDO",
                        "NOMBRE_COMPLETO", "NOMBRE Y APELLIDO", "NOMBRE_APELLIDO"]
id_cols = [col for col in id_cols_prioritarias if col in df.columns]

# ==============================
# Filtro dinámico por CATEGORÍA
# ==============================
if "CATEGORÍA" in df.columns:
    categorias = ["Todas"] + sorted(df["CATEGORÍA"].dropna().astype(str).unique())
    seleccion_categoria = st.selectbox("Filtrar por CATEGORÍA", categorias)
    if seleccion_categoria != "Todas":
        df = df[df["CATEGORÍA"].astype(str) == seleccion_categoria]

# ==============================
# Columnas a transformar en emojis
# ==============================
umbral_cols = {
    "THOMAS PSOAS (D)": 10,
    "THOMAS PSOAS (I)": 10,
    "THOMAS CUADRICEPS (D)": 50,
    "THOMAS CUADRICEPS (I)": 50,
    "THOMAS SARTORIO (D)": 80,
    "THOMAS SARTORIO (I)": 80,
    "JURDAN (D)": 75,
    "JURDAN (I)": 75
}

cols_emoji = [col for col in umbral_cols.keys() if col in df.columns]

# ==============================
# Función para asignar emojis
# ==============================
def asignar_emoji_html(valor, umbral):
    if pd.isna(valor):
        return ""
    try:
        if float(valor) >= umbral:
            return "<div style='color:green; font-size:32px; text-align:center;'>👍</div>"
        else:
            return "<div style='color:red; font-size:32px; text-align:center;'>👎</div>"
    except:
        return ""

# ====

