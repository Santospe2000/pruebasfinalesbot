from openai import OpenAI
import sqlite3
import matplotlib.pyplot as plt

# Configurar el cliente de OpenAI
client = OpenAI(
    api_key='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',  # Reemplaza con tu clave válida
    organization='org-FlkEgjV4NFCjXGnaLOIIRQsM',
    project='proj_YNJ20BfkFT5XSm7oXnxEEdD8',
)

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
        print("Gracias por tu interés, pero debes ser mayor de 18 años para usar este programa.")
        return
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

# Solicitar datos financieros al usuario
def solicitar_datos_financieros(usuario_id):
    try:
        ingresos_mensuales = float(input("Ingresos Mensuales: "))
        gastos_mensuales = float(input("Gastos Mensuales: "))
        activos_totales = float(input("Activos Totales: "))
        pasivos_totales = float(input("Pasivos Totales: "))
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO finanzas (usuario_id, ingresos_mensuales, gastos_mensuales, activos_totales, pasivos_totales)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, ingresos_mensuales, gastos_mensuales, activos_totales, pasivos_totales))
        conn.commit()
        conn.close()
        return ingresos_mensuales, gastos_mensuales, activos_totales, pasivos_totales
    except ValueError:
        print("Por favor, ingresa valores numéricos válidos.")
        return solicitar_datos_financieros(usuario_id)

# Calcular y mostrar el análisis financiero
def analizar_situacion_financiera(ingresos, gastos, activos, pasivos):
    flujo_caja_mensual = ingresos - gastos
    patrimonio_neto = activos - pasivos
    print(f"Análisis Resumen de tu Situación Financiera Actual")
    print(f"Ingresos Mensuales: ${ingresos}")
    print(f"Gastos Mensuales: ${gastos}")
    print(f"Flujo de Caja Mensual: ${flujo_caja_mensual} (Ingresos - Gastos)")
    print(f"Activos Totales: ${activos}")
    print(f"Pasivos Totales: ${pasivos}")
    print(f"Patrimonio Neto: ${patrimonio_neto} (Activos - Pasivos)")
    print("Análisis:")
    if flujo_caja_mensual > 0:
        print(f"Tienes un flujo de caja mensual positivo de ${flujo_caja_mensual}, lo cual indica que estás generando más ingresos de los que gastas.")
    else:
        print(f"Tienes un flujo de caja mensual negativo de ${flujo_caja_mensual}, lo cual indica que estás gastando más de lo que generas.")
    if patrimonio_neto > 0:
        print("Tu patrimonio neto es sólido, lo que sugiere una buena salud financiera en general.")
    else:
        print("Tu patrimonio neto es negativo, lo que sugiere que tienes más deudas que activos.")
    print("Acciones a Tomar:")
    print("Maximiza tu flujo de caja: Considera aumentar tus ingresos (si es posible) o reducir tus gastos para generar un mayor flujo de caja mensual.")
    print("Diversifica tus inversiones: Aunque tienes un buen patrimonio neto, asegúrate de que tus inversiones estén diversificadas en diferentes clases de activos para reducir el riesgo.")

# Solicitar datos del plan de inversión
def solicitar_plan_inversion():
    objetivos_financieros = input("Objetivos financieros (corto, mediano, largo plazo) Ejemplo Pagar Universidad: ")
    horizonte_inversion = input("Horizonte de inversión Tiempo que planeas mantener las inversiones. Meses : ")
    preferencias_inversion = input("Preferencias de inversión (acciones, bonos, bienes raíces, etc.): ")
    return objetivos_financieros, horizonte_inversion, preferencias_inversion

# Analizar y mostrar el plan de inversión
def analizar_plan_inversion(objetivos, horizonte, preferencias):
    print(f"Análisis Resumen de tu Plan de Inversión")
    print(f"Horizonte de Inversión: {horizonte}")
    print(f"Preferencias de Inversión: {preferencias}")
    print("Análisis:")
    if horizonte.lower() == "corto plazo":
        print("Tu horizonte de inversión es a corto plazo, lo cual limita las opciones de inversión más riesgosas.")
    if "bienes raíces" in preferencias.lower():
        print("Tu preferencia por bienes raíces sugiere un enfoque en inversiones tangibles y posiblemente generadoras de ingresos (rentas).")
    print("Acciones a Tomar:")
    print("Considera otras opciones de inversión: Dado tu horizonte de inversión a corto plazo, explora opciones de inversión líquidas y de bajo riesgo, como fondos de inversión de renta fija o depósitos a plazo.")
    print("Investiga a fondo el mercado inmobiliario: Antes de invertir en bienes raíces, investiga a fondo el mercado, las tendencias y los posibles riesgos y rendimientos.")

# Solicitar datos de proyección de retiro
def solicitar_proyeccion_retiro():
    try:
        edad_retiro = int(input("Edad de retiro deseada: "))
        ingresos_retiro = float(input("Ingresos esperados durante el retiro anual: "))
        gastos_retiro = float(input("Gastos esperados durante el retiro anual: "))
        ahorros_retiro = float(input("Ahorros actuales para el retiro: "))
        return edad_retiro, ingresos_retiro, gastos_retiro, ahorros_retiro
    except ValueError:
        print("Por favor, ingresa valores numéricos válidos.")
        return solicitar_proyeccion_retiro()

# Analizar y mostrar la proyección de retiro
def analizar_proyeccion_retiro(edad, ingresos, gastos, ahorros):
    print(f"Análisis Resumen de tu Proyección de Retiro")
    print(f"Edad de Retiro Deseada: {edad}")
    print(f"Ingresos Esperados Durante el Retiro: ${ingresos} anuales")
    print(f"Gastos Esperados Durante el Retiro: ${gastos} anuales (${gastos / 12} mensuales)")
    print(f"Ahorros Actuales para el Retiro: ${ahorros}")
    print("Análisis:")
    if edad < 60:
        print("Tu edad de retiro deseada es relativamente temprana, lo cual requiere una planificación sólida y un ahorro considerable.")
    if ingresos > gastos:
        print("Tus ingresos esperados durante el retiro parecen ser suficientes para cubrir tus gastos estimados, pero es importante considerar la inflación y otros factores.")
    if ahorros < ingresos * 10:
        print("Tus ahorros actuales para el retiro son bajos en comparación con tus ingresos y gastos esperados durante la jubilación.")
    print("Acciones a Tomar:")
    print("Aumenta tus ahorros para el retiro: Considera aumentar significativamente tus contribuciones a tus fondos de pensiones, cuentas de retiro e inversiones.")
    print("Revisa tus gastos de jubilación: Asegúrate de que tus gastos estimados para la jubilación sean realistas y consideren posibles gastos inesperados o cambios en tu estilo de vida.")
    print("Considera trabajar a tiempo parcial durante la jubilación: Si es necesario, considera la posibilidad de trabajar a tiempo parcial durante la jubilación para complementar tus ingresos.")

# Función para generar un análisis profundo utilizando OpenAI
def generar_analisis_profundo(ingresos, gastos, activos, pasivos, objetivos, horizonte, preferencias):
    prompt = f"""
    El usuario tiene los siguientes datos financieros:
    - Ingresos Mensuales: ${ingresos}
    - Gastos Mensuales: ${gastos}
    - Activos Totales: ${activos}
    - Pasivos Totales: ${pasivos}
    - Objetivos Financieros: {objetivos}
    - Horizonte de Inversión: {horizonte}
    - Preferencias de Inversión: {preferencias}

    Basado en estos datos, realiza un análisis profundo y resumido del perfil de inversión del usuario. Además, proporciona sugerencias paso a paso para mejorar su perfil de inversionista, considerando los siguientes criterios:
    1. Las finanzas personales son la base de todo. Si gastas todo o más de lo que ganas, nunca lograrás tu libertad financiera.
    2. No importa lo mucho que trabajes, si no organizas tus finanzas personales nunca podrás ser independiente financieramente.
    3. Aumentar los gastos en pequeñas cantidades puede llevar a una crisis financiera.
    4. La importancia de ahorrar y no depender de deudas para mantener un estilo de vida.
    5. La necesidad de diversificar las inversiones y no poner todos los huevos en la misma canasta.
    6. La importancia de tener un plan de inversión claro y realista.

    Por favor, proporciona un análisis detallado y sugerencias concretas para mejorar el perfil de inversión del usuario.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Cambiado a gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "Eres un experto en finanzas personales y planificación de inversiones."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

# Función principal
def main():
    crear_base_datos()
    nombre = input("Nombre: ")
    edad = int(input("Edad: "))
    email = input("Email: ")
    telefono = input("Teléfono: ")
    usuario_id = registrar_usuario(nombre, edad, email, telefono)
    respuesta = input("¿Deseas evaluar tu situación financiera? (si/no): ").lower()
    if respuesta == 'si':
        ingresos, gastos, activos, pasivos = solicitar_datos_financieros(usuario_id)
        analizar_situacion_financiera(ingresos, gastos, activos, pasivos)
        plan_respuesta = input("¿Deseas evaluar tu plan de inversión? (si/no): ").lower()
        if plan_respuesta == 'si':
            objetivos, horizonte, preferencias = solicitar_plan_inversion()
            analizar_plan_inversion(objetivos, horizonte, preferencias)
            # Generar análisis profundo con OpenAI
            analisis_profundo = generar_analisis_profundo(ingresos, gastos, activos, pasivos, objetivos, horizonte, preferencias)
            print("\nAnálisis Profundo y Sugerencias:")
            print(analisis_profundo)
        retiro_respuesta = input("¿Deseas evaluar tu proyección de retiro? (si/no): ").lower()
        if retiro_respuesta == 'si':
            edad, ingresos_retiro, gastos_retiro, ahorros_retiro = solicitar_proyeccion_retiro()
            analizar_proyeccion_retiro(edad, ingresos_retiro, gastos_retiro, ahorros_retiro)
    else:
        print("Gracias por usar el programa.")
    print("Por favor, descarga tu reporte y finaliza la calculadora para volver a empezar.")

if __name__ == "__main__":
    main()