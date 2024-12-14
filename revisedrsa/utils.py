import binascii


def text_to_bits(text):
    return ''.join(format(ord(i), '08b') for i in text)


def bits_to_text(bits):
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))


def split_into_groups(data, length):
    return [data[i:i+length] for i in range(0, len(data), length)]
