#library.py
import des
from time import sleep
import sys 

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def splitIntoGroups(string,length):
    results = []
    loc = 0
    temp = ""
    while(loc < len(string)):
        temp += string[loc]
        loc += 1
        if loc % length == 0:
            results.append(temp)
            temp = ""
    return results

def decrypt(self, ciphertext):
    plaintext_int = pow(ciphertext, self.d, self.n)
    try:
        plaintext = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big').decode('utf-8')
        return plaintext
    except UnicodeDecodeError:
        return plaintext_int

def encrypt(message):
    ki = des.DES()
    binary = text_to_bits(message)

    entries = splitIntoGroups(binary,8)

    encryptedEntries = []
    for i in range(len(entries)):
        encryptedMessage = ki.Encryption(entries[i])
        encryptedEntries.append(encryptedMessage)
    finalEncryptedMessage = "".join(encryptedEntries)
    return finalEncryptedMessage

def sending():
    print("\nSending ",end = "")
    for j in range(5):
        sleep(0.4)
        print(".", end = "")
        sys.stdout.flush()
    print(' SENT')