"""
Shows and controls main menu of foods
"""

from typing import List, Optional, Dict, Any
from psycopg2.extras import DictRow

from core.logger import logger_app
from core.db_settings import execute_query

def get_today_menu() -> List[DictRow]:
    """
    Gets today's menu from menu_products
    """
    query = """
    SELECT mp.id AS menu_product_id, p.title, p.price, mp.amount, mp.created_at
    FROM menu_products mp
    JOIN products p ON mp.product_id = p.id
    WHERE mp.menu_date = CURRENT_DATE AND mp.amount > 0
    ORDER BY p.title"""
    return execute_query(query=query, fetch="all")

def food_availability(menu_product_id:int, amount:int)-> bool:
    """
    Checks the availability of food by checking its amount
    """
    query = """
    SELECT amount
    FROM menu_products
    WHERE id = %s
    AND menu_date = CURRENT_DATE"""
    params = (menu_product_id,)
    result = execute_query(query=query, params=params, fetch="one")
    if not result:
        return False
    return result["amount"] >= amount

def add_products_for_today_menu(product_id: int, amount: int) -> bool:
    """
    Admin adds products for today's menu
    """
    query = """
    INSERT INTO menu_products
    (product_id, amount, menu_date)
    VALUES (%s, %s, CURRENT_DATE)"""
    params = (product_id, amount,)
    execute_query(query=query, params=params)
    logger_app.info(f"Successfully added {amount} to {product_id} for today's menu")
    return True

def remove_products_from_today_menu(menu_product_id: int) -> bool:
    """
    Admin removes products from today's menu
    """
    query = """
    DELETE FROM menu_products
    WHERE id = %s
    AND menu_date = CURRENT_DATE"""
    params = (menu_product_id,)
    execute_query(query=query, params=params)
    logger_app.info(f"Successfully removed {menu_product_id} from today's menu")
    return True

def decrease_food_amount(menu_product_id: int, amount:int) -> bool:
    """
    Decrease foo amount after taking order
    """
    if food_availability(menu_product_id=menu_product_id, amount=amount):
        query = """
        UPDATE menu_products
        SET amount = amount - %s
        WHERE id = %s
        AND menu_date = CURRENT_DATE"""
        params = (amount, menu_product_id,)
        execute_query(query=query, params=params)
        logger_app.info(f"Successfully decreased {amount} from {menu_product_id}")
        return True
    else:
        logger_app.warning("Failed to decrease food amount. Food not enough")
        return False

def show_admin_today_menu()-> None:
    """
    Show menu for admin
    """
    menu = get_today_menu()
    if not menu:
        print("No food is available for today")
        return
    print("\\--=|Today's menu|=--//")
    for i in menu:
        print(f"{i['menu_product_id']} | {i['title']} | {i['price']} | {i['amount']}")

def show_user_today_menu() -> None:
    menu = get_today_menu()
    if not menu:
        print("No food is left for today. Woops")
        return
    print("\\--=|Today's menu|=--//")
    for i in menu:
        print(f"{i['menu_product_id']}. Name: {i['title']} |Price: {i['price']} |Amount left: {i['amount']}")