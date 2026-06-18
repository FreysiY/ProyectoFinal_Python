import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bank Marketing", layout="wide")

@st.cache_data
def cargar_datos(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    return df

# CLASE (POO SIMPLE)

class Analizador:
    def __init__(self, df):
        self.df = df

    def numericas(self):
        return self.df.select_dtypes(include=['int64', 'float64']).columns

    def categoricas(self):
        return self.df.select_dtypes(include=['object']).columns

    def nulos(self):
        return self.df.isnull().sum()

# SIDEBAR

st.sidebar.title("Menú")
menu = st.sidebar.selectbox("Ir a:", ["Home", "Carga", "EDA"])

# HOME

if menu == "Home":
    st.title("Proyecto: Análisis de Campañas de Marketing Bancario")

    st.markdown("---")

    # DESCRIPCIÓN DEL PROYECTO
    
    st.subheader("Objetivo del Proyecto")

    st.write("""
    El objetivo de esta aplicación es realizar un Análisis Exploratorio de Datos (EDA) sobre un dataset de marketing bancario, con el fin de identificar patrones, comportamientos y factores que influyen en la aceptación de campañas.
    """)

    # DATOS DEL AUTOR
   
    st.subheader("Datos del Autor")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Nombre:** Freysi Zurita")
        st.write("**Curso:** Python for Analytics")

    with col2:
        st.write("**Año:** 2026")
        st.write("**Proyecto:** Caso de Estudio N°1")

    # EXPLICACIÓN DEL DATASET
 
    st.subheader("Descripción del Dataset")

    st.write("""
    El dataset BankMarketing contiene información de campañas realizadas por una institución financiera, donde se busca analizar qué factores influyen en que un cliente acepte o no una oferta.

    Incluye variables demográficas, económicas y de comportamiento, como:
    - Edad del cliente
    - Tipo de trabajo
    - Nivel educativo
    - Tipo de contacto
    - Duración de la llamada
    - Resultado de la campaña (variable objetivo: **y**)
    """)

    # CONTEXTO DEL PROBLEMA

    st.subheader("Contexto del Negocio")

    st.write("""
    La efectividad de las campañas de marketing ha disminuido en los últimos meses, pasando de un 12% a un 8%, lo cual afecta directamente los resultados comerciales. A través de este análisis se busca identificar oportunidades de mejora
    para optimizar las estrategias de contacto con los clientes.
    """)

    # TECNOLOGÍAS

    st.subheader("Tecnologías Utilizadas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Python")
        st.write("Pandas")

    with col2:
        st.write("Matplotlib")
        st.write("Streamlit")

    with col3:
        st.write("Análisis estadístico")
        st.write("EDA")

    st.markdown("---")

    # NOTA FINAL
    st.info("Aplicación desarrollada como proyecto académico orientado a análisis de datos.")


# CARGA

elif menu == "Carga":
    st.title("Carga de datos")

    file = st.file_uploader("Sube el CSV", type=["csv"])

    if file:
        df = cargar_datos(file)

        st.success("Archivo cargado")

        st.write(df.head())

        st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

# EDA

elif menu == "EDA":
    st.title("EDA - Análisis Exploratorio")

    file = st.file_uploader("Sube el CSV", type=["csv"])

    if file:
        df = cargar_datos(file)

        # REDUCIR TAMAÑO (CLAVE)
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

        # 1. INFO

        with tabs[0]:
            st.subheader("Información general")

            st.write(df.dtypes)
            st.write("Filas y columnas:", df.shape)

        # 2. VARIABLES

        with tabs[1]:
            num = analizador.numericas()
            cat = analizador.categoricas()

            st.write("Numéricas:", list(num))
            st.write("Categóricas:", list(cat))

        # 3. ESTADÍSTICAS

        with tabs[2]:
            st.write(df.describe())

        # 4. NULOS

        with tabs[3]:
            nulos = analizador.nulos()
            st.write(nulos[nulos > 0])

        # 5. NUMÉRICAS

        with tabs[4]:
            st.subheader("Distribución de variables numéricas")
        
            num = list(analizador.numericas())
        
            if len(num) > 0:
                col = st.selectbox("Selecciona una variable numérica", num, key="num5")
        
                if col:
                    st.write(f"Histograma de: {col}")
        
                    fig, ax = plt.subplots()
                    ax.hist(df[col].dropna(), bins=30)
        
                    st.pyplot(fig)
                else:
                    st.info("Selecciona una variable para visualizar")
            else:
                st.warning("No hay variables numéricas en el dataset")

        # 6. CATEGÓRICAS

        with tabs[5]:
            cat = list(analizador.categoricas())

            if cat:
                col = st.selectbox("Variable categórica", cat)

                conteo = df[col].value_counts().head(10)

                fig, ax = plt.subplots()
                conteo.plot(kind="bar", ax=ax)
                st.pyplot(fig)

        # 7. NUM vs CAT

        with tabs[6]:
            st.subheader("Relación: Variable numérica vs categórica")
        
            num = list(analizador.numericas())
            cat = list(analizador.categoricas())
        
            if len(num) > 0 and len(cat) > 0:
        
                col_num = st.selectbox("Variable numérica", num, key="num7")
                col_cat = st.selectbox("Variable categórica", cat, key="cat7")
        
                if col_num and col_cat:
                    st.write(f"Promedio de {col_num} por {col_cat}")
        
                    data = df.groupby(col_cat)[col_num].mean().sort_values(ascending=False).head(10)
        
                    fig, ax = plt.subplots()
                    data.plot(kind="bar", ax=ax)
        
                    st.pyplot(fig)
                else:
                    st.info("Selecciona ambas variables")
            else:
                st.warning("No hay suficientes variables para este análisis")

        # 8. CAT vs CAT

        with tabs[7]:
            st.subheader("Relación entre variables categóricas")
        
            cat = list(analizador.categoricas())
        
            if len(cat) >= 2:
        
                col1 = st.selectbox("Variable 1", cat, key="cat1_8")
                col2 = st.selectbox("Variable 2", cat, key="cat2_8")
        
                if col1 and col2:
                    tabla = pd.crosstab(df[col1], df[col2])
        
                    st.write("Tabla de contingencia:")
                    st.dataframe(tabla)
        
                else:
                    st.info("Selecciona ambas variables")
            else:
                st.warning("Se necesitan al menos 2 variables categóricas")

        # 9. DINÁMICO

        with tabs[8]:
            columnas = st.multiselect("Selecciona columnas", df.columns)

            if columnas:
                st.write(df[columnas].head())

        # 10. HALLAZGOS

        with tabs[9]:
            st.write("""
             Hallazgos principales:

            1.	La duración de la interacción con el cliente es el factor más influyente en la aceptación de la campaña.
            2.	Existen segmentos de clientes más propensos a aceptar ofertas, especialmente según su ocupación y nivel educativo.
            3.	El canal de comunicación utilizado impacta significativamente en los resultados.
            4.	Las condiciones económicas influyen en la decisión del cliente, por lo que deben considerarse en las estrategias.
            5.	Un mayor número de contactos puede incrementar la probabilidad de éxito si se realiza de forma adecuada.

            """)
    else:
        st.warning("Carga el dataset primero")
