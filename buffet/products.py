"""
Manages food products if the user is admin
"""

from typing import List,Optional, Dict, Any
from psycopg2.extras import DictRow

from core.db_settings import execute_query
from core.logger import logger_app

def create_product(title: str, price: str, description: str) -> bool:
    """
    Admin creates a new product
    """
    query = """
    INSERT INTO products (title, price, description)
    VALUES (%s, %s, %s)"""
    params = (title, price, description)
    execute_query(query=query, params=params)
    logger_app.info(f"Product created successfully: {title}, {price}, {description}")
    return True

def update_product(product_id: int, title: str, price: str, description:str) -> bool:
    """
    Admin updates a product
    """
    query = """
    UPDATE products
    SET title = %s, price = %s, description = %s
    WHERE id = %s"""
    params = (title, price, description, product_id)
    execute_query(query=query, params=params)
    logger_app.info(f"Product updated successfully: {title}, {price}, {description}")
    return True

def delete_product(product_id: int) -> bool:
    """
    Admin deletes a product
    """
    query = """
    DELETE FROM products
    WHERE id = %s"""
    params = (product_id,)
    execute_query(query=query, params=params)
    logger_app.info(f"Product deleted successfully: {product_id}")
    return True

def get_all_products(product_id: int, title:str, price:str, description:str) -> List[DictRow]:
    """
    Admin gets all products
    """
    query = """
    SELECT * FROM products
    ORDER BY id"""
    params = (product_id,)
    return execute_query(query=query, params=params)