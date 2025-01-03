
from Crypto.Cipher import AES
from Crypto import Random
import base64
import aes
import sys

def encrypt():
    # 加密
    encrypted = aes.encrypt_file("decrypted.txt", key, iv)
    print("Encrypted lines:")
    print(encrypted.getvalue())

def decrypt():
    # 解密
    decrypted = aes.decrypt_file("encrypted.txt", key, iv)
    print("\n")
    print("Decrypted lines are:")
    print(decrypted.getvalue())

def encryptAndDecrypt():
    """
    加解密
    :return:
    """
    # Encrypt the file
    encrypted = aes.encrypt_file("decrypted.txt", key, iv)
    print("Encrypted lines:")
    print(encrypted.getvalue())

    # Write the encrypted lines into a file
    with open("encrypted.txt", "wb") as fh:
        fh.write(encrypted.getvalue().encode("utf-8"))

    # Decrypt the encrypted file
    decrypted = aes.decrypt_file("encrypted.txt", key, iv)
    print("\n")
    print("Decrypted lines are:")
    print(decrypted.getvalue())

    # Compare the two
    with open("decrypted.txt", "r") as fh:
        clear_lines = [line.strip() for line in fh.readlines()]
    decrypted_lines = decrypted.getvalue().strip().split("\n")

    # check assertions
    assert len(clear_lines) == len(decrypted_lines), "%d vs %d" % (len(clear_lines), len(decrypted_lines))

    for i in range(0, len(clear_lines)):
        assert str(clear_lines[i]) == str(decrypted_lines[i]), "%s vs %s" % (clear_lines[i], decrypted_lines[i])

    print("Encrypted then decrypted and files match!")


if __name__ == "__main__":
    if len(sys.argv[1]) == 0:
        key = "own passwd, need remember"
    else:
        key = sys.argv[1]

    key = key.encode("utf-8")
    if len(key) > 32:
        key = aes.truncate(key)
    else:
        key = aes.expand(key)

    # Instead of a static key, create a key at random
    # key = Random.new().read(256//8)

    # iv = "I6V8HN5DMUPM4AES".encode("utf-8")
    # 需要记住自己的iv，iv的长度为16位
    iv = "abcdefghijklmnop".encode("utf-8")
    # Instead of a static IV, create a random IV
    # The IV needs to be the block size
    # iv = Random.new().read(AES.block_size)

    print("Key is %s" % base64.b64encode(key))
    print("IV is %s" % base64.b64encode(iv))

    print("IV is %s" % iv)

    print("\n")
    # 加解密
    encryptAndDecrypt()

    # 加密
    encrypt()

    # 解密
    decrypt()





