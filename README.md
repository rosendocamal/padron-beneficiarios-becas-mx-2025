# Datos abiertos consolidados del programa de becas educativas en México durante 2025

## Programa Nacional de Becas para el Bienestar Benito Juárez

Los programas de becas en México para los tres niveles educativos (básica, media superior y superior) forman parte de la política federal de Becas para el Bienestar, cuyo objetivo principal es garantizar el acceso, la permanencia y la conclusión de los estudios, reduciendo la deserción escolar por motivos económicos. Estos apoyos consisten en transferencias monetarias directas, priorizan a estudiantes de escuelas públicas y a poblaciones en condiciones de vulnerabilidad, y aumentan su monto conforme avanza el nivel educativo. En conjunto, los programas buscan que niñas, niños y jóvenes puedan continuar su trayectoria educativa completa, desde la educación básica hasta la universidad, sin que la falta de recursos sea un impedimento.

## Mi proyecto

Este proyecto consolida los *datasets* de los programas de becas de los tres niveles educativos cuya fuente original son los [datos abiertos de México.](https://www.datos.gob.mx/) Los *datasets* fueron descargados, limpiados, estandirizados y fusionados en una sola base de datos lista para su análisis. En total fueron **384 datasets en formato csv**. Esta cantidad se debe a que los datos originales se encuentra dividido en 3 programas de becas (por nivel educativo), presentados por 4 trimestres y por cada una de las 32 entidades federativas del país. El resultado final fue una base de datos en **SQLite** con un peso de **6.3 GB** y un total de **85,686,055 (85.6 millones)** de registros.

## Fuentes de datos

Los datos provienen de las fuentes oficiales de [Datos Abiertos de México:](https://www.datos.gob.mx/)

- [Programa de Becas de Educación Básica](https://www.datos.gob.mx/dataset/programa_nacional_becas_bienestar_benito_juarez_2025_programa_s072)
- [Programa de Becas de Educación Media Superior](https://www.datos.gob.mx/dataset/programa_nacional_becas_bienestar_benito_juarez_2025_programa_s311)
- [Programa de Becas de Educación Superior](https://www.datos.gob.mx/dataset/programa_nacional_becas_bienestar_benito_juarez_2025_programa_s283)

Fueron consultados el día 21 de enero de 2026, con última actualización de los datasets con fecha de 16 de enero de 2026 de acuerdo a lo publicado en los sitios oficiales. Los datasets corresponde al ejercicio fiscal de 2025, con datos reportados en cada trimestre del año por cada una de las 32 entidades federativas del país.

## Proceso de transformación

1. Obtener los enlances individuales de descarga de los datasets

Antes de generar el script en Python para realizar la descarga masiva de los 384 archivos en formato csv, analicé la estructura HTML de los sitios de datos con la finalida de identificar la manera de automatizar dicha descarga, ya que son 384 enlaces. Una vez encontrado la estructura, los elementos y clases del HTML, con ayuda de la libería de **request** para las peticiones HTTP y **BeautifulSoup** para el parseo del HTML obtuve los enlaces de descarga, los guarde en tres archivos de texto correspondiendo cada uno de los archivos a cada programa de becas.

> Puedes consultar el web scrapper [aquí.](scripts/etl/01_get_download_links.py)

2. Descarga masiva de los datasets

Con los enlaces guardados de manera persistente en archivos de texto descargo los datasets, con la ventaja de que se puede ejecutar la desccarga en cualquier momento o para tener a mano dichos enlaces para una revisión manual como posible opción. Los datasets se guardan mediante carpetas agrupados por el tipo de programa y el periodo trimestral correspondiente. Se modifica y se adapta el nombre de los archivos para una estandarización que nos ayudará más tarde. Los datasets se guardan en fragmentos o chunks.

> Puedes consultar el downloader [aquí.](scripts/etl/02_download_files.py)

3. Limpieza, unificación, normalización de nombres de columnas y conversión de tipos de datos 

Extraje los nombres de las cabeceras, los nombres de los programas en claves y los periodos trimestrales con la finalidad de normalizar y manipular pues los propios nombres de los datos, obtener la ruta para la lectura/escritura de los archivos y poder fragmentar los datos. En la separación de las columnas utilicé **';'** (punto y coma) en lugar de la coma por brindar mayor facilidad de uso. En este paso creo tres archivos unificados por programa en formato csv. Inicié un dataset unificado por programa a la vez y abría los archivos correspondientes registro por registro y limpiaba cada uno, los fragmenté por columnas usando la función un split modificado con el uso de regex para evitar hacer divisiones incorrectas con el uso del split nativo de Python. Cada fragmento pasaba por la verificación del tipo de dato, se eliminaba saltos de línea o si era fecha se adecuada al estándar de DD-MM-AAAA.

El dataset unificado de las Becas para Educación Básica cuenta con 64,977,396 registros y un peso de 4.3 GB. Por otro lado, el dataset del las Becas para Educación Media Superior cuenta con 18,599,297 registros y un peso de 1.3 GB. Por último, el dataset de las Becas para la Educación Superior cuenta con 2,109,362 registros y un peso de 146 MB. En total fueron 85,686,055 registros y un peso final de 5.74 GB aproximadamente.

> Puedes consultar el limpiador y unificador [aquí.](scripts/etl/03_merging_datasets.py)

> Gran parte de los pasos 1, 2 y 3 fueron ejecutados mediante una secuenciador o automatizador, incluye un contador de tiempo de ejecución y puedes consultar el automatizador **ETL** [aquí.](scripts/etl)

4. Unificación final y exportación a una base de datos

Por último, utilizo una base de datos con **SQLite** utilizando la librería de **sqlite3** con Python. Genero la tabla con los encabezados normalizados y su tipo de dato correspondiente de los csv. Luego, itero sobre los archivos concatenados del paso 3, proceso los registros y los inserto en la base de datos. También mido el tiempo de ejecución y la cantidad de registros por cada uno de los tres archivos fueron insertados de manera correcta.

**Herramientas usadas:**
- Python (BeautifulSoup, request, regex, os, time, sqlite3)
- SQL

## Estructura del proyecto

.
├── data/                        
│   ├── processed/               
│   │   ├── s072/                
│   │   │   └── names_files.txt
│   │   ├── s283/               
│   │   │   └── names_files.txt 
│   │   └── s311/                
│   │       └── names_files.txt 
│   ├── raw/                     # Datos crudos
│   │   ├── datasets/            
│   │   │   ├── s072/            
│   │   │   │   ├── Q1/         
│   │   │   │   ├── Q2/         
│   │   │   │   ├── Q3/         
│   │   │   │   ├── Q4/     
│   │   │   │   └── s072_datasets_links.txt
│   │   │   ├── s283/            
│   │   │   │   ├── Q1/         
│   │   │   │   ├── Q2/         
│   │   │   │   ├── Q3/         
│   │   │   │   ├── Q4/         
│   │   │   │   └── s283_datasets_links.txt
│   │   │   └── s311/            
│   │   │       ├── Q1/         
│   │   │       ├── Q2/         
│   │   │       ├── Q3/         
│   │   │       ├── Q4/         
│   │   │       └── s311_datasets_links.txt
│   └── db/                      
│       └── CNBBBJ_2025.db       # Base de datos con los datos consolidados
├── scripts/                     
│   ├── etl/                     # Scripts para el proceso de ETL (Extracción, Transformación y Carga)
│   │   ├── 01_get_download_links.py  # Obtención de enlaces de descarga de los datasets
│   │   ├── 02_download_files.py      # Descarga masiva de los archivos CSV
│   │   ├── 03_merging_datasets.py   # Unificación y limpieza de los datasets
│   │   └── automatic_etl.py         # Secuenciador que automatiza todo el proceso ETL
│   └── create_db.py                # Creación de la base de datos SQLite y carga de datos
├── .gitignore                     
├── LICENSE                        
├── README.md                      
└── requirements.txt               # Dependencias necesarias para ejecutar el proyecto
