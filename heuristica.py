import os
import re
from bs4 import BeautifulSoup

# Limpiar el HTML (incluso si el archivo no tiene extensión HTML)
def limpiar_html(texto_html):
    soup = BeautifulSoup(texto_html, 'html.parser')
    return soup.get_text(separator=" ").strip()

# Expresiones regulares ampliadas
direccion_regex = r'((?:Calle|Carrera|Avenida|Av\.|Blvd|Boulevard|Boulevar)\s+[^\n]*?\d+[-\d]*[^•\n]*?\s*,\s*(?:Colonia|Fraccionamiento|Unidad\sHabitacional|Barrio|Zona)\s+[^\n]*?\s*,\s*C[\.P\.]?\s*\d{5}\s*,\s*(?:Municipio|Delegación|Localidad)\s+[^\n]*?\s*,\s*(?:Estado|Provincia)\s+[^\n]*?,\s*(México))'
rfc_regex = r'\b([A-ZÑ&]{3,4}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\w{3})\b'
correos_regex = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?:com|net|org|edu|gov|mx|biz|info|tv|me|io|[a-zA-Z]{2,})\b'
telefonos_regex = r'\b(?:\(?\+?\d{1,3}\)?\s*\d{1,4}[-.\s]?\d{2,4}[-.\s]?\d{4}|\d{10,11})\b'
codigo_postal_regex = r'\b(?:C\.?P\.?\s*)?\d{5}\b'
metodo_pago_regex = r'\b(Tarjeta(?:\sde\sCrédito|\sde\sDébito)?|Crédito|Débito|Transferencia|Efectivo|Pago|PSE|Banca en Línea|PayPal|MercadoPago|Oxxo\sPay|SPEI|OpenPay|Stripe|QR)\b'
paqueteria_regex = r'\b(DHL|FedEx|UPS|Estafeta|Redpack|Correos\sde\sMéxico|Sendex|Paquetexpress|Tresguerras|Mensajería|Paquetería|Envíos|Entrega)\b'
region_regex = r'\b(Ciudad\sde\sMéxico|Monterrey|Guadalajara|Puebla|Querétaro|Estado\sde\sMéxico|Jalisco|Nuevo\sLeón|Tijuana|Mérida|León|Hermosillo|Culiacán|Cancún|Acapulco|Chihuahua|Toluca|Ciudad\sJuárez|Mexicali)\b'

# Palabras clave adicionales para ampliar el alcance
palabras_clave = {
    "dirección": ["dirección", "ubicación", "lugar", "domicilio", "residencia", "esquina", "frente a", "entre", direccion_regex],
    "teléfono": ["teléfono", "tel.", "número", "número de contacto", "contacto telefónico", "móvil", "celular", telefonos_regex],
    "RFC": ["RFC", "registro federal de contribuyentes", "clave fiscal", rfc_regex],
    "email": ["email", "correo", "correo electrónico", "e-mail", "dirección de correo", correos_regex],
    "método de pago": ["método de pago", "forma de pago", "pago", "pagos", "tarjeta", "transferencia", metodo_pago_regex],
    "paquetería": ["paquetería", "mensajería", "envío", "transporte", "entrega", "servicio de paquetería", paqueteria_regex],
    "código postal": ["código postal", "CP", "código ZIP", codigo_postal_regex],
    "ciudad": ["ciudad", "localidad", "municipio", "región", region_regex]
}


# Función para verificar si un archivo es útil basado en palabras clave y expresiones regulares
def es_util(texto):
    contador_palabras_clave = {key: 0 for key in palabras_clave}
    
    for clave, sinonimos in palabras_clave.items():
        for sinonimo in sinonimos:
            if isinstance(sinonimo, str):
                if re.search(sinonimo, texto, re.IGNORECASE):
                    contador_palabras_clave[clave] += 1
            elif re.search(sinonimo, texto, re.IGNORECASE):  # Para los patrones regex
                contador_palabras_clave[clave] += 1
    
    # Contar si hay suficientes coincidencias para cada categoría
    coincidencias_totales = sum(contador_palabras_clave.values())
    es_util = coincidencias_totales >= 3  # Umbral de coincidencias para considerarlo útil
    return es_util

# Función para procesar los archivos y verificar si son útiles
def process_directory(directory):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Leer el archivo y limpiar el contenido HTML (aunque no tenga la extensión HTML)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                cleaned_content = limpiar_html(content)
                
                # Verificar si es útil
                if es_util(cleaned_content):
                    print(f"El archivo '{filename}' contiene información útil.")
                else:
                    print(f"El archivo '{filename}' NO contiene información útil.")

# Llamar a la función para procesar el directorio(colocar la ruta de tu carpeta que contiene los archivos)
process_directory('C:/Users/Sam/Downloads/INEGI_muestra_scraping/muestra/www.mochila.org.mx')
