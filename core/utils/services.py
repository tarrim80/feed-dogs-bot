from datetime import datetime, time, timedelta

from core.settings import settings


async def get_estimated_time_to_feed() -> timedelta:
    now = datetime.now().time()
    morning_time = time(hour=int(settings.mode.first_time))
    evening_time = time(hour=int(settings.mode.second_time))
    if morning_time < now < evening_time:
        return datetime.combine(
            date=datetime.today(), time=evening_time
        ) - datetime.combine(date=datetime.today(), time=now)
    return datetime.combine(
        date=datetime.today(), time=morning_time
    ) - datetime.combine(date=datetime.today(), time=now)


async def get_estimated_time_formatted():
    estimated_time = await get_estimated_time_to_feed()
    est_hours, remainder = divmod(estimated_time.seconds, 3600)
    est_minutes, _ = divmod(remainder, 60)
    if est_hours > 0:
        return f"{est_hours:02d} часов, {est_minutes:02d} минут"
    return f"{est_minutes:02d} минут"
