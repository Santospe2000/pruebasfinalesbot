# -*- coding: utf-8 -*-
import streamlit as st
import os
from openai import OpenAI
from fpdf import FPDF
import matplotlib.pyplot as plt
import re
from PIL import Image

# Configuración inicial
st.set_page_config(page_title="Bot de Finanzas Personales", page_icon="💰", layout="wide")

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paleta de colores corporativos
COLOR_PRIMARIO = "#003366"  # Azul oscuro
COLOR_SECUNDARIO = "#808080"  # Gris
COLOR_FONDO = "#FFFFFF"  # Blanco
COLOR_BORDES = "#1E90FF"  # Azul brillante para bordes

# Frases de motivación y sugerencias de educación financiera
MOTIVACIONES = [
    "Nunca se pone mejor que un 'sí'.",
    "Golpee mientras el hierro está caliente.",
    "Trabaje con vendedores y compradores motivados.",
    # ... (resto de las frases originales)
]

SUGERENCIAS_EDUCACION = [
    "Las finanzas personales, la base de todo.",
    "Si gastas todo o más de lo que ganas, nunca lograrás tu libertad financiera.",
    # ... (resto de las sugerencias originales)
]

# Cargar imagen corporativa
def cargar_imagen():
    try:
        image = Image.open("aaaaa.png")  # Asegúrate de tener esta imagen en tu directorio
        return image
    except:
        st.warning("Imagen corporativa no encontrada")
        return None

# Estilos CSS personalizados
def aplicar_estilos():
    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {COLOR_FONDO};
                color: {COLOR_PRIMARIO};
            }}
            .css-18e3th9 {{
                padding: 2rem 5rem;
            }}
            .st-bb {{
                background-color: {COLOR_FONDO};
            }}
            .st-at {{
                background-color: {COLOR_PRIMARIO};
            }}
            .stTextInput>div>div>input, .stNumberInput>div>div>input {{
                border: 2px solid {COLOR_BORDES};
                border-radius: 5px;
                padding: 8px;
            }}
            .stButton>button {{
                background-color: {COLOR_PRIMARIO};
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 5px;
                font-weight: bold;
                margin: 10px 0;
                width: 100%;
            }}
            .stButton>button:hover {{
                background-color: #004080;
                color: white;
            }}
            .css-1aumxhk {{
                background-color: {COLOR_FONDO};
                border: 2px solid {COLOR_BORDES};
                border-radius: 5px;
                padding: 20px;
                margin-bottom: 20px;
            }}
            .css-1v0mbdj {{
                margin-bottom: 20px;
            }}
            .reportview-container .main .block-container {{
                padding-top: 2rem;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                gap: 5px;
            }}
            .stTabs [data-baseweb="tab"] {{
                background-color: {COLOR_SECUNDARIO};
                color: white;
                padding: 10px 20px;
                border-radius: 5px 5px 0 0;
                margin-right: 5px;
            }}
            .stTabs [aria-selected="true"] {{
                background-color: {COLOR_PRIMARIO};
                color: white;
            }}
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
                color: {COLOR_PRIMARIO};
            }}
            .success-message {{
                background-color: #d4edda;
                color: #155724;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
            .error-message {{
                background-color: #f8d7da;
                color: #721c24;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
        </style>
    """, unsafe_allow_html=True)

# Función para mostrar frases de motivación y sugerencias
def mostrar_motivacion_y_sugerencia():
    with st.container():
        st.markdown(f"""
        <div style='background-color:{COLOR_PRIMARIO}; color:white; padding:10px; border-radius:5px; margin:10px 0;'>
            <h4 style='color:white;'>📜 Frase de Motivación</h4>
            <p>{MOTIVACIONES[len(st.session_state) % len(MOTIVACIONES)]}</p>
        </div>
        <div style='background-color:{COLOR_SECUNDARIO}; color:white; padding:10px; border-radius:5px; margin:10px 0;'>
            <h4 style='color:white;'>🎯 Sugerencia de Educación Financiera</h4>
            <p>{SUGERENCIAS_EDUCACION[len(st.session_state) % len(SUGERENCIAS_EDUCACION)]}</p>
        </div>
        """, unsafe_allow_html=True)

# Validaciones mejoradas
def validar_email(email):
    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

def validar_telefono(telefono):
    return bool(re.match(r"^\+?[0-9]{10,15}$", telefono))

def validar_nombre(nombre):
    return bool(re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,50}$", nombre))

def validar_edad(edad):
    return 0 <= edad <= 120

# Funciones para cada sección (registro, situación financiera, etc.) con validaciones mejoradas
def registrar_usuario():
    with st.form("registro_form"):
        st.subheader("Registro de Usuario")
        nombre = st.text_input("Nombre completo*", max_chars=50, 
                              help="Ingrese su nombre completo (solo letras y espacios)")
        edad = st.number_input("Edad*", min_value=0, max_value=120, 
                             help="Ingrese su edad entre 0 y 120 años")
        email = st.text_input("Email*", max_chars=100, 
                            help="Ingrese un email válido (ejemplo@dominio.com)")
        telefono = st.text_input("Teléfono*", max_chars=15, 
                               help="Ingrese un número de teléfono válido (10-15 dígitos, con o sin +)")
        
        if st.form_submit_button("Registrar"):
            errores = []
            if not validar_nombre(nombre):
                errores.append("El nombre debe contener solo letras y espacios (2-50 caracteres)")
            if not validar_edad(edad):
                errores.append("La edad debe estar entre 0 y 120 años")
            if not validar_email(email):
                errores.append("Por favor, ingresa un correo electrónico válido")
            if not validar_telefono(telefono):
                errores.append("Por favor, ingresa un número de teléfono válido (10-15 dígitos)")
            
            if errores:
                for error in errores:
                    st.error(error)
            else:
                st.session_state['usuario'] = {
                    "nombre": nombre, 
                    "edad": edad, 
                    "email": email, 
                    "telefono": telefono
                }
                st.success("Usuario registrado con éxito.")
                mostrar_motivacion_y_sugerencia()
                st.session_state['current_tab'] = "Situación Financiera"

def evaluar_situacion_financiera():
    with st.form("finanzas_form"):
        st.subheader("Situación Financiera")
        st.write("Ingresa tus datos financieros en dólares ($):")
        
        col1, col2 = st.columns(2)
        with col1:
            activos = st.number_input("Activos totales* (efectivo, inversiones, propiedades, etc.):", 
                                    min_value=0.0, step=100.0)
        with col2:
            pasivos = st.number_input("Pasivos totales* (deudas, préstamos, hipotecas, etc.):", 
                                    min_value=0.0, step=100.0)
        
        col3, col4 = st.columns(2)
        with col3:
            ingresos_mensuales = st.number_input("Ingresos mensuales*:", min_value=0.0, step=100.0)
        with col4:
            gastos_mensuales = st.number_input("Gastos mensuales*:", min_value=0.0, step=100.0)
        
        if st.form_submit_button("Evaluar situación financiera"):
            if not all([activos >= 0, pasivos >= 0, ingresos_mensuales >= 0, gastos_mensuales >= 0]):
                st.error("Todos los valores deben ser números positivos")
            else:
                patrimonio_neto = activos - pasivos
                flujo_efectivo_mensual = ingresos_mensuales - gastos_mensuales
                
                st.session_state['situacion_financiera'] = {
                    "activos": activos, 
                    "pasivos": pasivos, 
                    "ingresos_mensuales": ingresos_mensuales, 
                    "gastos_mensuales": gastos_mensuales,
                    "patrimonio_neto": patrimonio_neto,
                    "flujo_efectivo": flujo_efectivo_mensual
                }
                
                with st.expander("Ver resultados"):
                    st.metric("Patrimonio Neto", f"${patrimonio_neto:,.2f}")
                    st.metric("Flujo de Efectivo Mensual", f"${flujo_efectivo_mensual:,.2f}")
                
                mostrar_motivacion_y_sugerencia()
                st.session_state['current_tab'] = "Plan de Inversión"

# ... (continuar con las demás funciones adaptadas al mismo estilo)

def main():
    # Aplicar estilos personalizados
    aplicar_estilos()
    
    # Mostrar logo
    logo = cargar_imagen()
    if logo:
        st.image(logo, width=150)
    
    # Título principal
    st.markdown(f"<h1 style='color:{COLOR_PRIMARIO};'>Bot de Finanzas Personales</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:{COLOR_SECUNDARIO};'>por Carlos Devis</h2>", unsafe_allow_html=True)
    
    # Inicializar estado de la sesión
    if 'current_tab' not in st.session_state:
        st.session_state['current_tab'] = "Registro"
    
    # Navegación por pestañas
    tabs = ["Registro", "Situación Financiera", "Plan de Inversión", "Proyección de Retiro", "Resumen"]
    current_tab = st.session_state['current_tab']
    
    # Mostrar contenido según la pestaña actual
    if current_tab == "Registro":
        registrar_usuario()
    elif current_tab == "Situación Financiera":
        evaluar_situacion_financiera()
    elif current_tab == "Plan de Inversión":
        evaluar_plan_inversion()
    elif current_tab == "Proyección de Retiro":
        evaluar_proyeccion_retiro()
    elif current_tab == "Resumen":
        mostrar_resumen()

if __name__ == "__main__":
    main()