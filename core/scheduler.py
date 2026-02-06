# core/schedular.py

from datetime import datetime, timedelta, time
from core.db_settings import execute_query

# Konfiguratsiya
START_TIME = time(11, 0)  # 11:00
END_TIME = time(15, 0)  # 15:00
SLOT_DURATION_MIN = 30  # 30 minut
MAX_SEATS = 200


def create_daily_slots():
    """
    Bugungi kun uchun slotlarni yaratadi, agar mavjud bo'lmasa
    """
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Avval mavjud slotlarni tekshirish
    query_check = "SELECT * FROM timetable WHERE start_time >= %s AND start_time < %s"
    existing_slots = execute_query(query=query_check, params=(START_TIME, END_TIME), fetch="all") or []

    if existing_slots:
        print("Bugungi slotlar allaqachon mavjud")
        return

    # Slotlarni generatsiya qilish
    current_datetime = datetime.combine(datetime.today(), START_TIME)
    end_datetime = datetime.combine(datetime.today(), END_TIME)

    while current_datetime < end_datetime:
        slot_start = current_datetime.time()
        slot_end = (current_datetime + timedelta(minutes=SLOT_DURATION_MIN)).time()

        # DB ga yozish
        query_insert = """
            INSERT INTO timetable (start_time, end_time, seats)
            VALUES (%s, %s, %s)
        """
        params = (slot_start, slot_end, MAX_SEATS)
        execute_query(query=query_insert, params=params)

        print(f"Slot yaratildi: {slot_start} - {slot_end}, Seats: {MAX_SEATS}")

        current_datetime += timedelta(minutes=SLOT_DURATION_MIN)


def get_available_slots() -> list[tuple[int, str]]:
    """
    Hozirgi vaqtdan keyingi slotlarni qaytaradi
    return: list of tuples (slot_id, 'HH:MM-HH:MM')
    """
    now = datetime.now().time()
    query = "SELECT id, start_time, end_time, seats FROM timetable ORDER BY start_time"
    slots = execute_query(query=query, fetch="all") or []

    available = []
    for slot in slots:
        slot_id = slot["id"]
        start_time = slot["start_time"]
        end_time = slot["end_time"]
        seats = slot["seats"]

        if seats > 0 and start_time > now:
            available.append((slot_id, f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"))

    return available