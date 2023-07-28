import base64
import nacl.secret
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from .file_cipher import File
from .name_cipher import Name

KEY_SIZE = 32 + 32 + 16 # scrypt生成密钥的长度
DEFAULT_SALT = b"\xA8\x0D\xF4\x3A\x8F\xBD\x03\x08\xA7\xCA\xB8\x3E\x58\x1F\x86\xB1" # rclone默认salt
# rclone密码加密密钥
PASSWD_CRYPT_KEY = b'\x9c\x93\x5b\x48\x73\x0a\x55\x4d\x6b\xfd\x7c\x63\xc8\x86\xa9\x2b\xd3\x90\x19\x8e\xb8\x12\x8a\xfb\xf4\xde\x16\x2b\x8b\x95\xf6\x38'

def passwd_deobscure(passwd: bytes) -> bytes:
    if not passwd:
        return b''
    if type(passwd) == str:
        passwd = bytes(passwd, 'utf-8')
    padding_num = 4 - len(passwd) % 4
    passwd = passwd + b'=' * padding_num
    try:
        passwd = base64.urlsafe_b64decode(passwd)
        crypter = AES.new(key = PASSWD_CRYPT_KEY, mode = AES.MODE_CTR,
                          initial_value = passwd[: 16], nonce = b'')
        return crypter.decrypt(passwd[16 :])
    except:
        ValueError('fail to deobscure passwd')

class Crypt:
    """
    rclone文件和名称加密/解密
    :param `passwd`: 密码, 对应rclone password
    :param `salt`: 对应rclone password2, 可不设
    :param `passwd_obscured`: 密码是否经过混淆
    """
    def __init__(self, passwd: str, salt: str = DEFAULT_SALT, passwd_obscured: bool = False) -> None:
        if type(passwd) == str:
            passwd = bytes(passwd, 'utf-8')
        if passwd_obscured:
            passwd = passwd_deobscure(passwd)
        if type(salt) == str:
            salt = bytes(salt, 'utf-8')
        if passwd_obscured and not (salt == DEFAULT_SALT):
            salt = passwd_deobscure(salt)
        key = scrypt(passwd, salt, KEY_SIZE, 16384, 8, 1)
        box = nacl.secret.SecretBox(key[:32])
        nameKey = key[32 : 64]
        nameTweak = key[64 :]
        cipher = AES.new(nameKey, AES.MODE_ECB)
        self.File = File(box)
        self.Name = Name(nameKey, nameTweak, cipher)