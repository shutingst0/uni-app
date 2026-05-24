def input_text(message):
    try:
        return input(message)
    except EOFError:
        return ""


def pad_number(number, length):
    return str(number).zfill(length)


def grade_from_mark(mark):
    if mark < 50:
        return "Z"
    elif mark < 65:
        return "P"
    elif mark < 75:
        return "C"
    elif mark < 85:
        return "D"
    else:
        return "HD"
