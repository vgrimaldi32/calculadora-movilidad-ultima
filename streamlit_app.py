import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración
st.set_page_config(layout="wide")
st.title("📈 Calculadora de Movilidad Previsional")
st.subheader("Comparación: ANSeS (ley) vs. Fallos Martínez/Italiano (Justicia)")

# --- Datos hardcodeados ---
# Coeficientes ANSeS (aumentos de ley)
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

# Coeficientes Justicia (Fallos combinados Martínez/Italiano)
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
df_anses["Fecha"] = pd.to_datetime(df_anses["Fecha"])
df_justicia["Fecha"] = pd.to_datetime(df_justicia["Fecha"])

# --- Interfaz de usuario ---
nombre = st.text_input("Nombre de la persona:")
haber_base = st.number_input("Haber base:", min_value=0.0, format="%.2f", value=38000.0)
fecha_base = st.text_input("Fecha de jubilación o primer cobro (YYYY-MM):", value="2021-10")

# --- Cálculos ---
def calcular_actualizacion(haber_base, fecha_base):
    fecha_base_dt = pd.to_datetime(fecha_base)
    
    # ANSeS
    coefs_anses = df_anses[df_anses["Fecha"] >= fecha_base_dt]["Coeficiente"]
    haber_anses = haber_base
    for coef in coefs_anses:
        haber_anses *= coef
    
    # Justicia
    coefs_justicia = df_justicia[df_justicia["Fecha"] >= fecha_base_dt]["Coeficiente"]
    haber_justicia = haber_base
    for coef in coefs_justicia:
        haber_justicia *= coef
    
    return haber_anses, haber_justicia

if st.button("Calcular"):
    try:
        haber_anses, haber_justicia = calcular_actualizacion(haber_base, fecha_base)
        diferencia = haber_justicia - haber_anses
        porcentaje = (diferencia / haber_anses) * 100 if haber_anses != 0 else 0
        
        st.markdown("---")
        st.subheader(f"🔍 Resultados para {nombre}:")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ANSeS (Ley)", f"${haber_anses:,.2f}")
        with col2:
            st.metric("Justicia (Fallos)", f"${haber_justicia:,.2f}")
        
        st.metric("Diferencia", 
                 f"${diferencia:,.2f}", 
                 f"{porcentaje:.2f}%",
                 delta_color="inverse")
        
        # Ejemplo: $38,000 desde octubre 2021
        if fecha_base == "2021-10":
            st.info(f"💡 Ejemplo validado: Para $38,000 desde octubre 2021, el resultado debería ser ~$XXX.XXX (ajústame el número esperado para calibrar).")
    
    except Exception as e:
        st.error(f"Error: {e}. Verifica la fecha ingresada.")

# --- Instrucciones ---
st.markdown("---")
st.info("""
**📌 Instrucciones:**  
1. Ingresa el nombre de la persona (opcional).  
2. Indica el **haber base** (ej: $38,000 en octubre 2021).  
3. Selecciona la **fecha de jubilación o primer cobro** (formato YYYY-MM).  
4. Haz clic en **Calcular** para ver la comparación.  
""")
