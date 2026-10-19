import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.scheduler_service import scheduled_report_job

async def test_scheduler_loop():
    print("Probando el Scheduler (Se ejecutará cada minuto)...")
    print("Presiona Ctrl+C para detener.")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_report_job, 'cron', minute='*')
    scheduler.start()

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    
if __name__ == "__main__":
    asyncio.run(test_scheduler_loop())