from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.logger import logger

scheduler = AsyncIOScheduler()


def reset_today():
    # No reset needed (Mongo handles date filtering automatically)
    logger.info("Daily reset check completed.")


def reset_week():
    # No reset needed (Mongo handles date filtering automatically)
    logger.info("Weekly reset check completed.")


def start_scheduler():
    scheduler.add_job(
        reset_today,
        "cron",
        hour=0,
        minute=0
    )

    scheduler.add_job(
        reset_week,
        "cron",
        day_of_week="mon",
        hour=0,
        minute=0
    )

    scheduler.start()
