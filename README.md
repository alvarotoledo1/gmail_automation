# Gmail Automation - Excel Attachment Processor

## Descripción

Este proyecto automatiza la lectura de correos electrónicos en Gmail que contienen archivos Excel adjuntos, descarga esos archivos, valida el remitente, normaliza la estructura de los datos y genera un archivo procesado listo para ser utilizado en otros sistemas o procesos.

El objetivo principal es eliminar tareas manuales repetitivas relacionadas con la recepción y preparación de archivos enviados por correo.

---

## Problema que resuelve

En muchos entornos de trabajo se reciben archivos Excel por correo electrónico de forma periódica. Procesarlos manualmente implica:

- Revisar correos nuevos
- Descargar adjuntos
- Verificar remitente
- Abrir archivos
- Corregir nombres de columnas
- Unificar formatos
- Guardar versiones finales

Este proyecto automatiza todo ese flujo.

---

## Flujo del proceso

1. Conexión a Gmail mediante API.
2. Búsqueda de correos nuevos con archivos `.xlsx`.
3. Validación del remitente autorizado.
4. Descarga del archivo adjunto.
5. Lectura del Excel con Python.
6. Normalización de nombres de columnas.
7. Agregado de columna de origen.
8. Generación de archivo final procesado.

---

## Tecnologías utilizadas

- Python
- Gmail API
- Google OAuth 2.0
- Pandas
- Openpyxl
- Git
- GitHub

---

## Estructura del proyecto

```text
gmail_automation/
│── app.py
│── config.json
│── credentials.json
│── token.json
│── requirements.txt
│── .gitignore
│── data/
│   ├── raw/
│   └── processed/
│── logs/