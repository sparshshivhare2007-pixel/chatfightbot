from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.reset_manager import reset_today, reset_week
import datetime

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(reset_today, "cron", hour=0, minute=0)
    scheduler.add_job(reset_week, "cron", day_of_week="mon", hour=0, minute=0)
    scheduler.start()
