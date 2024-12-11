# Documentación del Proyecto de Clasificación Automática de Archivos HTML

## Descripción del Proyecto

Este proyecto tiene como objetivo principal **mejorar el manejo y análisis de archivos HTML** dentro de un sistema de extracción de datos enfocado en la **medición de negocios en la economía digital**. El desarrollo consistió en diseñar un script que automatiza la clasificación de archivos, eliminando aquellos que no son relevantes antes de ser procesados por herramientas de *scraping*. Esta automatización no solo **incrementa la eficiencia**, sino que también **reduce la carga operativa** y los posibles errores humanos derivados del análisis manual de grandes volúmenes de datos.

La solución propuesta optimiza el proceso de clasificación en entornos donde el volumen de datos es elevado. La clasificación manual de archivos HTML resultaba lenta y propensa a errores, lo que dificultaba el análisis posterior de la información. Gracias a este script, el filtrado automático de archivos irrelevantes mejora la eficiencia operativa al reducir el tiempo invertido en tareas manuales y facilita la integración con herramientas de *scraping*. 

Esto no solo mejora la calidad de los resultados obtenidos, sino que también optimiza los recursos disponibles.

## Dependencias

El script requiere las siguientes bibliotecas de Python:

- `os`: Para recorrer directorios y manejar archivos.
- `re`: Para utilizar expresiones regulares.
- `hashlib`: Para calcular *hashes* y detectar duplicados.
- `bs4` (*BeautifulSoup*): Para limpiar el contenido HTML.
- `sklearn`: Para calcular la similitud de texto con `TfidfVectorizer` y `cosine_similarity`.

Instala las dependencias:

```bash
pip install beautifulsoup4 scikit-learn
```

## Configuración del Script

### Umbrales y Pesos

- **Umbrales**:
  - `UMBRAL_PALABRAS_CLAVE`: Puntuación mínima para considerar un archivo relevante (por defecto, `5`).
  - `UMBRAL_SIMILITUD`: Valor de similitud para identificar archivos similares (por defecto, `0.7`).
  - `UMBRAL_EXPRESIONES_NECESARIAS`: Número mínimo de expresiones clave para considerar un archivo útil (por defecto, `3`).

- **Pesos para Expresiones Clave**:
  - `PESO_DIRECCION`: Peso para direcciones (`1.5`).
  - `PESO_RFC`: Peso para RFCs (`2.0`).
  - `PESO_CORREO`: Peso para correos electrónicos (`2.0`).
  - `PESO_TELEFONO`: Peso para teléfonos (`1.5`).

### Expresiones Regulares

Las siguientes expresiones regulares se utilizan para buscar patrones específicos en los archivos HTML:

- **Direcciones**: `direccion_regex`
- **RFC**: `rfc_regex`
- **Correos Electrónicos**: `correos_regex`
- **Teléfonos**: `telefonos_regex`
- **Códigos Postales**: `codigo_postal_regex`
- **Métodos de Pago**: `metodo_pago_regex`
- **Paquetería**: `paqueteria_regex`
- **Regiones**: `region_regex`

### Palabras Clave

El script incluye una lista de **palabras clave adicionales** tanto en español como en inglés para mejorar la identificación de archivos relevantes.

## Funciones Principales

### `limpiar_html(texto_html)`

- **Descripción**: Limpia el contenido HTML y devuelve solo el texto.
- **Parámetros**: `texto_html` (cadena con el contenido HTML).
- **Retorna**: Texto limpio.

### `calcular_similitud(texto1, texto2)`

- **Descripción**: Calcula la similitud entre dos textos usando TF-IDF y similitud coseno.
- **Parámetros**: `texto1` y `texto2` (cadenas de texto).
- **Retorna**: Valor de similitud (flotante).

### `puntuar_palabras_clave(texto)`

- **Descripción**: Calcula la puntuación basada en las coincidencias con expresiones regulares y palabras clave.
- **Parámetros**: `texto` (cadena de texto).
- **Retorna**: Una tupla con la puntuación total y el número de expresiones coincidentes.

### `process_directory(directory)`

- **Descripción**: Recorre el directorio especificado, analiza cada archivo HTML y lo clasifica como relevante, no útil, innecesario o duplicado.
- **Parámetros**: `directory` (ruta del directorio a procesar).

- **Acciones Automáticas**:
  - **Eliminar archivos innecesarios**: Si un archivo tiene una puntuación baja (por debajo del `UMBRAL_PALABRAS_CLAVE`), se elimina automáticamente del directorio.
  - **Eliminar archivos duplicados**: Si un archivo es idéntico a otro previamente procesado, se elimina automáticamente.

## Ejecución del Script

Ejecuta el script especificando el directorio que contiene los archivos HTML:

```python
process_directory("ruta/a/tu/directorio")
```

El script realizará las siguientes acciones:

1. **Detectar duplicados** mediante *hashes*.
2. **Limpiar el contenido HTML** y analizar su texto.
3. **Calcular la puntuación** basada en las expresiones clave y palabras clave.
4. **Clasificar archivos** en las siguientes categorías:
   - **Duplicados**: Archivos idénticos a otros previamente procesados (se eliminan).
   - **No útiles**: Archivos con menos de tres coincidencias de expresiones clave.
   - **Innecesarios**: Archivos con puntuación baja (se eliminan).
   - **Relevantes**: Archivos que cumplen con los umbrales establecidos.

## Ejemplo de Salida

```plaintext
'archivo1.html' es idéntico a 'archivo2.html'. Archivo eliminado como duplicado.
'archivo3.html' no contiene al menos tres expresiones o palabras clave. Marcado como no útil.
'archivo4.html' tiene baja puntuación (3). Archivo eliminado como innecesario.
'archivo5.html' es relevante.
```

## Conclusión

Este script facilita la clasificación automática de archivos HTML, optimizando el proceso de filtrado previo al *scraping*. La automatización mejora la eficiencia operativa y reduce los errores humanos, permitiendo un análisis más ágil y efectivo de la información relevante en el contexto de la economía digital.
