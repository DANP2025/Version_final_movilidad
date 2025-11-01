# app.py
import streamlit as st
import pandas as pd
import os

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(
    page_title="Resultados test de Movilidad",
    layout="wide"
)

# Título principal
st.title("📊 Resultados test de Movilidad")

# Mostrar logo (debe estar en la misma carpeta que app.py)
st.image("logo.png", width=180)  # Ajustá el tamaño si querés

# ==============================
# FUNCIONES
# ==============================

@st.cache_data
def cargar_datos():
    """
    Carga los datos desde el archivo Excel.
    Si el archivo no se encuentra o hay error, muestra un mensaje.
    """
    archivo_excel = "PRUEBAS MOVILIDAD.xlsx"
    
    if not os.path.exists(archivo_excel):
        st.error(f"No se encontró el archivo Excel en la carpeta del proyecto: {archivo_excel}")
        return pd.DataFrame()
    
    try:
        df = pd.read_excel(archivo_excel)
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        return pd.DataFrame()

# ==============================
# CARGAR DATOS
# ==============================
df = cargar_datos()

# Botón para refrescar los datos
if st.button("🔄 Refrescar datos"):
    df = cargar_datos()

if df.empty:
    st.stop()

# ==============================
# FILTRO POR CATEGORÍA
# ==============================
if "CATEGORÍA" in df.columns:
    categorias = ["Todas"] + sorted(df["CATEGORÍA"].dropna().astype(str).unique())
    seleccion_categoria = st.selectbox("Filtrar por CATEGORÍA", categorias)
    if seleccion_categoria != "Todas":
        df = df[df["CATEGORÍA"].astype(str) == seleccion_categoria]

# ==============================
# COLUMNAS Y UMBRALES
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
# FUNCIÓN PARA ASIGNAR EMOJIS
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

# ==============================
# CREAR DATAFRAME CON EMOJIS
# ==============================
df_emojis = df.copy()
for col in cols_emoji:
    df_emojis[col] = df_emojis[col].apply(lambda x: asignar_emoji_html(x, umbral_cols[col]))

# ==============================
# COLUMNAS DE IDENTIFICACIÓN
# ==============================
id_cols_prioritarias = ["JUGADOR", "ID", "NOMBRE", "APELLIDO", "NOMBRE_COMPLETO", "NOMBRE Y APELLIDO", "NOMBRE_APELLIDO"]
id_cols = [col for col in id_cols_prioritarias if col in df_emojis.columns]
otras_cols = [col for col in df_emojis.columns if col not in id_cols]
df_emojis = df_emojis[id_cols + otras_cols]

# ==============================
# MOSTRAR TABLA
# ==============================
st.markdown(f"**Número de registros mostrados:** {df_emojis.shape[0]}")
st.markdown(df_emojis.to_html(escape=False, index=False), unsafe_allow_html=True)

st.success("✅ Datos cargados correctamente.")
