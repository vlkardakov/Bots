def decode(binary_string):
    ascii_string = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        try:
            ascii_string += chr(int(byte, 2))
        except ValueError:
            return "Неправильная кодировка."
    return ascii_string


if __name__ == "__main__":
    try:
        with open("input.txt", "r") as input_file:
            binary_data = input_file.read().strip()

        decoded_text = decode(binary_data)

        with open("output.txt", "w") as output_file:
            output_file.write(decoded_text)
    except Exception as e:
        print(f"ОШИБКА: {e}")