import os
import json
from pathlib import Path
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.services.report_service import ReportService, REPORT_MODELS, get_columns_for_model
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

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Muestra el historial de reportes ordenados por fecha de creación"""
    if not REPORTS_DIR.exists():
        REPORTS_DIR.mkdir(exist_ok=True)
        
    files = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.xlsx')]
    
    files_with_time = []
    for f in files:
        file_path = REPORTS_DIR / f
        files_with_time.append((f, os.path.getmtime(file_path)))
    
    files_with_time.sort(key=lambda x: x[1], reverse=True)
    
    report_files = [f[0] for f in files_with_time]
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "reports": report_files,
        "app_name": settings.app_name,
        "settings": settings
    })

@app.get("/download/{filename}")
async def download_report(filename: str):
    file_path = REPORTS_DIR / filename
    if file_path.exists():
        return FileResponse(
            path=str(file_path), 
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    raise HTTPException(status_code=404, detail="Archivo no encontrado")

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    report_types = list(REPORT_MODELS.keys())
    all_columns = {t: get_columns_for_model(t) for t in report_types}
    
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "settings": settings,
        "app_name": settings.app_name,
        "report_types": report_types,
        "all_columns": all_columns
    })

@app.post("/settings")
async def update_settings(
    app_name: str = Form(...),
    company_name: str = Form(...),
    contact_email: str = Form(...),
    report_schedule: str = Form(...),
    db_type: str = Form(...),
    default_report_type: str = Form(...),
    default_days: int = Form(...),
    sheet_name: str = Form(...),
    included_columns: List[str] = Form(...)
):
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
            "included_columns": included_columns
        }
    }

    with open("config/settings.json", "w") as f:
        json.dump(new_config, f, indent=4)

    html_content = """
    <script>
        alert('✅ ¡Configuración guardada! El sistema se está reiniciando...');
        window.location.href = '/settings';
    </script>
    """
    return HTMLResponse(content=html_content)

@app.post("/run-report")
async def run_report_manual():
    """Ejecuta el proceso y responde SOLO cuando el email se ha enviado"""
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        email_service = EmailService()
        
        path = report_service.get_report(report_type=settings.default_report_type)
        
        if path:
            await email_service.send_report_email(file_path=path)
            return {"status": "success", "message": "Email enviado correctamente"}
        else:
            raise HTTPException(status_code=400, detail="No hay datos para el reporte")
            
    except Exception as e:
        print(f"Error en ejecución manual: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()