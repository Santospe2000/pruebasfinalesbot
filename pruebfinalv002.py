# -*- coding: utf-8 -*-
import streamlit as st
import os
from openai import OpenAI
from fpdf import FPDF
import matplotlib.pyplot as plt
import re  # Para validar expresiones regulares (email, teléfono)

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Función para generar un PDF con el informe
def generar_pdf(usuario, analisis_financiero=None, analisis_inversion=None, analisis_retiro=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título del informe
    pdf.cell(200, 10, txt="Informe Financiero Personal", ln=True, align="C")
    pdf.ln(10)

    # Información del usuario
    pdf.cell(200, 10, txt=f"Nombre: {usuario['nombre']}", ln=True)
    pdf.cell(200, 10, txt=f"Edad: {usuario['edad']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {usuario['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Teléfono: {usuario['telefono']}", ln=True)
    pdf.ln(10)

    # Análisis financiero
    if analisis_financiero:
        pdf.cell(200, 10, txt="Análisis Financiero:", ln=True)
        pdf.multi_cell(0, 10, txt=analisis_financiero)
        pdf.ln(5)

    # Análisis de inversión
    if analisis_inversion:
        pdf.cell(200, 10, txt="Análisis de Plan de Inversión:", ln=True)
        pdf.multi_cell(0, 10, txt=analisis_inversion)
        pdf.ln(5)

    # Análisis de retiro
    if analisis_retiro:
        pdf.cell(200, 10, txt="Análisis de Proyección de Retiro:", ln=True)
        pdf.multi_cell(0, 10, txt=analisis_retiro)
        pdf.ln(5)

    # Guardar el PDF
    pdf_output = "informe_financiero.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Función para validar el correo electrónico
def validar_email(email):
    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return True
    return False

# Función para validar el teléfono
def validar_telefono(telefono):
    if re.match(r"^\+?[0-9]{10,15}$", telefono):  # Acepta números de 10 a 15 dígitos, con o sin +
        return True
    return False

# Función para registrar al usuario
def registrar_usuario():
    st.write("\n¡Bienvenido al Bot de Finanzas Personales De Carlos Devis!")
    nombre = st.text_input("Nombre", max_chars=50)
    edad = st.number_input("Edad", min_value=0, max_value=120)
    email = st.text_input("Email", max_chars=100)
    telefono = st.text_input("Teléfono", max_chars=15)

    if st.button("Registrar"):
        if not nombre:
            st.error("El nombre es obligatorio.")
        elif not email or not validar_email(email):
            st.error("Por favor, ingresa un correo electrónico válido.")
        elif not telefono or not validar_telefono(telefono):
            st.error("Por favor, ingresa un número de teléfono válido.")
        else:
            st.session_state['usuario'] = {"nombre": nombre, "edad": edad, "email": email, "telefono": telefono}
            st.success("Usuario registrado con éxito.")
            st.session_state['current_tab'] = "Situación Financiera"  # Pasar a la siguiente pestaña

# Función para evaluar la situación financiera
def evaluar_situacion_financiera():
    st.write("\nPor favor, ingresa tus datos financieros en dólares ($):")
    activos = st.number_input("¿Cuáles son tus activos totales? (efectivo, inversiones, propiedades, etc.): $", min_value=0.0)
    pasivos = st.number_input("¿Cuáles son tus pasivos totales? (deudas, préstamos, hipotecas, etc.): $", min_value=0.0)
    ingresos_mensuales = st.number_input("¿Cuáles son tus ingresos mensuales?: $", min_value=0.0)
    gastos_mensuales = st.number_input("¿Cuáles son tus gastos mensuales?: $", min_value=0.0)

    if st.button("Evaluar situación financiera"):
        if activos < 0 or pasivos < 0 or ingresos_mensuales < 0 or gastos_mensuales < 0:
            st.error("Los valores no pueden ser negativos.")
        else:
            patrimonio_neto = activos - pasivos
            flujo_efectivo_mensual = ingresos_mensuales - gastos_mensuales

            st.write(f"\nPatrimonio Neto: ${patrimonio_neto:.2f}")
            st.write(f"Flujo de Efectivo Mensual: ${flujo_efectivo_mensual:.2f}")

            st.session_state['situacion_financiera'] = {"activos": activos, "pasivos": pasivos, "ingresos_mensuales": ingresos_mensuales, "gastos_mensuales": gastos_mensuales}
            st.session_state['current_tab'] = "Plan de Inversión"  # Pasar a la siguiente pestaña

# Función para evaluar el plan de inversión
def evaluar_plan_inversion():
    st.write("\nPor favor, ingresa tus datos de inversión:")
    objetivos = st.text_input("¿Cuáles son tus objetivos de inversión? (corto, mediano, largo plazo)", max_chars=100)
    preferencias = st.text_input("¿Cuáles son tus preferencias de inversión? (acciones, bonos, bienes raíces, etc.)", max_chars=100)

    if st.button("Evaluar plan de inversión"):
        if not objetivos or not preferencias:
            st.error("Todos los campos son obligatorios.")
        else:
            st.session_state['plan_inversion'] = {"objetivos": objetivos, "preferencias": preferencias}
            st.session_state['current_tab'] = "Proyección de Retiro"  # Pasar a la siguiente pestaña

# Función para evaluar la proyección de retiro
def evaluar_proyeccion_retiro():
    st.write("\nPor favor, ingresa tus datos de retiro en dólares ($):")
    edad_actual = st.number_input("Edad actual", min_value=0, max_value=120)
    edad_retiro = st.number_input("Edad de retiro deseada", min_value=0, max_value=120)
    ingresos_retiro = st.number_input("Ingresos esperados durante el retiro (anuales): $", min_value=0.0)
    gastos_retiro = st.number_input("Gastos esperados durante el retiro (anuales): $", min_value=0.0)
    ahorros_actuales = st.number_input("Ahorros actuales para el retiro: $", min_value=0.0)
    ahorros_proyectados = st.number_input("Ahorros proyectados anuales: $", min_value=0.0)

    if st.button("Evaluar proyección de retiro"):
        if edad_retiro <= edad_actual:
            st.error("La edad de retiro debe ser mayor que la edad actual.")
        elif ingresos_retiro < 0 or gastos_retiro < 0 or ahorros_actuales < 0 or ahorros_proyectados < 0:
            st.error("Los valores no pueden ser negativos.")
        else:
            st.session_state['proyeccion_retiro'] = {"edad_actual": edad_actual, "edad_retiro": edad_retiro, "ingresos_retiro": ingresos_retiro, "gastos_retiro": gastos_retiro, "ahorros_actuales": ahorros_actuales, "ahorros_proyectados": ahorros_proyectados}
            st.session_state['current_tab'] = "Resumen"  # Pasar a la siguiente pestaña

# Función para analizar con OpenAI
def analizar_con_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un analista financiero experto. Analiza la información proporcionada y proporciona recomendaciones claras y detalladas."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error al conectar con OpenAI: {e}")
        return None

# Función para generar la gráfica de status
def generar_grafica_status(status):
    fig, ax = plt.subplots(figsize=(10, 2))
    
    # Definir el color de la barra según el porcentaje
    if status <= 50:
        color = 'red'
    elif status <= 80:
        color = 'yellow'
    else:
        color = 'green'
    
    # Crear la barra
    ax.barh([0], [status], color=color, height=0.5)
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 10))
    ax.set_yticks([])
    ax.set_title(f"Status de tu posición financiera: {status}% 📈")
    st.pyplot(fig)

# Función principal
def main():
    # Estilos CSS para mejorar la presentación
    st.markdown("""
        <style>
            .stApp {
                max-width: 1200px;
                margin: auto;
                padding: 20px;
                background-color: #f0f2f6;
            }
            .stButton>button {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                background-color: #1f77b4;
                color: white;
                border-radius: 5px;
            }
            .stButton>button:hover {
                background-color: #165a8a;
            }
            .stTextInput>div>div>input, .stNumberInput>div>div>input {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            .stMarkdown {
                margin-bottom: 20px;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
            }
            .stTabs [data-baseweb="tab"] {
                padding: 10px 20px;
                border-radius: 5px;
                background-color: #e0e0e0;
            }
            .stTabs [aria-selected="true"] {
                background-color: #1f77b4;
                color: white;
            }
            .status-bar {
                background-color: #1f77b4;
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo y título
    st.image("aaaaa.png", width=100)  # Asegúrate de tener un archivo logo.png en el mismo directorio
    st.title("Bot de Finanzas Personales De Carlos Devis")

    # Inicializar la pestaña actual en el estado de la sesión
    if 'current_tab' not in st.session_state:
        st.session_state['current_tab'] = "Registro"

    # Crear pestañas para cada módulo
    tabs = ["Registro", "Situación Financiera", "Plan de Inversión", "Proyección de Retiro", "Resumen"]
    current_tab_index = tabs.index(st.session_state['current_tab'])

    # Mostrar la pestaña actual
    if st.session_state['current_tab'] == "Registro":
        registrar_usuario()
    elif st.session_state['current_tab'] == "Situación Financiera":
        evaluar_situacion_financiera()
    elif st.session_state['current_tab'] == "Plan de Inversión":
        evaluar_plan_inversion()
    elif st.session_state['current_tab'] == "Proyección de Retiro":
        evaluar_proyeccion_retiro()
    elif st.session_state['current_tab'] == "Resumen":
        st.write("\nResumen de tu análisis financiero:")
        st.write(f"**Nombre:** {st.session_state['usuario']['nombre']}")
        st.write(f"**Edad:** {st.session_state['usuario']['edad']}")
        st.write(f"**Email:** {st.session_state['usuario']['email']}")
        st.write(f"**Teléfono:** {st.session_state['usuario']['telefono']}")

        if 'analisis_financiero' in st.session_state:
            st.write("\n**Análisis Financiero:**")
            st.write(st.session_state['analisis_financiero'])

        if 'analisis_inversion' in st.session_state:
            st.write("\n**Análisis de Plan de Inversión:**")
            st.write(st.session_state['analisis_inversion'])

        if 'analisis_retiro' in st.session_state:
            st.write("\n**Análisis de Proyección de Retiro:**")
            st.write(st.session_state['analisis_retiro'])

        # Gráfica de status
        if 'analisis_financiero' in st.session_state and 'analisis_inversion' in st.session_state and 'analisis_retiro' in st.session_state:
            status = 75  # Este valor debería ser calculado en base a los análisis
            generar_grafica_status(status)

        # Botón para descargar el informe en PDF
        if st.button("Descargar Informe en PDF"):
            pdf_path = generar_pdf(
                st.session_state['usuario'],
                st.session_state.get('analisis_financiero'),
                st.session_state.get('analisis_inversion'),
                st.session_state.get('analisis_retiro')
            )
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="Descargar PDF",
                    data=file,
                    file_name="informe_financiero.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()