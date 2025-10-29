# app.py
import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

# ------------------------------
# Verificación de dependencias
# ------------------------------
try:
    import openpyxl  # solo para chequeo
except ImportError:
    st.error("El paquete 'openpyxl' no está instalado. Instálalo con 'pip install openpyxl'.")
    st.stop()

# ------------------------------
# Configuración de la página
# ------------------------------
st.set_page_config(page_title="Resultados test de Movilidad", layout="wide")
st.title("Resultados test de Movilidad")

# ------------------------------
# Ruta del archivo Excel
# ------------------------------
EXCEL_FILE = r"C:\Users\Daniel\Desktop\score_tscore\PRUEBAS MOVILIDAD.xlsx"

# ------------------------------
# Cargar datos (cacheado)
# ------------------------------
@st.cache_data
def cargar_datos(path):
    if not os.path.exists(path):
        st.error(f"No se encontró el archivo Excel en la ruta: {path}")
        return pd.DataFrame()
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        return pd.DataFrame()

df = cargar_datos(EXCEL_FILE)

# Botón de refrescar
if st.button("🔄 Refrescar datos"):
    df = cargar_datos(EXCEL_FILE)

if df.empty:
    st.stop()

# ------------------------------
# Columnas de identificación prioritarias
# ------------------------------
id_cols_prioritarias = ["JUGADOR", "ID", "NOMBRE", "APELLIDO",
                        "NOMBRE_COMPLETO", "NOMBRE Y APELLIDO", "NOMBRE_APELLIDO"]
id_cols = [col for col in id_cols_prioritarias if col in df.columns]

# ------------------------------
# Filtro por CATEGORÍA si existe
# ------------------------------
if "CATEGORÍA" in df.columns:
    categorias = ["Todas"] + sorted(df["CATEGORÍA"].dropna().astype(str).unique())
    seleccion_categoria = st.selectbox("Filtrar por CATEGORÍA", categorias)
    if seleccion_categoria != "Todas":
        df = df[df["CATEGORÍA"].astype(str) == seleccion_categoria]

# ------------------------------
# Definición de umbrales (ajusta si es necesario)
# ------------------------------
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

# ------------------------------
# Asegurar que las columnas numéricas sean numéricas
# ------------------------------
for col in cols_emoji:
    # convertimos valores a numéricos; valores no convertibles serán NaN
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ------------------------------
# Función para asignar emojis en HTML
# ------------------------------
def asignar_emoji_html(valor, umbral):
    if pd.isna(valor):
        return "<div style='font-size:20px; text-align:center; color:gray;'>—</div>"
    try:
        if float(valor) >= float(umbral):
            return "<div style='color:green; font-size:28px; text-align:center;'>👍</div>"
        else:
            return "<div style='color:red; font-size:28px; text-align:center;'>👎</div>"
    except Exception:
        return "<div style='font-size:20px; text-align:center; color:gray;'>—</div>"

# ------------------------------
# Crear copia con emojis (HTML) para las columnas indicadas
# ------------------------------
df_emojis = df.copy()
for col in cols_emoji:
    df_emojis[col] = df_emojis[col].apply(lambda x, u=umbral_cols[col]: asignar_emoji_html(x, u))

# ------------------------------
# Ordenar columnas: IDs primero si existen
# ------------------------------
otras_cols = [col for col in df_emojis.columns if col not in id_cols]
cols_finales = id_cols + otras_cols
df_emojis = df_emojis[cols_finales]

# ------------------------------
# Mostrar número de registros
# ------------------------------
st.markdown(f"**Número de registros mostrados:** {df_emojis.shape[0]}")

# ------------------------------
# Renderizar la tabla como HTML segura
# ------------------------------
html_table = df_emojis.to_html(escape=False, index=False)
# components.html permite renderizar el HTML generado (ajusta height si es necesario)
components.html(html_table, height=600, scrolling=True)
