"""
Database table for UniBento project
"""

user = """
        CREATE TABLE IF NOT EXISTS users
        (
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            is_login BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) \
            """

products = """
        CREATE TABLE IF NOT EXISTS products
        (
            id BIGSERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) \
            """

menu_products = """
        CREATE TABLE IF NOT EXISTS menu_products
        (
            id BIGSERIAL PRIMARY KEY,
            menu_date DATE NOT NULL,
            product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
            amount INTEGER NOT NULL CHECK (amount > 0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) \
            """

timeslots = """
        CREATE TABLE IF NOT EXISTS timetable
        (
            id BIGSERIAL PRIMARY KEY,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            seats INTEGER NOT NULL CHECK (seats > 0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) \
            """
orders = """
        CREATE TABLE IF NOT EXISTS orders
        (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
            menu_product_id BIGINT REFERENCES menu_products(id) ON DELETE CASCADE,
            amount INTEGER NOT NULL CHECK (amount > 0),
            timeslot_id BIGINT REFERENCES timeslots(id),
            status VARCHAR(255) NOT NULL, -- pending | canceled | completed
            order_type VARCHAR(255) NOT NULL, -- in_hall | take_away
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) \
            """