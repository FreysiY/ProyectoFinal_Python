import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Bank Marketing", layout="wide")

# -------------------------
# CACHE (CLAVE PARA MEMORIA)
# -------------------------
@st.cache_data
def cargar_datos(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    return df

# -------------------------
# CLASE (POO SIMPLE)
# -------------------------
class Analizador:
    def __init__(self, df):
        self.df = df

    def numericas(self):
        return self.df.select_dtypes(include=['int64', 'float64']).columns

    def categoricas(self):
        return self.df.select_dtypes(include=['object']).columns

    def nulos(self):
        return self.df.isnull().sum()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("Menú")
menu = st.sidebar.selectbox("Ir a:", ["Home", "Carga", "EDA"])

# -------------------------
# HOME
# -------------------------
if menu == "Home":
    st.title("📊 Bank Marketing App")

    st.write("Análisis exploratorio del dataset de marketing bancario.")

    st.write("""
    **Autor:** Freysi Zurita  
    **Curso:** Python for Analytics  
    """)

# -------------------------
# CARGA
# -------------------------
elif menu == "Carga":
    st.title("📂 Carga de datos")

    file = st.file_uploader("Sube el CSV", type=["csv"])

    if file:
        df = cargar_datos(file)

        st.success("Archivo cargado")

        st.write(df.head())

        st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

# -------------------------
# EDA
# -------------------------
elif menu == "EDA":
    st.title("📊 EDA - Análisis Exploratorio")

    file = st.file_uploader("Sube el CSV", type=["csv"])

    if file:
        df = cargar_datos(file)

        # 🔥 REDUCIR TAMAÑO (CLAVE)
        if len(df) > 5000:
            df = df.sample(5000, random_state=1)

        analizador = Analizador(df)

        tabs = st.tabs([
            "1. Info",
            "2. Variables",
            "3. Estadísticas",
            "4. Nulos",
            "5. Numéricas",
            "6. Categóricas",
            "7. Num vs Cat",
            "8. Cat vs Cat",
            "9. Dinámico",
            "10. Hallazgos"
        ])

        # -------------------------
        # 1. INFO
        # -------------------------
        with tabs[0]:
            st.subheader("Información general")

            st.write(df.dtypes)
            st.write("Filas y columnas:", df.shape)

        # -------------------------
        # 2. VARIABLES
        # -------------------------
        with tabs[1]:
            num = analizador.numericas()
            cat = analizador.categoricas()

            st.write("Numéricas:", list(num))
            st.write("Categóricas:", list(cat))

        # -------------------------
        # 3. ESTADÍSTICAS
        # -------------------------
        with tabs[2]:
            st.write(df.describe())

        # -------------------------
        # 4. NULOS
        # -------------------------
        with tabs[3]:
            nulos = analizador.nulos()
            st.write(nulos[nulos > 0])

        # -------------------------
        # 5. NUMÉRICAS
        # -------------------------
        with tabs[4]:
            num = list(analizador.numericas())

            if num:
                col = st.selectbox("Selecciona variable", num)

                fig, ax = plt.subplots()
                ax.hist(df[col], bins=30)
                st.pyplot(fig)

        # -------------------------
        # 6. CATEGÓRICAS
        # -------------------------
        with tabs[5]:
            cat = list(analizador.categoricas())

            if cat:
                col = st.selectbox("Variable categórica", cat)

                conteo = df[col].value_counts().head(10)

                fig, ax = plt.subplots()
                conteo.plot(kind="bar", ax=ax)
                st.pyplot(fig)

        # -------------------------
        # 7. NUM vs CAT
        # -------------------------
        with tabs[6]:
            num = list(analizador.numericas())
            cat = list(analizador.categoricas())

            if num and cat:
                col_num = st.selectbox("Numérica", num)
                col_cat = st.selectbox("Categórica", cat)

                df.groupby(col_cat)[col_num].mean().head(10).plot(kind="bar")
                st.pyplot(plt)

        # -------------------------
        # 8. CAT vs CAT
        # -------------------------
        with tabs[7]:
            cat = list(analizador.categoricas())

            if len(cat) >= 2:
                col1 = st.selectbox("Variable 1", cat)
                col2 = st.selectbox("Variable 2", cat)

                tabla = pd.crosstab(df[col1], df[col2])
                st.write(tabla)

        # -------------------------
        # 9. DINÁMICO
        # -------------------------
        with tabs[8]:
            columnas = st.multiselect("Selecciona columnas", df.columns)

            if columnas:
                st.write(df[columnas].head())

        # -------------------------
        # 10. HALLAZGOS
        # -------------------------
        with tabs[9]:
            st.write("""
            🔎 Hallazgos principales:

            1. Mayor duración de llamada → mayor probabilidad de éxito.
            2. Algunas ocupaciones responden mejor a campañas.
            3. Variables económicas influyen en la decisión.
            4. Contactos repetidos pueden mejorar conversión.
            5. El canal de contacto impacta resultados.
            """)
    else:
        st.warning("Carga el dataset primero")
