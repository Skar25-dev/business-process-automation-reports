# 📊 Business Process Automation Reports (BPAR)

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema **Full-Stack** avanzado de automatización para la generación y distribución de reportes empresariales. Transforma datos crudos en informes profesionales y los gestiona de forma autónoma o bajo demanda mediante una interfaz web moderna, reactiva y elegante.

---

## 🚀 Descripción

BPAR es una solución integral diseñada para eliminar la carga operativa manual en la gestión de datos. El sistema automatiz ael ciclo completo del reporte:
- **Extracción Inteligente:** Consulta dinámica a múltiples tablas (Ventas, Inventario) en bases de datos SQL.
- **Procesamiento de Datos:** Limpieza, filtrado y cálculo de métricas mediante el motor de **Pandas**.
- **Generación Multiformato:** Creación de archivos **Excel (.xlsx)** con Openpyxl y **PDF (.pdf)** con ReportLab (incluyendo diseño corporativo).
- **Distribución Automatizada:** Envío seguro por **Email (SMTP)** con gestión de adjuntos.
- **Gestión Web:** Interfaz para configurar columnas, horarios, formatos y tipos de reporte sin tocar código.

## 📺 Demo en Vivo

Muestra del flujo completo: generación manual, notificación en tiempo real, recepción de email y personalización del sistema.

https://github.com/user-attachments/assets/abb82dbc-a2d8-4289-8a8e-7af0fe1a4ef1



## 📸 Capturas de Pantalla

### 🖥️ Dashboard Principal
Gestión centralizada con iconos dinámicos para PDF/Excel y sistema de notificaciones asíncronas.
![Dashboard](docs/screenshots/dashboard.png)

### ⚙️ Panel de Configuración
Control total con lógica condicional para ocultar campos y selección dinámica de columnas.
![Settings](docs/screenshots/settings.png)

### 📧 Entrega de Reportes
Ejemplo de recepción de reporte mediante protocolo SMTP, garantizando la distribución inmediata.
![Email](docs/screenshots/email_received.png)

### 📊 Resultado Profesional
Vista del reporte PDF generado automáticamente con diseño corporativo y optimización de lectura.
![PDF Preview](docs/screenshots/pdf_preview.png)

---

## ✨ Funcionalidades

✅ **Soporte Multiformato:** Elige entre Excel para análisis profundo o PDF para presentaciones ejecutivas.  
✅ **Dashboard Operativo:** Historial ordenado cronológicamente con iconos visuales diferenciados (Verde/Excel, Rojo/PDF).  
✅ **Configuración Reactiva:** Selección de columnas mediante checkboxes que se actualizan dinámicamente según la tabla elegida.  
✅ **Lógica Condicional de UI:** Interfaz inteligente que oculta campos irrelevantes (ej. oculta "Nombre de hoja" si seleccionas formato PDF).  
✅ **Notificaciones Real-time:** Sistema de mensajes Flash (Toasts) con feedback inmediato tras confirmar el envío del email.  
✅ **Automatización 24/7:** Robot programador (Scheduler) integrado para ejecuciones programadas desatendidas.  
✅ **Arquitectura Multi-DB:** Conector flexible compatible con **SQLite** (desarrollo) y **PostgreSQL** (producción).

---

## 🏗️ Arquitectura del Sistema

El sistema utiliza una arquitectura desacoplada donde el núcleo de datos es independiente de la interfaz de usuario.

### 🔵 Flujo de Trabajo
```text
[ Usuario ] <───► [ Dashboard/Settings ] <───► [ FastAPI ]
                           │                        │
                           ▼                        ▼
[settings.json] ◄─── [ Pydantic Core ] ◄─── [ Background Tasks ]
      │                    │                        │
      ▼                    ▼               ┌────────┴────────┐
[ DB SQL ] ───► [ Pandas Engine ] ───► [ Excel Generator ] o [ PDF Generator ]
                                           └────────┬────────┘
                                                    ▼
                                             [ Email SMTP ]
```

### 📂 Estructura del Proyecto
```text
├── app/
│   ├── main.py            # Punto de entrada: API, Rutas Web e Historial cronológico
│   ├── config.py          # Cerebro de configuración y validación (Pydantic)
│   ├── database.py        # Conexión dinámica (Switch SQLite/Postgres)
│   ├── models.py          # Definición de modelos de negocio (Sales, Inventory)
│   ├── services/          # 🧠 Lógica de Negocio
│   │   ├── report_service.py    # Procesamiento multireporte y filtros dinámicos
│   │   ├── email_service.py     # Envío de correos SMTP y validación
│   │   └── scheduler_service.py # Robot programador (APScheduler)
│   ├── utils/             # 🛠️ Generadores de Archivos
│   │   ├── excel_generator.py   # Motor de diseño Excel (Openpyxl)
│   │   └── pdf_generator.py     # Motor de diseño PDF (ReportLab)
│   ├── templates/         # 📄 Vistas HTML (Jinja2)
│   │   ├── index.html           # Dashboard con Toasts y JS reactivo
│   │   └── settings.html        # Configuración con lógica condicional
│   └── static/            # 🎨 Archivos Estáticos
│       └── css/
│           └── style.css        # Identidad visual (Deep Navy & Tech Violet)
├── config/
│   └── settings.json      # Ajustes de usuario persistentes (JSON)
├── data/
│   └── business_data.db   # Base de datos local (SQLite)
├── reports/               # Almacenamiento cronológico de reportes generados
├── tests/                 # 📂 Suite de Pruebas Automatizadas
├── docs/                  # 📸 Capturas de pantalla y documentación
├── .env.example           # Plantilla de secretos para nuevos entornos
├── .gitignore             # Filtro de seguridad para Git
├── seed_data.py           # Script para poblar la DB con datos coherentes
├── run.sh                 # Script de arranque rápido con autorecarga
├── requirements.txt       # Listado de dependencias del sistema
└── README.md              # Documentación técnica del proyecto

```
### 🛠️ Tecnologías Utilizadas
- **Backend:** FastAPI, SQLAlchemy, Pydantic, APScheduler.
- **Data:** Pandas, Openpyxl, **ReportLab**.
- **Frontend:** Jinja2, Bootstrap5, JavaScript (Fetch API).
- **Seguridad:** Dotenv, Python-Multipart, Watchfiles.

### ⚙️ Instalación y Uso

**1. Preparar entorno:**
```Bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**2. Configurar Secretos:**

- Copia `.env.example` a `.env.`
- Rellena tus credenciales de Email (Password de aplicación) y Base de Datos.

**3. Poblar Base de Datos e iniciar:**

```Bash
python seed_data.py
```

**4. Iniciar el Sistema:**
```bash
./run.sh
```

**5. Acceso:**

- **Dashboard:** `http://localhost:8000`
- **Ajustes:** `http://localhost:8000/settings` 

---
## 📓 Notas de Desarrollo
Este proyecto fue construido siguiendo un roadmap de 8 días, aplicando principios de **Clean Architecture, Programación Asíncrona** y **Diseño UX/UI** orientado a resultados de negocio.

build: versión final 1.2.0 estable
