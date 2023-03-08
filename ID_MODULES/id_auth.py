def is_valid_id(id):
    if len(id) > 9:
        raise ValueError("ERROR: INVALID ID LENGTH")

    if len(id) != 9:
        id = fill_id(id)

    x = "121212121"
    sum = 0

    for index in range(len(x)):
        mult = int(id[index]) * int(x[index])

        if mult > 9:
            sum += mult % 10 + mult // 10
        else:
            sum += mult

    return sum % 10 == 0


def get_auth_digit(id_val):
    x = "12121212"

    if len(id_val) != len(x):
        raise ValueError("ERROR: INVALID ID LENGTH")

    sum = 0

    for index in range(len(id_val)):
        mult = int(id_val[index]) * int(x[index])

        if mult > 9:
            sum += mult % 10 + mult // 10
        else:
            sum += mult

    round_to_nearest = 10
    val = round(sum / round_to_nearest) * round_to_nearest

    return val - sum


def fill_id(id, wanted_len=9):
    while len(id) < abs(wanted_len):
        id = "0" + id

    return id
