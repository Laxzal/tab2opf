
def remove_niqqud_from_string(my_string):
    return ''.join(['' if 1456 <= ord(c) <= 1479 else c for c in my_string])
