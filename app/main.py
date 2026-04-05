import os
import json
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.services.report_service import REPORT_MODELS
from app.services.email_service import EmailService
from app.services.scheduler_service import start_scheduler
from app.config import settings

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el arranque y cierre del robot (Scheduler)"""
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="BPAR System", lifespan=lifespan)

# Montar archivos estáticos y plantillas
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# --- INTERFAZ WEB (DASHBOARD) ---

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Muestra el historial de reportes y el panel de control"""
    if not REPORTS_DIR.exists():
        REPORTS_DIR.mkdir(exist_ok=True)
        
    report_files = sorted(
        [f for f in os.listdir(REPORTS_DIR) if f.endswith('.xlsx')],
        reverse=True
    )
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "reports": report_files,
        "app_name": settings.app_name,
        "settings": settings
    })

@app.get("/download/{filename}")
async def download_report(filename: str):
    """Gestiona la descarga segura de archivos Excel"""
    file_path = REPORTS_DIR / filename
    
    if file_path.exists():
        return FileResponse(
            path=str(file_path), 
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    raise HTTPException(status_code=404, detail="Archivo no encontrado")

# --- PANEL DE CONFIGURACIÓN ---

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    report_types = list(REPORT_MODELS.keys())

    return templates.TemplateResponse("settings.html", {
        "request": request,
        "settings": settings,
        "app_name": settings.app_name,
        "report_types": report_types
    })

@app.post("/settings")
async def update_settings(
    app_name: str = Form(...),
    company_name: str = Form(...),
    contact_email: str = Form(...),
    report_schedule: str = Form(...),
    db_type: str = Form(...),
    default_report_type: str = Form(...),
    # NUEVOS CAMPOS:
    default_days: int = Form(...),
    sheet_name: str = Form(...),
    included_columns: str = Form(...) # Recibimos el texto de las columnas
):
    # Convertir el texto de columnas "col1, col2" en una lista real ["col1", "col2"]
    columns_list = [c.strip() for c in included_columns.split(",")]

    # Crear el nuevo diccionario para el JSON respetando la estructura anidada
    new_config = {
        "app_name": app_name,
        "company_name": company_name,
        "contact_email": contact_email,
        "report_schedule": report_schedule,
        "db_type": db_type,
        "default_report_type": default_report_type,
        "report_settings": {
            "default_days": default_days,
            "sheet_name": sheet_name,
            "included_columns": columns_list
        }
    }

    # Guardar físicamente en el archivo
    with open("config/settings.json", "w") as f:
        json.dump(new_config, f, indent=4)

    html_content = f"""
    <script>
        alert('¡Configuración guardada! Reiniciando sistema...');
        window.location.href = '/settings';
    </script>
    """
    return HTMLResponse(content=html_content)

# --- ACCIONES MANUALES (API) ---

@app.post("/run-report")
async def run_report_manual(background_tasks: BackgroundTasks):
    """Lanza la generación y envío del reporte en segundo plano"""
    async def task():
        db = SessionLocal()
        try:
            report_service = ReportService(db)
            email_service = EmailService()
            path = report_service.get_report(report_type="ventas")
            if path:
                await email_service.send_report_email(file_path=path)
        finally:
            db.close()
    
    background_tasks.add_task(task)
    return {"status": "success", "message": "Proceso de reporte iniciado"}