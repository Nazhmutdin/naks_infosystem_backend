from re import fullmatch


def validate_insert(v: str) -> bool:
    if fullmatch(r"В[0-9]", v):
        return True
    
    return False


def validate_method(v: str) -> bool:
    if fullmatch(r"[A-Яа-я]+", v):
        return True
    
    return False


def validate_certification_number(v: str) -> bool:
    if fullmatch(r"[A-Я]+-[0-9A-Я]+-[IV]+-[0-9]{5}", v):
        return True
    
    return False


def validate_name(v: str) -> bool:
    if fullmatch(r"[A-ЯA-Za-zа-я ]+", v):
        return True
    
    return False
