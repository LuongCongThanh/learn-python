import re

def is_valid_credit_card(card):
    if not re.match(r'^[456]', card):
        return "Invalid"

    if not re.match(r'^[\d-]+$', card):
        return "Invalid"

    clean_card = card.replace("-", "")
    if len(clean_card) != 16:
        return "Invalid"

    if re.search(r'(\d)\1{3,}', clean_card):
        return "Invalid"

    if '-' in card and not re.match(r'^\d{4}-\d{4}-\d{4}-\d{4}$', card):
        return "Invalid"

    return "Valid"

N = int(input().strip())
if not (0 < N < 100):
    print("Invalid input: N must be between 1 and 99")
    exit()

for _ in range(N):
    card = input().strip()
    print(is_valid_credit_card(card))
