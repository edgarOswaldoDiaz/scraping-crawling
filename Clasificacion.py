
import os
import re
import hashlib
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Limpiar el HTML (incluso si el archivo no tiene extensión HTML)
def limpiar_html(texto_html):
    soup = BeautifulSoup(texto_html, 'lxml')
    return soup.get_text(separator=" ").strip()

# Expresiones regulares ampliadas
direccion_regex = r'(?:Calle|Carrera|Avenida|Av\.|Blvd|Boulevard|Boulevar|Carretera|Camino)\s+[^\n,]*\d+[^\n,]*\s*,?\s*(?:Colonia|Fraccionamiento|Unidad\sHabitacional|Barrio|Zona|Sector|Residencial)\s+[^\n,]*\s*,?\s*(?:C\.?P\.?\s*)?\d{5}\s*,?\s*(?:Municipio|Delegación|Localidad|Colonia|Ciudad)\s+[^\n,]*\s*,?\s*(?:Estado|Provincia|Entidad|Región)\s+[^\n,]*,\s*(México)'
rfc_regex = r'\b([A-ZÑ&]{3,4}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[A-Z\d]{2}[A\d])\b'
correos_regex = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
telefonos_regex = r'\b(?:\+?52\s?)?(?:\(?\d{2,3}\)?[-.\s]?\d{4}[-.\s]?\d{4}|\d{10,11})\b'
codigo_postal_regex = r'\b(?:C\.?P\.?\s*)?\d{5}\b'
metodo_pago_regex = r'\b(Tarjeta(?:\sde\s(Crédito|Débito))?|Crédito|Débito|Transferencia|Efectivo|Pago|PSE|Banca\sEn\sLínea|PayPal|MercadoPago|Oxxo\sPay|SPEI|OpenPay|Stripe|QR)\b'
paqueteria_regex = r'\b(DHL|FedEx|UPS|Estafeta|Redpack|Correos\sde\sMéxico|Sendex|Paquetexpress|Tresguerras|Mensajería|Paquetería|Envíos|Entrega)\b'
region_regex = r'\b(Ciudad\sde\sMéxico|Monterrey|Guadalajara|Puebla|Querétaro|Estado\sde\sMéxico|Jalisco|Nuevo\sLeón|Tijuana|Mérida|León|Hermosillo|Culiacán|Cancún|Acapulco|Chihuahua|Toluca|Ciudad\sJuárez|Mexicali)\b'

# Unificar todas las expresiones regulares y palabras clave en una sola lista
patrones_busqueda = [
    direccion_regex, rfc_regex, correos_regex, telefonos_regex, 
    codigo_postal_regex, metodo_pago_regex, paqueteria_regex, region_regex
]

# Palabras clave adicionales
palabras_clave = [
    # Español
    "dirección", "ubicación", "lugar", "domicilio", "residencia", "esquina", "frente a", "entre", "intersección", "Cda.", "Fracc.",
    "teléfono", "tel.", "número", "número de contacto", "contacto telefónico", "móvil", "celular", "Tel. móvil", "número de móvil",
    "RFC", "registro federal de contribuyentes", "clave fiscal", "cédula fiscal",
    "email", "correo", "correo electrónico", "e-mail", "dirección de correo", "dirección de e-mail",
    "método de pago", "forma de pago", "pago", "pagos", "tarjeta", "transferencia", "crédito", "débito", "efectivo", "pagaré", "depósito",
    "paquetería", "mensajería", "envío", "transporte", "entrega", "servicio de paquetería", "Courier", "logística", "carrier",
    "código postal", "CP", "código ZIP", "código postal ZIP", 
    "ciudad", "localidad", "municipio", "región",
    
    # Inglés
    "address", "location", "place", "domicile", "residence", "corner", "in front of", "between", "intersection", "crossing",
    "phone", "telephone", "contact number", "mobile", "cell", "mobile phone", 
    "tax ID", "fiscal code", "business tax ID", 
    "payment method", "form of payment", "payment", "payments", "card", "transfer", "cash", "wire transfer", "debit", "credit",
    "courier", "shipping", "delivery", "messaging service", "logistics", 
    "ZIP code", "postal code", "postal ZIP code", 
    "city", "locality", "municipality", "region"
]


# Umbral de coincidencias mínimo para considerar el archivo útil
UMBRAL_COINCIDENCIAS = 3

# Función para verificar si un archivo es útil basado en palabras clave y expresiones regulares
def es_util(texto):
    coincidencias = 0

    # Verificar por palabras clave
    for palabra in palabras_clave:
        if re.search(palabra, texto, re.IGNORECASE):
            coincidencias += 1
        if coincidencias >= UMBRAL_COINCIDENCIAS:
            return True

    # Verificar con expresiones regulares
    for patron in patrones_busqueda:
        if re.search(patron, texto, re.IGNORECASE):
            coincidencias += 1
        if coincidencias >= UMBRAL_COINCIDENCIAS:
            return True

    return False

# Función para calcular el hash MD5 del contenido
def calcular_hash(texto):
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

# Función para calcular la similitud de archivos utilizando Cosine Similarity
def calcular_similitud(texto1, texto2):
    vectorizer = TfidfVectorizer().fit_transform([texto1, texto2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]

# Función para procesar los archivos y verificar si son útiles o duplicados
def process_directory(directory, umbral_similitud=0.7):
    hash_dict = {}  # Para guardar hashes únicos de archivos útiles
    archivos_similares = {}  # Para detectar archivos similares

    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Leer el archivo y limpiar el contenido HTML
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                cleaned_content = limpiar_html(content)

                # Verificar si es útil
                if es_util(cleaned_content):
                    # Calcular hash del contenido
                    hash_val = calcular_hash(cleaned_content)

                    # Detectar si el archivo es un duplicado exacto
                    if hash_val in hash_dict:
                        print(f"El archivo '{filename}' es un duplicado exacto de '{hash_dict[hash_val]}'.")
                    else:
                        # Comprobar si hay archivos similares
                        similar_found = False
                        for archivo_guardado, texto_guardado in archivos_similares.items():
                            similitud = calcular_similitud(cleaned_content, texto_guardado)
                            if similitud >= umbral_similitud:
                                print(f"El archivo '{filename}' es similar a '{archivo_guardado}' con una similitud de {similitud:.2f}.")
                                similar_found = True
                                break
                        
                        if not similar_found:
                            print(f"El archivo '{filename}' contiene información útil y es único.")
                            hash_dict[hash_val] = filename
                            archivos_similares[filename] = cleaned_content
                else:
                    print(f"El archivo '{filename}' NO contiene información útil.")

# Llamar a la función para procesar el directorio (coloca la ruta de tu carpeta que contiene los archivos)
process_directory('C:/Users/Sam/Downloads/INEGI_muestra_scraping/muestra/assemexico.com')

