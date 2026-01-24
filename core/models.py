user = """
        CREATE TABLE IF NOT EXISTS users
        (
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
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
            date_of_menu TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
            amount INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) \
            """

timetable = """
        CREATE TABLE IF NOT EXISTS timetable
        (
            id BIGSERIAL PRIMARY KEY,
            start_time VARCHAR(255) NOT NULL,
            end_time VARCHAR(255) NOT NULL,
            seats INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) \
            """
orders = """
        CREATE TABLE IF NOT EXISTS orders
        (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
            menu_id BIGINT REFERENCES menu_products(id),
            amount INTEGER NOT NULL,
            timeslot_id BIGINT REFERENCES timetable(id),
            status VARCHAR(255) NOT NULL,
            order_type VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) \
            """