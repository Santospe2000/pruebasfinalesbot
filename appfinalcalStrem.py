import streamlit as st
from openai import OpenAI
import sqlite3
import matplotlib.pyplot as plt

# Configurar el cliente de OpenAI
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    organization=st.secrets["OPENAI_ORG"],
    project=st.secrets["OPENAI_PROJECT"],
)

# Configuración inicial de la página
st.set_page_config(page_title="Calculadora Financiera", page_icon="💰", layout="wide")

# Crear la base de datos y la tabla de usuarios
def crear_base_datos():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            edad INTEGER,
            email TEXT,
            telefono TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finanzas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            ingresos_mensuales REAL,
            gastos_mensuales REAL,
            activos_totales REAL,
            pasivos_totales REAL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

# Registrar un nuevo usuario
def registrar_usuario(nombre, edad, email, telefono):
    if edad < 18:
        st.warning("Debes ser mayor de 18 años para usar este programa.")
        return None
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nombre, edad, email, telefono)
        VALUES (?, ?, ?, ?)
    ''', (nombre, edad, email, telefono))
    usuario_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return usuario_id

# Calcular y mostrar el análisis financiero
def analizar_situacion_financiera(ingresos, gastos, activos, pasivos):
    flujo_caja_mensual = ingresos - gastos
    patrimonio_neto = activos - pasivos
    
    st.subheader("Análisis Resumen de tu Situación Financiera Actual")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Ingresos Mensuales", f"${ingresos:,.2f}")
        st.metric("Gastos Mensuales", f"${gastos:,.2f}")
        st.metric("Flujo de Caja Mensual", f"${flujo_caja_mensual:,.2f}", 
                 delta="Positivo" if flujo_caja_mensual > 0 else "Negativo")
    
    with col2:
        st.metric("Activos Totales", f"${activos:,.2f}")
        st.metric("Pasivos Totales", f"${pasivos:,.2f}")
        st.metric("Patrimonio Neto", f"${patrimonio_neto:,.2f}", 
                 delta="Positivo" if patrimonio_neto > 0 else "Negativo")
    
    st.subheader("Análisis")
    if flujo_caja_mensual > 0:
        st.success(f"Tienes un flujo de caja mensual positivo de ${flujo_caja_mensual:,.2f}, lo cual indica que estás generando más ingresos de los que gastas.")
    else:
        st.error(f"Tienes un flujo de caja mensual negativo de ${flujo_caja_mensual:,.2f}, lo cual indica que estás gastando más de lo que generas.")
    
    if patrimonio_neto > 0:
        st.success("Tu patrimonio neto es sólido, lo que sugiere una buena salud financiera en general.")
    else:
        st.error("Tu patrimonio neto es negativo, lo que sugiere que tienes más deudas que activos.")
    
    with st.expander("Acciones Recomendadas"):
        st.write("""
        1. **Maximiza tu flujo de caja**: Considera aumentar tus ingresos o reducir gastos
        2. **Diversifica tus inversiones**: Distribuye tus activos para reducir riesgos
        3. **Crea un presupuesto detallado**: Identifica todos tus gastos
        4. **Establece metas claras**: Define objetivos a corto, mediano y largo plazo
        """)

# Generar plan de trabajo financiero con OpenAI
def generar_plan_trabajo(ingresos, gastos, activos, pasivos):
    prompt = f"""
    Como experto en finanzas personales, analiza la situación financiera con estos datos:
    - Ingresos: ${ingresos}/mes
    - Gastos: ${gastos}/mes
    - Activos: ${activos}
    - Pasivos: ${pasivos}
    
    Crea un plan detallado que incluya:
    1. Diagnóstico claro de la situación actual
    2. Estrategias para mejorar el flujo de caja
    3. Plan de reducción de deudas (si aplica)
    4. Recomendaciones de inversión personalizadas
    5. Metas a corto (3 meses), mediano (1 año) y largo plazo (5+ años)
    6. Ejercicios prácticos para implementar el plan
    
    Usa un lenguaje claro y motivador, con ejemplos concretos.
    """
    
    with st.spinner('Generando tu plan personalizado...'):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asesor financiero experto que ayuda a personas a mejorar sus finanzas personales."},
                {"role": "user", "content": prompt}
            ]
        )
    
    return response.choices[0].message.content

# Analizar y mostrar el plan de inversión
def analizar_plan_inversion(objetivos, horizonte, preferencias):
    st.subheader("Análisis de tu Plan de Inversión")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Objetivos", objetivos)
    col2.metric("Horizonte", horizonte)
    col3.metric("Preferencias", preferencias)
    
    with st.expander("Análisis Detallado"):
        if "corto plazo" in horizonte.lower():
            st.write("""
            - **Horizonte corto**: Considera inversiones líquidas y de bajo riesgo
            - **Opciones recomendadas**: Fondos del mercado monetario, certificados de depósito
            """)
        else:
            st.write("""
            - **Horizonte largo**: Puedes considerar inversiones con mayor potencial de crecimiento
            - **Opciones recomendadas**: Índices bursátiles, bienes raíces, fondos de inversión
            """)
        
        if "bienes raíces" in preferencias.lower():
            st.write("""
            - **Bienes raíces**: Excelente para generar ingresos pasivos
            - **Recomendación**: Investiga el mercado local y considera propiedades en zonas con crecimiento
            """)

# Analizar y mostrar la proyección de retiro
def analizar_proyeccion_retiro(edad_actual, edad_retiro, ingresos_retiro, gastos_retiro, ahorros_retiro):
    años_para_retiro = edad_retiro - edad_actual
    necesidad_total = gastos_retiro * 25  # Regla del 4%
    ahorro_necesario_anual = (necesidad_total - ahorros_retiro) / años_para_retiro if años_para_retiro > 0 else 0
    
    st.subheader("Proyección de Retiro")
    
    cols = st.columns(2)
    cols[0].metric("Edad Actual", edad_actual)
    cols[1].metric("Edad de Retiro", edad_retiro, f"En {años_para_retiro} años")
    
    cols = st.columns(3)
    cols[0].metric("Ingresos Anuales", f"${ingresos_retiro:,.2f}")
    cols[1].metric("Gastos Anuales", f"${gastos_retiro:,.2f}")
    cols[2].metric("Ahorros Actuales", f"${ahorros_retiro:,.2f}")
    
    st.progress(min(ahorros_retiro/necesidad_total, 1.0), text="Progreso hacia tu meta de retiro")
    
    with st.expander("Análisis Detallado"):
        st.metric("Necesidad total estimada (regla del 4%)", f"${necesidad_total:,.2f}")
        st.metric("Ahorro anual necesario", f"${ahorro_necesario_anual:,.2f}")
        
        if ahorros_retiro < necesidad_total * 0.1:
            st.error("Tus ahorros actuales son insuficientes para tu retiro. Necesitas aumentar tus contribuciones.")
        
        st.write("""
        **Acciones recomendadas:**
        1. Aumenta tus contribuciones a cuentas de retiro
        2. Considera inversiones que generen ingresos pasivos
        3. Revisa tu asignación de activos periódicamente
        """)

# Función para generar un análisis profundo utilizando OpenAI
def generar_analisis_profundo(ingresos, gastos, activos, pasivos, objetivos, horizonte, preferencias):
    prompt = f"""
    Como experto en finanzas personales y bienes raíces, analiza esta situación:
    
    **Datos financieros:**
    - Ingresos: ${ingresos}/mes
    - Gastos: ${gastos}/mes
    - Activos: ${activos}
    - Pasivos: ${pasivos}
    - Objetivos: {objetivos}
    - Horizonte: {horizonte}
    - Preferencias: {preferencias}

    Realiza un análisis que incluya:
    1. Diagnóstico financiero completo
    2. Estrategias para optimizar ingresos/gastos
    3. Plan de inversión personalizado
    4. Casos prácticos aplicables
    5. Ejercicios y pasos accionables

    Usa analogías financieras y un estilo motivador pero realista.
    """
    
    with st.spinner('Generando análisis profundo con IA...'):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un analista financiero especializado en finanzas personales y bienes raíces. Proporciona consejos prácticos y personalizados."},
                {"role": "user", "content": prompt}
            ]
        )
    
    return response.choices[0].message.content

# Interfaz principal de Streamlit
def main():
    st.title("💰 Calculadora Financiera Personalizada")
    st.markdown("""
    Esta herramienta te ayudará a analizar tu situación financiera actual, crear un plan de acción 
    y establecer metas claras para tu futuro económico.
    """)
    
    # Paso 1: Registro de usuario
    with st.expander("📝 Información Personal", expanded=True):
        st.subheader("Datos Personales")
        nombre = st.text_input("Nombre completo")
        edad = st.number_input("Edad", min_value=18, max_value=100, value=30)
        email = st.text_input("Email")
        telefono = st.text_input("Teléfono")
        
        if st.button("Guardar información personal"):
            if nombre and email:
                usuario_id = registrar_usuario(nombre, edad, email, telefono)
                st.session_state['usuario_id'] = usuario_id
                st.success("Información guardada correctamente")
            else:
                st.warning("Por favor completa todos los campos obligatorios")
    
    # Paso 2: Datos financieros
    if 'usuario_id' in st.session_state:
        with st.expander("💵 Situación Financiera Actual", expanded=True):
            st.subheader("Ingresa tus datos financieros")
            
            col1, col2 = st.columns(2)
            ingresos = col1.number_input("Ingresos Mensuales ($)", min_value=0.0, value=3000.0, step=100.0)
            gastos = col1.number_input("Gastos Mensuales ($)", min_value=0.0, value=2500.0, step=100.0)
            activos = col2.number_input("Activos Totales ($)", min_value=0.0, value=50000.0, step=1000.0)
            pasivos = col2.number_input("Pasivos Totales ($)", min_value=0.0, value=20000.0, step=1000.0)
            
            if st.button("Analizar mi situación financiera"):
                st.session_state['datos_financieros'] = (ingresos, gastos, activos, pasivos)
                analizar_situacion_financiera(ingresos, gastos, activos, pasivos)
                
                # Generar y mostrar plan de trabajo
                plan = generar_plan_trabajo(ingresos, gastos, activos, pasivos)
                with st.expander("📝 Plan de Trabajo Financiero Personalizado", expanded=True):
                    st.write(plan)
    
    # Paso 3: Plan de inversión
    if 'datos_financieros' in st.session_state:
        with st.expander("📈 Plan de Inversión"):
            st.subheader("Configura tu estrategia de inversión")
            
            objetivos = st.text_input("Objetivos financieros (ej: comprar casa, retiro temprano)", 
                                    "Crear fuentes de ingreso pasivo")
            horizonte = st.selectbox("Horizonte de inversión", 
                                   ["Corto plazo (1-3 años)", "Mediano plazo (3-5 años)", "Largo plazo (5+ años)"])
            preferencias = st.multiselect("Preferencias de inversión", 
                                        ["Bienes raíces", "Acciones", "Bonos", "Fondos", "Criptomonedas", "Negocios"])
            
            if st.button("Analizar plan de inversión"):
                st.session_state['plan_inversion'] = (objetivos, horizonte, ", ".join(preferencias))
                analizar_plan_inversion(objetivos, horizonte, ", ".join(preferencias))
                
                # Análisis profundo con IA
                ingresos, gastos, activos, pasivos = st.session_state['datos_financieros']
                analisis = generar_analisis_profundo(ingresos, gastos, activos, pasivos, objetivos, horizonte, ", ".join(preferencias))
                
                with st.expander("🧠 Análisis Profundo con Inteligencia Artificial", expanded=True):
                    st.write(analisis)
    
    # Paso 4: Proyección de retiro
    if 'datos_financieros' in st.session_state:
        with st.expander("👵 Proyección de Retiro"):
            st.subheader("Planificación para tu jubilación")
            
            col1, col2 = st.columns(2)
            edad_actual = col1.number_input("Tu edad actual", min_value=18, max_value=100, value=30)
            edad_retiro = col2.number_input("Edad de retiro deseada", min_value=edad_actual+1, max_value=100, value=65)
            
            ingresos_retiro = st.number_input("Ingresos anuales esperados durante el retiro ($)", 
                                            min_value=0.0, value=40000.0, step=1000.0)
            gastos_retiro = st.number_input("Gastos anuales esperados durante el retiro ($)", 
                                          min_value=0.0, value=30000.0, step=1000.0)
            ahorros_retiro = st.number_input("Ahorros actuales para el retiro ($)", 
                                           min_value=0.0, value=10000.0, step=1000.0)
            
            if st.button("Calcular proyección de retiro"):
                analizar_proyeccion_retiro(edad_actual, edad_retiro, ingresos_retiro, gastos_retiro, ahorros_retiro)
    
    # Pie de página
    st.markdown("---")
    st.markdown("""
    ### 📌 Recomendaciones Finales
    - Revisa periódicamente tu situación financiera
    - Implementa los cambios de manera consistente
    - Considera asesoría profesional para estrategias avanzadas
    """)

if __name__ == "__main__":
    crear_base_datos()
    main()