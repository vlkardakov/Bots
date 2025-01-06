from massive import edit_array

from main import load_verified

array = edit_array(load_verified())

print(type(array))

if 'list' in str(type(array)):
    print(f"СПИСОК = {array}")
    with open("verified_domains.txt", "w") as f:
        f.write(f"{array}")