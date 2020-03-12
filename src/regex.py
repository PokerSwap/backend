import re

def hard_rock(text):
    buyin = re.search(r'buy[\s\-_]*in\D{1,5}([0-9,\.]+)', text, re.IGNORECASE)
    buyin = buyin and buyin.group(1)
    seat = re.search(r'seat\D+\d+\D+(\d+)', text, re.IGNORECASE)
    seat = seat and seat.group(1)
    table = re.search(r'seat\D+(\d+)', text, re.IGNORECASE)
    table = table and table.group(1)
    name = re.search(r'name[ :,]+([a-zA-Z() ]+)', text, re.IGNORECASE)
    name = name and name.group(1)
    date = re.search(r'received[ :\w]+\n(.*)\n',text, re.IGNORECASE)
    date = date and date.group(1)
    id = re.search(r'player\D+(\d+)', text, re.IGNORECASE)
    id = id and id.group(1)
    cas = re.search(r'^([^\n]+)\n([^\n]+)', text, re.IGNORECASE)
    casino = cas and f'{cas.group(1)} {cas.group(2)}'
    return {
        'casino': casino,
        'player name': name,
        'player id': id,
        'buyin amount': buyin,
        'seat': seat,
        'table': table,
        'receipt timestamp': date
    }