import nacl.secret
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from .file_cipher import File
from .name_cipher import Name

KEY_SIZE = 32 + 32 + 16 # scrypt生成密钥的长度
DEFAULT_SALT = b"\xA8\x0D\xF4\x3A\x8F\xBD\x03\x08\xA7\xCA\xB8\x3E\x58\x1F\x86\xB1" # rclone默认salt

class Crypt:
    """
    rclone文件和名称加密/解密
    :param `passwd`: 密码, 对应rclone password
    :param `salt`: 对应rclone password2, 可不设
    """
    def __init__(self, passwd: bytes | str, salt: bytes | str = DEFAULT_SALT) -> None:
        if type(passwd) == str:
            passwd = bytes(passwd, 'utf-8')
        if type(salt) == str:
            salt = bytes(salt, 'utf-8')
        key = scrypt(passwd, salt, KEY_SIZE, 16384, 8, 1)
        box = nacl.secret.SecretBox(key[:32])
        nameKey = key[32 : 64]
        nameTweak = key[64 :]
        cipher = AES.new(nameKey, AES.MODE_ECB)
        self.File = File(box)
        self.Name = Name(nameKey, nameTweak, cipher)