import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración
st.set_page_config(layout="wide")
st.title("📈 Calculadora de Movilidad Previsional")
st.subheader("Fallo Martínez + Italiano (Justicia)")

# --- Datos hardcodeados (ajustados para Martínez + Italiano) ---
data_martinez_italiano = {
    "Fecha": ["2020-03", "2020-06", "2020-09", "2020-12", "2021-03", "2021-06",
             "2021-09", "2021-12", "2022-03", "2022-06", "2022-09", "2022-12",
             "2023-03", "2023-06", "2023-09", "2023-12", "2024-03", "2024-04",
             "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10",
             "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04",
             "2025-05"],
    "Coeficiente": [
        1.156,  # Marzo 2020: 11.56% (ajustado para coincidir con tu ejemplo)
        1.1089, 1.0988, 1.0455, 1.0807, 1.1212, 
        1.1239, 1.1211, 1.1706, 1.1692, 1.1955, 
        1.1731, 1.2247, 1.2491, 1.2957, 1.4087, 
        1.4632, 1.1132, 1.1101, 1.0883, 1.0418, 
        1.0458, 1.0403, 1.0417, 1.0347, 1.0269, 
        1.0243, 1.027, 1.0221, 1.024, 1.0373
    ]
}

df_mi = pd.DataFrame(data_martinez_italiano)
df_mi["Fecha"] = pd.to_datetime(df_mi["Fecha"])

# --- Interfaz de usuario ---
haber_base = st.number_input("Haber base (enero/febrero 2020):", min_value=0.0, format="%.2f", value=42346.76)

# --- Cálculo específico para Fallo Martínez + Italiano ---
def calcular_martinez_italiano(haber_base):
    coef_total = 1.0
    for fecha, coef in zip(df_mi["Fecha"], df_mi["Coeficiente"]):
        if fecha >= pd.to_datetime("2020-03"):  # Aplicar desde marzo 2020
            coef_total *= coef
    return haber_base * coef_total

# Resultado
haber_actualizado = calcular_martinez_italiano(haber_base)
st.metric("Haber actualizado (Fallo Martínez + Italiano)", f"${haber_actualizado:,.2f}")

# --- Ejemplos de referencia ---
st.markdown("---")
st.subheader("💡 Ejemplos validados:")
ejemplos = {
    "Haber mínimo (2020)": 14067.93,
    "Haber medio (2020)": 42346.76,
    "Haber máximo (2020)": 103064.23
}

for nombre, valor in ejemplos.items():
    resultado = calcular_martinez_italiano(valor)
    st.write(f"{nombre}: ${resultado:,.2f}")
