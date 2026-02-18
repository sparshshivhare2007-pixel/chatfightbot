from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import redis_client

scheduler = AsyncIOScheduler()


def reset_today():
    for key in redis_client.scan_iter("*:today"):
        redis_client.delete(key)


def reset_week():
    for key in redis_client.scan_iter("*:week"):
        redis_client.delete(key)


def start_scheduler():
    scheduler.add_job(reset_today, "cron", hour=0, minute=0)
    scheduler.add_job(reset_week, "cron", day_of_week="mon", hour=0, minute=0)
    scheduler.start()
