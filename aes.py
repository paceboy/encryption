
from io import StringIO
from Crypto.Cipher import AES
import base64


def expand(s):
    """
    扩充到32位的长度
    :param s: 二进制字符串
    :return: 扩充后的字符串
    """
    return s + b"\0" * (AES.key_size[2] - len(s))


def truncate(s):
    """
    截断到32位的长度
    :param s:二进制字符串
    :return:截断后的字符串
    """
    return s[:AES.key_size[2]]


def pad(s):
    """
        简单的补齐字符串到某个长度
    """
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def unpad(s):
    """
    删除掉填充字符'\0'
    :param s:
    :return:
    """
    return s.rstrip("\0").lstrip("\0")


def encrypt_file(input_file, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    buf = StringIO()
    with open(input_file, "rb") as fh:
        # Read a line as a multiple of the AES block size.
        for line in fh:
            # pad (to match block size) -> encrypt -> b64encode (to make it suitable for urls)
            pad(line)
            encrypted = cipher.encrypt(pad(line))
            # Use the URL safe version of the b64 encoding
            b64_encoded = base64.urlsafe_b64encode(encrypted)
            buf.write(b64_encoded.decode("utf-8"))
            buf.write("\n")
    return buf


def decrypt_file(input_file, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    buf = StringIO()
    with open(input_file, "rb") as fh:
        for line in fh:
            # Reverse the process
            # b64decode -> decrypt -> unpad
            # Use the URL safe version of the b64 decoding
            decrypted = unpad(cipher.decrypt(base64.urlsafe_b64decode(line)).decode("utf-8"))
            buf.write(decrypted)
    return buf
