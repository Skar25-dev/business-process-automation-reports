from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import SessionLocal
from app.services.report_service import ReportService
from app.services.email_service import EmailService
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def scheduled_report_job():
    logger.info("Robot: Iniciando tarea programada...")
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        path = report_service.get_report(report_type=settings.default_report_type)

        if path:
            email_service = EmailService()
            await email_service.send_report_email(file_path=path)
            logger.info("Reporte enciado con éxito.")
        
        else:
            logger.warning("Robot: No hay datos para el reporte de hoy.")
    except Exception as e:
        logger.error(f"Robot: Error en la tarea: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = AsyncIOScheduler()
    hour, minute = settings.report_schedule.split(":")

    scheduler.add_job(
        scheduled_report_job,
        'cron',
        hour=hour,
        minute=minute,
        id="daily_report_job"
    )

    scheduler.start()
    logger.info(f"Scheduler iniciado: Reporte programado todos los días a las {settings.report_schedule}")
    return scheduler

def reload_scheduler(new_hour: str):
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    hour, minute = new_hour.split(":")
