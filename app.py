import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# Configuración inicial
st.set_page_config(layout="wide")

# Logo (asegúrate de tener el archivo logo_para_app.png en el mismo directorio)
try:
    st.image("logo_para_app.png", width=200)
except:
    st.warning("No se encontró el logo de la aplicación")

st.title("CALCULADORA MARTINEZ/ITALIANO")
st.subheader("Comparación de movilidad según ANSeS vs Justicia")

# Entradas de usuario
nombre = st.text_input("Nombre del caso")
haber = st.number_input("Ingrese el haber base", min_value=0.0, format="%.2f", step=100.0)
fecha_base = st.text_input("Fecha del haber base (YYYY-MM)", value="2020-03")

# Cargar datos
@st.cache_data
def cargar_datos():
    # Datos ANSeS (hardcodeados para evitar problemas con el archivo)
    data_anses = {
        "Fecha": ["2020-03", "2020-06", "2020-09", "2020-12", "2021-03", "2021-06", 
                 "2021-09", "2021-12", "2022-03", "2022-06", "2022-09", "2022-12",
                 "2023-03", "2023-06", "2023-09", "2023-12", "2024-03", "2024-04",
                 "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10",
                 "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04",
                 "2025-05", "2025-06"],
        "Coeficiente": [1.0, 1.0612, 1.075, 1.05, 1.0807, 1.1212, 1.1239, 1.1211,
                       1.1706, 1.1691, 1.1955, 1.1731, 1.2247, 1.2491, 1.2957,
                       1.4087, 1.4633, 1.132, 1.1101, 1.0883, 1.0418, 1.0458,
                       1.0403, 1.0417, 1.0347, 1.0269, 1.0243, 1.027, 1.0221,
                       1.024, 1.0373, 1.0278]
    }
    
    # Datos Justicia (corregidos los valores que estaban mal)
    data_justicia = {
        "Fecha": ["2020-03", "2020-06", "2020-09", "2020-12", "2021-03", "2021-06",
                 "2021-09", "2021-12", "2022-03", "2022-06", "2022-09", "2022-12",
                 "2023-03", "2023-06", "2023-09", "2023-12", "2024-03", "2024-04",
                 "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10",
                 "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04",
                 "2025-05"],
        "Coeficiente": [1.1156, 1.1089, 1.0988, 1.0455, 1.0807, 1.1212, 1.1239,
                        1.1211, 1.1706, 1.1692, 1.1955, 1.1731, 1.2247, 1.2491,
                        1.2957, 1.4087, 1.4632, 1.1132, 1.1101, 1.0883, 1.0418,
                        1.0458, 1.0403, 1.0417, 1.0347, 1.0269, 1.0243, 1.027,
                        1.0221, 1.024, 1.0373]
    }
    
    df_anses = pd.DataFrame(data_anses)
    df_justicia = pd.DataFrame(data_justicia)
    
    # Convertir fechas
    df_anses["Fecha"] = pd.to_datetime(df_anses["Fecha"], format="%Y-%m")
    df_justicia["Fecha"] = pd.to_datetime(df_justicia["Fecha"], format="%Y-%m")
    
    return df_anses, df_justicia

try:
    df_anses, df_justicia = cargar_datos()
    
    # Validar fecha base
    fecha_base_dt = pd.to_datetime(fecha_base, format="%Y-%m")
    
    # Verificar que la fecha base sea válida
    min_fecha_anses = df_anses["Fecha"].min()
    min_fecha_justicia = df_justicia["Fecha"].min()
    min_fecha = max(min_fecha_anses, min_fecha_justicia)
    
    if fecha_base_dt < min_fecha:
        st.warning(f"La fecha base no puede ser anterior a {min_fecha.strftime('%Y-%m')}. Se usará {min_fecha.strftime('%Y-%m')} como fecha base.")
        fecha_base_dt = min_fecha
    
    # Filtrar coeficientes desde fecha base
    coef_anses = df_anses[df_anses["Fecha"] >= fecha_base_dt]["Coeficiente"]
    coef_justicia = df_justicia[df_justicia["Fecha"] >= fecha_base_dt]["Coeficiente"]
    
    if coef_anses.empty or coef_justicia.empty:
        st.error("No hay datos disponibles para la fecha seleccionada")
        st.stop()
    
    # Calcular actualización
    haber_anses = haber
    for c in coef_anses:
        haber_anses *= c
    
    haber_justicia = haber
    for c in coef_justicia:
        haber_justicia *= c
    
    # Calcular diferencia y porcentaje
    diferencia = haber_justicia - haber_anses
    if haber_anses != 0:
        porcentaje = (diferencia / haber_anses) * 100
    else:
        porcentaje = 0
    
    # Mostrar resultados
    st.markdown("---")
    st.markdown("### Resultados:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Haber actualizado según ANSeS", f"${haber_anses:,.2f}")
    
    with col2:
        st.metric("Haber actualizado según Justicia", f"${haber_justicia:,.2f}")
    
    st.metric("Diferencia", 
              f"${diferencia:,.2f}", 
              f"{porcentaje:.2f}%",
              delta_color="inverse")
    
    # Gráfico comparativo
    st.markdown("---")
    st.markdown("### Evolución comparativa")
    
    # Preparar datos para el gráfico
    fechas_comunes = sorted(set(df_anses["Fecha"]).union(set(df_justicia["Fecha"])))
    fechas_comunes = [f for f in fechas_comunes if f >= fecha_base_dt]
    
    evol_anses = [haber]
    evol_justicia = [haber]
    
    for fecha in fechas_comunes[1:]:
        # ANSeS
        coef = df_anses[df_anses["Fecha"] == fecha]["Coeficiente"]
        if not coef.empty:
            evol_anses.append(evol_anses[-1] * coef.values[0])
        else:
            evol_anses.append(evol_anses[-1])
        
        # Justicia
        coef = df_justicia[df_justicia["Fecha"] == fecha]["Coeficiente"]
        if not coef.empty:
            evol_justicia.append(evol_justicia[-1] * coef.values[0])
        else:
            evol_justicia.append(evol_justicia[-1])
    
    # Crear DataFrame para el gráfico
    df_evol = pd.DataFrame({
        "Fecha": fechas_comunes,
        "ANSeS": evol_anses,
        "Justicia": evol_justicia
    })
    
    # Mostrar gráfico
    st.line_chart(df_evol.set_index("Fecha"))

except Exception as e:
    st.error(f"Ocurrió un error: {str(e)}")
    st.error("Por favor verifica los datos ingresados y vuelve a intentar.")
