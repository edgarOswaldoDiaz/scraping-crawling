# Clasificación de Archivos HTML para Información Útil

## Objetivo

El objetivo de este código es analizar archivos de texto que contienen código HTML y verificar si estos archivos contienen información relevante relacionada con direcciones, teléfonos, RFC, correos electrónicos, métodos de pago, entre otros datos clave. Esto es útil para procesos automatizados de scraping o análisis de contenido en páginas web.

## Funcionamiento

El código sigue los siguientes pasos para clasificar los archivos:

1. **Limpieza del Contenido HTML**: Aunque los archivos no tienen extensión HTML, su contenido sigue este formato. Se utiliza `BeautifulSoup` para limpiar las etiquetas HTML y extraer solo el texto visible.
   
2. **Búsqueda de Palabras Clave y Expresiones Regulares**: Se definen varias expresiones regulares (regex) que permiten encontrar información específica como direcciones, teléfonos, correos electrónicos, RFCs, etc. También se utilizan palabras clave que amplían el alcance del código.

3. **Verificación de Utilidad**: El archivo se considera útil si contiene al menos 3 de las palabras clave o si las expresiones regulares encuentran coincidencias. Si se encuentra una cantidad suficiente de coincidencias, el archivo se marca como que contiene información útil.

4. **Procesamiento de Archivos**: El código revisa todos los archivos de una carpeta específica, lee su contenido, lo limpia, y luego verifica si es útil o no.

## Librerías Necesarias

Este código requiere las siguientes librerías:
- **`os`**: Para recorrer los archivos de la carpeta.
- **`re`**: Para el uso de expresiones regulares en la búsqueda de patrones.
- **`BeautifulSoup`** (de `bs4`): Para limpiar el contenido HTML y extraer solo el texto.

### Instalación de Librerías

Si no tienes instaladas estas librerías, puedes instalarlas usando `pip`:

```bash
pip install beautifulsoup4
