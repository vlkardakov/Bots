def decrypt_message(encrypted_message):
    decrypted_message = ""
    for char in encrypted_message:
        if 'a' <= char <= 'z':
            decrypted_char = chr(((ord(char) - ord('a') - 3) % 26) + ord('a')) # ROT3 Caesar cipher
        elif 'A' <= char <= 'Z':
            decrypted_char = chr(((ord(char) - ord('A') - 3) % 26) + ord('A'))  # ROT3 Caesar cipher
        else:
            decrypted_char = char
        decrypted_message += decrypted_char
    return decrypted_message


if __name__ == "__main__":
        with open("signal.txt", "r") as input_file:
            encrypted_message = input_file.read()

        decrypted_message = decrypt_message(encrypted_message)

        with open("decoded.txt", "w") as output_file:
            output_file.write(decrypted_message)
