# utils/validators.py

from datetime import datetime, time

def is_integer(value: str) -> bool:
    """
    Tekshiradi, value butun sonmi
    """
    return value.isdigit()


def validate_menu_choice(choice: str, max_option: int) -> bool:
    """
    Tekshiradi, choice 1..max_option oralig'ida bo'lsa True, aks holda False
    """
    if not choice.isdigit():
        return False
    choice_int = int(choice)
    return 1 <= choice_int <= max_option


def validate_amount(amount: str) -> bool:
    """
    Tekshiradi, ovqat miqdori ijobiy son (>0) bo'lsa True
    """
    if not amount.isdigit():
        return False
    return int(amount) > 0


def validate_slot(slot_id: str, available_slots: list[int]) -> bool:
    """
    Tekshiradi, slot_id available_slots ichida bo'lsa True
    """
    if not slot_id.isdigit():
        return False
    return int(slot_id) in available_slots


def validate_future_time(time_str: str) -> bool:
    """
    Tekshiradi, time_str hozirgi vaqtdan keyin bo'lsa True
    time_str format: 'HH:MM'
    """
    try:
        slot_time = datetime.strptime(time_str, "%H:%M").time()
        now_time = datetime.now().time()
        return slot_time > now_time
    except ValueError:
        return False