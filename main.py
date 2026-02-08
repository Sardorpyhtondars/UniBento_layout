# main.py

from auth.login import register, login, get_active_user, logout_all
from buffet.meals_menu import show_admin_today_menu, show_user_today_menu, add_products_for_today_menu, \
    remove_products_from_today_menu
from buffet.products import create_product, delete_product
from buffet.orders import create_order, get_user_orders, cancel_order
from buffet.timetable import get_timeslots
from utils.menus import auth_menu, admin_menu, user_menu
from utils.validators import validate_menu_choice, validate_amount, validate_slot


def main():
    print("Welcome to UniBento!")

    while True:
        print(auth_menu)
        choice = input("Tanlang: ")

        if not validate_menu_choice(choice, 3):
            print("Iltimos, to'g'ri raqam kiriting")
            continue

        if choice == "1":  # Login
            if login():
                user = get_active_user()
                print(f"Xush kelibsiz, {user['username']}!")
                if user['is_admin']:
                    admin_loop()
                else:
                    user_loop(user['id'])
            else:
                print("Login yoki parol xato")

        elif choice == "2":  # Register
            if register():
                print("Ro'yxatdan o'tdingiz. Endi login qiling")
            else:
                print("Ro'yxatdan o'tishda xatolik")

        elif choice == "3":  # Exit
            logout_all()
            print("Chiqdingiz. Xayr!")
            break


def admin_loop():
    while True:
        print(admin_menu)
        choice = input("Tanlang: ")
        if not validate_menu_choice(choice, 9):
            print("Iltimos, to'g'ri raqam kiriting")
            continue

        if choice == "1":
            print("Barcha mahsulotlar:")
        elif choice == "2":
            title = input("Title: ")
            price = input("Price: ")
            description = input("Description: ")
            create_product(title, price, description)
            print("Mahsulot yaratildi!")

        elif choice == "3":
            product_id = input("Product ID: ")
            if product_id.isdigit():
                delete_product(int(product_id))
                print("Mahsulot o'chirildi!")
            else:
                print("ID butun son bo'lishi kerak")

        elif choice == "4":
            show_admin_today_menu()

        elif choice == "5":
            product_id = input("Product ID: ")
            amount = input("Amount: ")
            if product_id.isdigit() and validate_amount(amount):
                add_products_for_today_menu(int(product_id), int(amount))
                print("Mahsulot menyuga qo'shildi")
            else:
                print("Noto'g'ri kiritildi")

        elif choice == "6":
            menu_product_id = input("Menu Product ID: ")
            if menu_product_id.isdigit():
                remove_products_from_today_menu(int(menu_product_id))
                print("Mahsulot menyudan o'chirildi")
            else:
                print("ID butun son bo'lishi kerak")

        elif choice == "7":
            print("Bu joyga buyurtmalarni ko'rsatish funksiyasini yozish kerak")

        elif choice == "8":
            print("Bu joyga order statusini o'zgartirish funksiyasini yozish kerak")

        elif choice == "9":
            logout_all()
            print("Admin menyudan chiqildi")
            break


def user_loop(user_id: int):
    while True:
        print(user_menu)
        choice = input("Tanlang: ")
        if not validate_menu_choice(choice, 5):
            print("Iltimos, to'g'ri raqam kiriting")
            continue

        if choice == "1":

            show_user_today_menu()

        elif choice == "2":

            menu_product_id = input("Menu Product ID: ")
            amount = input("Amount: ")
            timeslots = get_timeslots()
            print("Available slots:")
            for slot in timeslots:
                print(f"{slot['id']} | {slot['start_time']} - {slot['end_time']} | Seats: {slot['seats']}")
            slot_id = input("Slot ID: ")


            if all([
                menu_product_id.isdigit(),
                validate_amount(amount),
                validate_slot(slot_id, [s['id'] for s in timeslots])
            ]):
                create_order(user_id, int(menu_product_id), int(amount), int(slot_id), "in_hall")
                print("Buyurtma yaratildi!")
            else:
                print("Noto'g'ri kiritildi")

        elif choice == "3":
            # Show my orders
            orders = get_user_orders(user_id)
            print("Sizning buyurtmalaringiz:")
            for o in orders:
                print(f"{o['id']} | {o['title']} | {o['amount']} | {o['status']} | {o['order_type']}")

        elif choice == "4":
            # Cancel order
            order_id = input("Order ID: ")
            if order_id.isdigit():
                cancel_order(user_id, int(order_id))
                print("Buyurtma bekor qilindi")
            else:
                print("ID butun son bo'lishi kerak")

        elif choice == "5":
            logout_all()
            print("Foydalanuvchi menyudan chiqdi")
            break


if __name__ == "__main__":
    main()