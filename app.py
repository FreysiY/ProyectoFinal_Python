import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# CONFIGURACIÓN
# -------------------------------
st.set_page_config(page_title="Bank Marketing App", layout="wide")

# -------------------------------
# CLASE (POO)
# -------------------------------
class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    def resumen(self):
        return self.df.describe()

    def tipos_variables(self):
        num = self.df.select_dtypes(include=['int64', 'float64']).columns
        cat = self.df.select_dtypes(include=['object']).columns
        return num, cat

    def valores_nulos(self):
        return self.df.isnull().sum()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Menú")
opcion = st.sidebar.selectbox(
    "Selecciona un módulo",
    ["Home", "Carga de datos", "EDA"]
)

# -------------------------------
# MÓDULO 1: HOME
# -------------------------------
if opcion == "Home":
    st.title("📊 Proyecto Bank Marketing")

    st.write("""
    **Objetivo:** Analizar el dataset BankMarketing para identificar patrones
    en campañas de marketing.
    """)

    st.subheader("👩‍💻 Autor")
    st.write("""
    Nombre: Freysi Zurita  
    Curso: Python for Analytics  
    Año: 2026
    """)

    st.subheader("📁 Dataset")
    st.write("Datos de campañas de marketing bancario.")

    st.subheader("🛠 Tecnologías")
    st.write("Python, Pandas, Streamlit, Matplotlib, Seaborn")

# -------------------------------
# MÓDULO 2: CARGA DE DATOS
# -------------------------------
elif opcion == "Carga de datos":

    st.title("📂 Carga del Dataset")

    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

    if archivo is not None:
        df = pd.read_csv(archivo)

        st.success("Archivo cargado correctamente ✅")

        st.subheader("Vista previa")
        st.dataframe(df.head())

        st.subheader("Dimensiones")
        st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

    else:
        st.warning("Por favor, carga un archivo")

# -------------------------------
# MÓDULO 3: EDA
# -------------------------------
elif opcion == "EDA":

    st.title("📊 Análisis Exploratorio")

    archivo = st.file_uploader("Sube el CSV para analizar", type=["csv"])

    if archivo is not None:
        df = pd.read_csv(archivo)
        analyzer = DataAnalyzer(df)

        tab1, tab2, tab3, tab4 = st.tabs(
            ["General", "Numéricas", "Categóricas", "Avanzado"]
        )

        # -----------------------
        # TAB 1
        # -----------------------
        with tab1:
            st.subheader("Información general")

            st.write("Tipos de datos")
            st.write(df.dtypes)

            st.write("Valores nulos")
            st.write(analyzer.valores_nulos())

            st.write("Estadísticas")
            st.write(analyzer.resumen())

        # -----------------------
        # TAB 2
        # -----------------------
        with tab2:
            st.subheader("Variables numéricas")

            num_cols, _ = analyzer.tipos_variables()

            if len(num_cols) > 0:
                col = st.selectbox("Selecciona variable", list(num_cols))
            
                if col in df.columns:
                    fig, ax = plt.subplots()
                    sns.histplot(df[col], kde=True, ax=ax)
                    st.pyplot(fig)
                else:
                    st.error("La columna seleccionada no existe en el dataset")
            else:
                st.warning("No hay variables numéricas disponibles")

        # -----------------------
        # TAB 3
        # -----------------------
        with tab3:
            st.subheader("Variables categóricas")

            _, cat_cols = analyzer.tipos_variables()

            if len(cat_cols) > 0:
                col = st.selectbox("Selecciona variable categórica", list(cat_cols))
            
                if col in df.columns:
                    conteo = df[col].value_counts()
            
                    st.write(conteo)
            
                    fig, ax = plt.subplots()
                    conteo.plot(kind='bar', ax=ax)
                    st.pyplot(fig)
                else:
                    st.error("Columna inválida")
            else:
                st.warning("No hay variables categóricas")
    
        # -----------------------
        # TAB 4
        # -----------------------
        with tab4:
            st.subheader("Análisis bivariado")

            num_cols, cat_cols = analyzer.tipos_variables()

            if len(num_cols) > 0 and len(cat_cols) > 0:
            
                col_num = st.selectbox("Variable numérica", list(num_cols))
                col_cat = st.selectbox("Variable categórica", list(cat_cols))
            
                if col_num in df.columns and col_cat in df.columns:
                    fig, ax = plt.subplots()
                    sns.boxplot(x=df[col_cat], y=df[col_num], ax=ax)
                    st.pyplot(fig)
                else:
                    st.error("Columnas inválidas")
            else:
                st.warning("Faltan variables para análisis bivariado")

            # Hallazgos simples
            st.subheader("Hallazgos")
            st.write("""
            - Clientes con mayor duración de llamada tienden a aceptar más.
            - Algunas categorías muestran mayor conversión.
            """)

    else:
        st.warning("Primero carga el dataset")
