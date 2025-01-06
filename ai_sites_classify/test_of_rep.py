from get_domain import get_domain

checked_domains = []

while True:
    current_domain = get_domain(input())
    if not current_domain in checked_domains:
        print("OK")
        checked_domains.append(current_domain)
    else:
        print("PASS")

