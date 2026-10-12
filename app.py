import streamlit as st
import pandas as pd
import os

st.title("Control de Gastos Familiares 📊")

st.subheader("Cargar nuevo gasto")
with st.form("form_gasto", clear_on_submit=True):
    concepto = st.text_input("Concepto del gasto (ej: Supermercado)")
    monto = st.number_input("Monto ($)", min_value=0.0, step=100.0)
    enviar = st.form_submit_button("Registrar Gasto")

if enviar:
    if concepto and monto > 0:
        archivo_existe = os.path.exists("gastos.csv")
        df_nuevo = pd.DataFrame([[concepto, monto]], columns=["Concepto", "Monto"])
        df_nuevo.to_csv("gastos.csv", mode="a", index=False, header=not archivo_existe)
        st.success(f"¡Guardado! {concepto}: ${monto}")
        st.rerun()
    else:
        st.warning("Completá bien los datos antes de guardar.")

st.markdown("---")
st.subheader("Historial y Análisis")

if os.path.exists("gastos.csv"):
    try:
        df = pd.read_csv("gastos.csv")
        if "Monto" not in df.columns or "Concepto" not in df.columns:
            df = pd.read_csv("gastos.csv", header=None, names=["Concepto", "Monto"])
    except Exception:
        df = pd.DataFrame(columns=["Concepto", "Monto"])

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        total_gastado = df["Monto"].sum()
        st.metric(label="Total Gastado", value=f"${total_gastado:,.2f}")
        
        df_agrupado = df.groupby("Concepto")["Monto"].sum()
        
        st.subheader("Evolución Visual")
        st.bar_chart(df_agrupado)
    else:
        st.info("El archivo CSV está vacío.")
else:
    st.warning("Todavía no hay registros cargados. ¡Cargá el primero arriba!")