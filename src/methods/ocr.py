

def hard_rock(msg):
    buyin = re.search(r'buy[\s\-_]*in\D{1,5}([0-9,\.]+)', msg, re.IGNORECASE)
    buyin = buyin and buyin.group(1)
    seat = re.search(r'seat\D{,5}([0-9]+)', msg, re.IGNORECASE)
    seat = seat and seat.group(1)
    table = re.search(r'table\D{,5}([0-9]+)', msg, re.IGNORECASE)
    table = table and table.group(1)
    name = re.search(r'name[ :,]+([a-zA-Z() ]+)', msg, re.IGNORECASE)
    name = name and name.group(1)
    account_number = '' # get account_number
    return {
        'name': name,
        'buyin': buyin,
        'seat': seat,
        'table': table,
        'account_number': ''
    }