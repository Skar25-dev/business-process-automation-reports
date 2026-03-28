# 📊 Business Process Automation Reports (BPAR)

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema integral de automatización para la generación y distribución de reportes empresariales. Transforma datos crudos en informes profesionales (Excel/PDF) y los distribuye automáticamente por email.

---

## 🚀 Descripción

BPAR es una solución diseñada para eliminar tareas repetitivas en departamentos de administración y finanzas. El sistema automatiza el ciclo de vida completo del dato:
- **Extracción:** Consulta dinámica a bases de datos (SQLite/PostgreSQL).
- **Procesamiento:** Limpieza y cálculo de métricas mediante **Pandas**.
- **Generación:** Creación de archivos profesionales con **Openpyxl**.
- **Distribución:** Envío automático por **Email (SMTP)** con archivos adjuntos.

---

## ✨ Funcionalidades

✅ **Generación Automática:** Reportes profesionales listos sin intervención humana.  
✅ **Envío por Email:** Distribución automática a destinatarios configurables.  
✅ **Dashboard Web:** Interfaz visual para gestionar y descargar reportes (En desarrollo).  
✅ **Arquitectura Multi-DB:** Compatible con **SQLite** y **PostgreSQL**.  
✅ **Configuración Segura:** Uso de archivos `.env` para credenciales y `settings.json` para ajustes.  
✅ **Suite de Pruebas:** Pruebas modulares organizadas para validar cada capa del sistema.  

---

## 🏗️ Arquitectura del Sistema

### 🔵 Flujo de Trabajo
```
[ DB ] ──► [ Pandas Engine ] ──► [ Excel Generator ] ──► [ Email Service ] ──► [ Destinatario ]
```
### 🛠️ Componentes Principales
- **Capa de Configuración:** Gestión de secretos con `python-dotenv` y validación con `Pydantic`.
- **Capa de Servicios:**
  - **ReportService:** Orquesta la extracción y procesamiento.
  - **EmailService:** Gestiona la conexión SMTP y el envío de adjuntos.
- **Suite de Pruebas:** Localizada en `/tests`, permite verificar el sistema de forma aislada o integral.

### 📂 Estructura del Proyecto
```
├── app/
│   ├── main.py            # Entrada de la API y Scheduler
│   ├── config.py          # Cerebro de configuración y validación
│   ├── database.py        # Conector flexible SQLite/Postgres
│   ├── models.py          # Modelos de datos (SQLAlchemy)
│   ├── services/          
│   │   ├── report_service.py # Lógica de reportes y filtros
│   │   └── email_service.py  # Lógica de envío de correos (Día 4)
│   └── utils/             
│       └── excel_generator.py # Motor de diseño de Excel
├── config/                # Ajustes de usuario (settings.json)
├── data/                  # Almacenamiento de base de datos local
├── reports/               # Histórico de archivos generados
├── tests/                 # 📂 Suite de Pruebas (Organizado Día 4)
│   ├── check_data_pandas.py
│   ├── test_config.py
│   ├── test_report.py
│   └── test_full_flow.py  # Prueba del flujo completo: DB -> Excel -> Email
├── .env                   # Secretos y passwords (Excluido de Git)
├── .env.example           # Plantilla de secretos para nuevos entornos
├── .gitignore             # Filtro de seguridad para Git
├── seed_data.py           # Generador de datos iniciales
├── requirements.txt
└── README.md
```
### 🛠️ Tecnologías Utilizadas
- **Backend:** Python 3.12+, FastAPI, SQLAlchemy.
- **Datos**: Pandas, Openpyxl.
- **Email**: FastAPI-Mail (aiosmtplib).
- **Validación**: Pydantic Settings & Dotenv.

### ⚙️ Instalación y Configuración

**1. Preparar entorno:**
```
Bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**2. Configurar Secretos:**

- Copia .env.example a .env.

- Rellena MAIL_USERNAME y MAIL_PASSWORD (Usa una Contraseña de Aplicación si usas Gmail).

**3. Poblar Base de Datos:**

```
Bash
python seed_data.py
```

**4. Ejecutar Pruebas (Desde la raíz):**

- Verificar configuración: ` python -m tests.test_config `
- Generar Excel: ` python -m tests.test_report `
- **Flujo Completo (Envío de Email):** `python -m tests.test_full_flow`