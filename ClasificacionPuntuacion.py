import os
import re
import hashlib
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Definiciones de umbrales y pesos
UMBRAL_PALABRAS_CLAVE = 5
UMBRAL_SIMILITUD = 0.7
UMBRAL_EXPRESIONES_NECESARIAS = 3

# Pesos de expresiones clave
PESO_DIRECCION = 1.5
PESO_RFC = 2.0
PESO_CORREO = 2.0
PESO_TELEFONO = 1.5

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

# Limpiar HTML
def limpiar_html(texto_html):
    soup = BeautifulSoup(texto_html, 'lxml')
    return soup.get_text(separator=" ").strip()

# Función para calcular similitud
def calcular_similitud(texto1, texto2):
    vectorizer = TfidfVectorizer().fit_transform([texto1, texto2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]

# Función para calcular la puntuación y contar expresiones necesarias
def puntuar_palabras_clave(texto):
    score = 0
    cuenta_total_expresiones = 0
    
    # Contar coincidencias de expresiones regulares
    if len(re.findall(direccion_regex, texto)) > 0:
        score += len(re.findall(direccion_regex, texto)) * PESO_DIRECCION
        cuenta_total_expresiones += 1
    if len(re.findall(rfc_regex, texto)) > 0:
        score += len(re.findall(rfc_regex, texto)) * PESO_RFC
        cuenta_total_expresiones += 1
    if len(re.findall(correos_regex, texto)) > 0:
        score += len(re.findall(correos_regex, texto)) * PESO_CORREO
        cuenta_total_expresiones += 1
    if len(re.findall(telefonos_regex, texto)) > 0:
        score += len(re.findall(telefonos_regex, texto)) * PESO_TELEFONO
        cuenta_total_expresiones += 1
    
    # Contar coincidencias de palabras clave adicionales
    for palabra in palabras_clave:
        if re.search(rf'\b{re.escape(palabra)}\b', texto, re.IGNORECASE):
            score += 1
            cuenta_total_expresiones += 1
    
    return score, cuenta_total_expresiones

# Procesar directorio y filtrar archivos
def process_directory(directory):
    archivos_procesados = {}
    archivos_innecesarios = []
    archivos_no_utiles = []
    archivos_duplicados = []

    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            
            # Calcular hash del archivo para detectar duplicados idénticos
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            # Si el archivo ya fue procesado por ser idéntico, lo registramos como duplicado
            if file_hash in archivos_procesados:
                print(f"'{filename}' es idéntico a '{archivos_procesados[file_hash]['filename']}'. Marcado como duplicado.")
                archivos_duplicados.append(file_path)
                continue
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                cleaned_content = limpiar_html(content)

                # Calcular puntuación y contar expresiones necesarias
                puntuacion, cuenta_total_expresiones = puntuar_palabras_clave(cleaned_content)
                
                # Identificar si el archivo es no útil (menos de tres expresiones necesarias)
                if cuenta_total_expresiones < UMBRAL_EXPRESIONES_NECESARIAS:
                    print(f"'{filename}' no contiene al menos tres expresiones o palabras clave. Marcado como no útil.")
                    archivos_no_utiles.append(file_path)
                    continue

                # Filtrar archivos con baja puntuación
                if puntuacion < UMBRAL_PALABRAS_CLAVE:
                    print(f"'{filename}' tiene baja puntuación ({puntuacion}). Archivo marcado como innecesario.")
                    archivos_innecesarios.append(file_path)
                    continue

                archivo_unico = True
                for archivo, data in archivos_procesados.items():
                    similitud = calcular_similitud(cleaned_content, data['contenido'])

                    if similitud >= UMBRAL_SIMILITUD:
                        archivo_unico = False
                        if puntuacion > data['puntuacion']:
                            print(f"'{filename}' es mejor en palabras clave que '{data['filename']}' (puntuación {puntuacion} vs {data['puntuacion']}). '{data['filename']}' marcado como duplicado.")
                            archivos_duplicados.append(data['path'])
                            archivos_procesados[file_hash] = {'contenido': cleaned_content, 'puntuacion': puntuacion, 'path': file_path, 'filename': filename}
                        else:
                            print(f"'{data['filename']}' es mejor en palabras clave que '{filename}' (puntuación {data['puntuacion']} vs {puntuacion}). '{filename}' marcado como duplicado.")
                            archivos_duplicados.append(file_path)
                        break

                if archivo_unico:
                    archivos_procesados[file_hash] = {'contenido': cleaned_content, 'puntuacion': puntuacion, 'path': file_path, 'filename': filename}
                    print(f"'{filename}' agregado como archivo único con puntuación {puntuacion}.")

    
# Llamar a la función
process_directory('C:/Users/Sam/Downloads/INEGI_muestra_scraping/muestra/bhealth.mx')
