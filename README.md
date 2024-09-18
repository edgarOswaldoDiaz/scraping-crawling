## Project Scraping & Crawling for Data Engineering

# Objetivo

Aprovechar la información de los sitios web con dominio mexicano y extraer información para el análisis del contenido de los datos y su vinculación con el Registro Estadístico de Negocios de México (RENEM) para la identificación y análisis de la economía digital.

# Metodología

Para atender los objetivos específicos del proyecto, que incluyen la obtención de un listado de sitios de Internet de negocios con dominio mexicano y sus características para vincularlos con el RENEM mediante web scraping, se propone la siguiente metodología:

#. Selección de Sitios Web: Identificar y listar sitios web relevantes con dominio mexicano, enfocándose en aquellos que pertenecen a negocios y empresas.
#. Desarrollo de Herramientas de Web Scraping: Crear o adaptar herramientas específicas de web scraping que sean capaces de extraer información relevante de estos sitios de manera eficiente y respetando las normativas legales y éticas.
#. **Extracción de Datos**: Utilizar las herramientas de web scraping para recolectar datos específicos de los sitios web seleccionados, como el tipo de negocio, servicios ofrecidos, datos de contacto, entre otros.
#. **Análisis y Clasificación de Datos**: Analizar los datos recopilados para clasificarlos y organizarlos de manera que puedan ser fácilmente vinculados con la información existente en el RENEM.
#. **Integración de Datos con el RENEM**: Desarrollar un sistema o metodología para integrar de forma eficaz los datos recopilados con la base de datos del RENEM, asegurando la precisión y la actualización de la información.

# Sitios Web

Es necesario trabajar con grandes cantidades de datos para obtener información valiosa sobre negocios y comercio. Es por eso que se busca expandir las fuentes a sitios web. Las estrategias más usuales para estos propósitos consisten en un rastreo constante para generar índices del internet para luego **estructurar la información disponible**.

- 670,485 sitios
- 6,398,357 páginas
- 1,093 Gb

# Detección de datos

Cada fuente se describe de acuerdo a un conjunto de variables que se extraen del mismo sitio e intentan describir la naturaleza del negocio como geolocalización, contenido, e-commerce, marketing, datos técnicos y de hosting.

Para la vinculación de registros del RENEM con diferentes fuentes de información se toman como como referencia dos principales grupos de datos:

- **Datos de identificación**: Nombre, Razón Social
- **Datos de ubicación**: Ubicación geográfica, Domicilio postal

De acuerdo a las características y contenido de la base de datos se pueden definir diferentes criterios de búsqueda y confronta:

| Campos extraídos         | Registros Asociados        |
| ------------------------ | -------------------------- |
| Business Registry number | RFC                        |
| Company Name             | Nombre del Establecimiento |
| Company Name             | Razón social               |
| Company Name y Address   | Razón Social y Domicilio   |
| Hostname                 | Sitio web                  |
| Hostname                 | Nombre del Establecimiento |
| Hostname                 | Razón Social               |
| Phone Number             | Teléfono                   |


## Campos Principales

| Campo                     | Ejemplo             |
| ------------------------- | ------------------- |
| Company name              | Zonyx               |
| Company type              | Lucro - no lucro    |
| Legal entity              | SA de CV            |
| Business registry number  | RFC                 |
| IBAN number               |                     |
| BIC number                |                     |
| Tax number                |                     |
| Email address             | gmorklla@gmail.com  |
| Secondary email addresses |                     |

## Campos Geográficos

| Campo     | Ejemplo         | 
| --------- | --------------- |
| Region    | Veracruz        |
| City      | Álvaro Obregón  |
| Address   |                 |
| Addresses |                 |
| Zip code  | 15800           |
| Continent | Norte América   |
| Country   | MX              |

## Campos de Transacciones

| Campo                     | Ejemplo       |
| ------------------------- | ------------- |
| Shopping cart system      | MercadoShops  |
| Trustmarks                | GoDaddy       |
| Delivery services         | FedEx         |
| Payment methods           | MasterCard    |
| Payment service providers | PayPal        |
| Currency                  | MXN           |

## Campos Adicionales

| Campo             |
| ----------------- |
| **Description**   |
| Keywords          |

----------------------------------
> INEGI 2024 | Programa Anual de Investigación. 
