# 📊 Business Process Automation Reports (BPAR)

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema integral de automatización para la generación y distribución de reportes empresariales. Elimina la carga operativa manual, reduce errores humanos y garantiza la entrega puntual de información crítica.

## 🚀 Descripción

Este proyecto permite a empresas automatizar la generación de reportes diarios, eliminando tareas manuales repetitivas y reduciendo errores humanos.

El sistema:
- Consulta datos desde una base de datos
- Genera reportes en Excel (o PDF)
- Envía los reportes automáticamente por email
- Permite generar reportes manualmente mediante una API

---

## 💡 Caso de Uso Real
Ideal para departamentos de Finanzas, Ventas u Operaciones que actualmente dedican horas diarias a exportar datos de un ERP/CRM, darles formato en Excel y enviarlos por correo a los gerentes. **BPAR lo hace en segundos y sin intervención humana.**

## 💡 Caso de uso real

Muchas empresas generan reportes diariamente de forma manual:
- Exportando datos
- Creando Excel
- Enviando emails

Este sistema automatiza todo el proceso, permitiendo:
- Ahorro de tiempo
- Reducción de errores
- Estandarización de informes

---

## ⚙️ Funcionalidades

✅ Generación automática de reportes  
✅ Envío de emails con adjuntos  
✅ Programación diaria de tareas  
✅ API para ejecución manual  
✅ Almacenamiento de reportes históricos  
✅ Configuración flexible mediante JSON  

---
## 🏗️ Arquitectura del Sistema

El sistema está diseñado siguiendo una arquitectura modular por capas, separando la lógica de obtención de datos, el procesamiento y la distribución.

### 🔵 Flujo de Datos
```text
[ Base de Datos ] 
      │
      ▼
[ SQLAlchemy ORM ] ──► (Modelos de Datos)
      │
      ▼
[ Service Layer ] ──► [ Pandas Processing ] ──► [ Excel/PDF Utils ]
      │                                               │
      │                                               ▼
      ├───────► [ Scheduler ] ───┐             [ Archivos .xlsx ]
      │         (Auto-ejecución) │                    │
      ▼                          ▼                    │
[ FastAPI ] ◄─────────── [ Email Service ] ◄──────────┘
(Ejecución Manual)       (Envío con Adjunto)
```
### 🛠️ Componentes Principales
- Capa de Datos (DAL): Utiliza SQLAlchemy para la interacción con la base de datos. Los modelos definen la estructura de ventas y productos.
- Capa de Procesamiento (Utils): Módulos especializados que transforman datos crudos en archivos finales. Usa Pandas para el análisis y Openpyxl para el formato profesional de Excel.
- Capa de Servicios (Services):
- Report Service: Orquestador que extrae datos y genera los archivos.
- Email Service: Gestiona la conexión SMTP y el envío de correos con adjuntos.
- Scheduler Service: Utiliza APScheduler para ejecutar tareas automáticas en segundo plano (Cron jobs).
- Capa de Interfaz (API): Desarrollada con FastAPI, permite disparar reportes manualmente y monitorear el sistema.

### 🛠️ Tecnologías Utilizadas
- Lenguaje: Python 3.12+
- Framework API: FastAPI
- Análisis de Datos: Pandas
- ORM: SQLAlchemy
- Generación de Archivos: Openpyxl (Excel) & ReportLab (PDF)
- Automatización: APScheduler
- Emails: FastAPI-Mail (SMTP)

### 📂 Estructura del Proyecto
```
├── app/
│   ├── main.py            # Punto de entrada de la API y Scheduler
│   ├── database.py        # Configuración de SQLAlchemy
│   ├── models.py          # Modelos de la base de datos
│   ├── services/          # Lógica de negocio (Email, Reportes, Agenda)
│   └── utils/             # Generadores de archivos (Excel, PDF)
├── config/                # Ajustes y credenciales (JSON)
├── data/                  # Base de datos local (SQLite)
├── reports/               # Histórico de archivos generados
├── seed_data.py           # Script para generar datos ficticios iniciales
├── check_data_pandas.py   # Script de verificación y análisis de datos
├── requirements.txt
└── README.md
```
