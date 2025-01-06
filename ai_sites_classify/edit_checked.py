from array import array

from massive import edit_array

from main import load_checked, save_checked

array = edit_array(load_checked())

print(type(array))

if 'list' in str(type(array)):
    print(f"СПИСОК = {array}")
    with open("checked_domains.txt", "w") as f:
        f.write(f"{array}")