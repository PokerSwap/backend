

def hard_rock(text):
    buyin = re.search(r'buy[\s\-_]*in\D{1,5}([0-9,\.]+)', text, re.IGNORECASE)
    buyin = buyin and buyin.group(0)
    seat = re.search(r'seat\D{,5}([0-9]+)', text, re.IGNORECASE)
    seat = seat and seat.group(0)
    table = re.search(r'table\D{,5}([0-9]+)', text, re.IGNORECASE)
    table = table and table.group(0)
    name = re.search(r'name[ :,]+([a-zA-Z() ]+)', text, re.IGNORECASE)
    name = name and name.group(0)
    account_number = '' # get account_number
    return {
        'player_name': name,
        'date_on_receipt': None,
        'buyin_amount': buyin,
        'seat': seat,
        'table': table,
        'account_number': None
    }