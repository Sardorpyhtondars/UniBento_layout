"""
Creates and manages orders
"""

from typing import List, Optional, Dict, Any
from psycopg2.extras import DictRow

from buffet.meals_menu import food_availability, decrease_food_amount
from core.logger import logger_app
from core.db_settings import execute_query

def create_order(user_id: int, menu_product_id: int, amount: int, timeslot_id: int, order_type: str) -> bool:
    """
    Creates a new order
    """
    if not food_availability(menu_product_id, amount):
        logger_app.warning("Food not available")
        return False
    query = """
    INSERT INTO orders (user_id, menu_product_id, amount, timeslot_id, status, order_type)
    VALUES (%s, %s, %s, %s, 'pending', %s)"""
    params = (user_id, menu_product_id, amount, timeslot_id, order_type)
    execute_query(query=query, params=params)
    decrease_food_amount(menu_product_id, amount)
    logger_app.info(f"Order created by {user_id}")
    return True

def cancel_order(user_id: int, order_id: int)-> None:
    """
    Cancels an order by its id
    """
    query = """
    UPDATE orders
    SET status = 'canceled'
    WHERE id = %s"""
    params = (order_id,)
    execute_query(query=query, params=params)
    logger_app.info(f"Order canceled by user: {user_id}, order_id:{order_id}")

def complete_order(user_id: int, order_id: int) -> None:
    """
    Completes an order by its id
    """
    query = """
    UPDATE orders
    SET status = 'completed'
    WHERE id = %s"""
    params = (order_id,)
    execute_query(query=query, params=params)
    logger_app.info(f"Order completed by user: {user_id}, order_id:{order_id}")

def get_user_orders(user_id: int) -> List[DictRow]:
    """
    Gets all orders that user has made
    """
    query = """
    SELECT o.id, p.title, o.amount, o.status, o.order_type, t.start_time, t.end_time, o.created_at
    FROM orders o
    JOIN menu_products mp ON o.menu_product_id = mp.id
    JOIN products p ON mp.product_id = p.id
    LEFT JOIN timetable t ON o.timeslot_id = t.id
    WHERE o.user_id = %s
    ORDER BY o.created_at DESC"""
    params = (user_id,)
    return execute_query(query=query, params=params, fetch="all")