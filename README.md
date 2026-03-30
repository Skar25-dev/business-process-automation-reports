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

✅ **Dashboard Web:** Interfaz visual moderna (Bootstrap 5) para el control del sistema.
✅ **Ejecución Manual:** Botón para disparar reportes al instante sin esperar al Scheduler.
✅ **Historial de Reportes:** Listado automático y visor de archivos generados.
✅ **Descarga Directa:** Acceso inmediato a los archivos Excel desde el navegador.
✅ **Automatización 24/7:** Robot programador (Scheduler) para envíos diarios.
✅ **Arquitectura Robusta:** Uso de rutas absolutas y tareas en segundo plano (Background Tasks).

---

## 🏗️ Arquitectura del Sistema

El sistema utiliza una arquitectura orientada a servicios (SOA) con un motor de tareas en segundo plano.

### 🔵 Flujo de Trabajo
```
[ Usuario ] <───► [ Dashboard HTML/CSS ] <───► [ FastAPI ]
                                                   │
      ┌────────────────────────────────────────────┤
      ▼                                            ▼
[ Background Task ]                          [ File System ]
      │                                            │
      └─► [ ReportService ] ──► [ Excel ] ──► [ reports/ ]
```
### 🛠️ Componentes Principales
- **Interfaz (Frontend):** Plantillas dinámicas con Jinja2 y estilos modulares en **CSS3**.
- **Backend (FastAPI):** Gestión de rutas estáticas, descarga de archivos y procesamiento asíncrono.
- **Persistencia:** Almacenamiento físico de reportes con nombres fechados para auditoria.

### 📂 Estructura del Proyecto
```
├── app/
│   ├── main.py            # Entrada de la API y arranque del Scheduler (Día 5)
│   ├── config.py          # Cerebro de configuración y validación
│   ├── database.py        # Conector flexible SQLite/Postgres
│   ├── models.py          # Modelos de datos (SQLAlchemy)
│   ├── services/          # 🧠 Lógica de Negocio
│   │   ├── report_service.py    # Procesamiento y filtros
│   │   ├── email_service.py     # Envío de correos (SMTP)
│   │   └── scheduler_service.py # ⏱️ Programador de tareas (Día 5)
│   └── utils/             
│       └── excel_generator.py   # Motor de diseño de Excel
├── config/                # Ajustes de usuario (settings.json)
├── data/                  # Almacenamiento de base de datos local
├── reports/               # Histórico de archivos generados (.xlsx)
├── tests/                 # 📂 Suite de Pruebas y Verificación
│   ├── test_config.py     # Valida .env y configuración
│   ├── test_report.py     # Valida generación de Excel
│   ├── test_full_flow.py  # Valida flujo integral (Manual)
│   └── test_scheduler.py  # Valida autonomía del robot (Día 5)
├── .env                   # Secretos y passwords (Excluido de Git)
├── .env.example           # Plantilla de secretos para nuevos entornos
├── .gitignore             # Filtro de seguridad para Git
├── seed_data.py           # Generador de datos iniciales (Faker)
├── requirements.txt
└── README.md
```
### 🛠️ Tecnologías Utilizadas
- **Backend:** Python 3.12+, FastAPI, SQLAlchemy.
- **Datos:** Pandas, Openpyxl.
- **Email:** FastAPI-Mail (aiosmtplib).
- **Validación:** Pydantic Settings & Dotenv.
- **Automatización:** APScheduler.

### ⚙️ Instalación y Configuración

**1. Preparar entorno:**
```Bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**2. Configurar Secretos:**

- Copia .env.example a .env.

- Rellena MAIL_USERNAME y MAIL_PASSWORD (Usa una Contraseña de Aplicación si usas Gmail).

**3. Poblar Base de Datos:**

```Bash
python seed_data.py
```

**4. Ejecutar Pruebas (Desde la raíz):**

- Verificar configuración: ` python -m tests.test_config `
- Generar Excel: ` python -m tests.test_report `
- **Flujo Completo (Envío de Email):** `python -m tests.test_full_flow`
- **Probar el Robot (Scheduler):** `python -m test.test_scheduler` (ejecución cada minuto).

**5. Iniciar Servidor Producción:**
```Bash
uvicorn app.main:app --reload --reload-include "*.json" --reload-include "*.html" --reload-include "*.css" --port 8000
```