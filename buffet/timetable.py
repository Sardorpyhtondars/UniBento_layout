"""
Manages seats and time slots
"""

from typing import List,Optional, Dict, Any
from psycopg2.extras import DictRow

from core.db_settings import execute_query
from core.logger import logger_app

def create_timeslot(start_time: str, end_time:str, seats:str) ->bool:
    """
    Admin creates a timeslot with given start and end time
    """
    query = """
    INSERT INTO timeslot (start_time, end_time, seats)
    VALUES (%s, %s, %s)"""
    params = (start_time, end_time, seats)
    execute_query(query=query, params=params)
    logger_app.info("Timeslot created")
    return True

def get_timeslots() -> List[DictRow]:
    """
    Admin gets timeslots with given start and end time
    """
    query = """
    SELECT * FROM timeslots
    ORDER BY start_time"""
    return execute_query(query=query, fetch="all")

def check_seat_availability(timeslot_id:int)->bool:
    """
    Admin checks if seat availability is available
    """
    query = """
    SELECT seats FROM timeslots
    WHERE id = %s"""
    params = (timeslot_id,)
    result = execute_query(query=query, params=params)
    if not result:
        return False

    return result["seats"]>0

def decrease_seat_number(timeslot_id:int)->bool:
    """
    Decreases seat in a given timeslot after an order
    """
    if not check_seat_availability(timeslot_id):
        logger_app.warning("No seats left")
        return False

    query = """
    UPDATE timeslots
    SET seats = seats - 1
    WHERE id = %s"""
    params = (timeslot_id,)
    execute_query(query=query, params=params)
    logger_app.info(f"Seats number in a {timeslot_id} timeslot decreased")
    return True