import pytest
from src.rclone import Crypt
from src.rclone.file_cipher import byte_increment, nonce_increment, nonce_add

crypt_with_passwd2 = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')
crypt_without_passwd2 = Crypt('Z2rCKxxvrm6pQMW')
crypt_with_passwd2_obscure = Crypt('SpnX0yEFxpNJjo9bxd3xAlVoXA7F4cr3C0SA-zmfzw', 'ziWH7jKYerB6o5vHnaXAvISTguFD6ZFJFbhT3BlLVQ', True)
crypt_without_passwd2_obscure = Crypt('MgfGDnK6S3la2nrxfSx6Qk01oTyErIXvu_pRrnPfLw', passwd_obscured = True)

nonce = b'{\xed\xa2\xf0>g\xfc\xab\x10\xe8\xc6\xc6\xad\xcd4\xdeB\xbd\xdcx\xd2v\x1a\xc1'
origin_bytes = b"\xbc\x87\x8b\xd2\xa1u|\x8e'\xa6\xa5\xa6\xbd\xcc\x83\xe1\xde1\xdfqL\xae\x1eG\r\x1b\xfa\x1b\x81Y\xeb\x87B\x12\xff\xbe\xee\x9f\x02\xfe\x95\xb5\x84\t\xb5d\x01\xd9ot\xdah\x98T\xec|k\x80z\x9a{\n\xb89x\x96\xdf\x01\x0f\xda1\xed\xf5\x13\xc1\xbe\x9f,f\xb1\x88\xcd\n\xb6\x89F\xca\xff\x92\xbeF;\x04^-\x11\xe9B\xe9/"
encrypted_with_passwd2 = b')\x16e\x10\x8e\xc3}\xf0\xc6 \xa4\x9b+\x8b\xb8P#\xc8\x8b\xe4\xd4=\x06\xb3\xfc\xec\xc5\xdfr\x1a\x0cmU\x969\xc7Y\xf8D3\xe2\xfbKi+\xed\x0c\xfd\xc0\xcfC\xfe\xfc\xaf\x02\xe0TU\r-\xf7\x1d\xc6\xaa\xb7\xfb\xfe\xc3\xdf\xfe\xecd6\x1dE\xf5\x0fS>\x9f\x16z\x81~\xffwr{\xa8\x08\x1e\xd1\xe5\xa8\x94x\x94\xf3\x1fn\x1cH\xd5dn\x80\xf3R\x96\x8a\x0c$\xd5\x81|\xcf'
encrypted_without_passwd2 = b"W\xfct'_\xe3\xbeN\xed\xaakySOB\xadlL\x11\xc8\xe8e\xe4\x1e&\x1a&t\x06;\xff^\xa8OX\xea\xc5]q\xd1\xed\xe67LY\xeb\xbc&\xbeK\x00\x98c\xcf\xde'\\\xb1:\x92\xadH\xf8\x1d\x85\xd8\x02\x8f\x11\xcfLO6\xc5\x93\xfb\xcd\xed\xf84em\x92\xcb\xb9\xf1R~\x0157\xe6\xbc\n\x87\xf2\xcc\xc0\xec\xb9\x0b%\x14\x93\x91\x9a\xb9\xf29\x06V\xa6\x93\xdcO}"
encrypted_with_passwd2_obscure = b')\x16e\x10\x8e\xc3}\xf0\xc6 \xa4\x9b+\x8b\xb8P#\xc8\x8b\xe4\xd4=\x06\xb3\xfc\xec\xc5\xdfr\x1a\x0cmU\x969\xc7Y\xf8D3\xe2\xfbKi+\xed\x0c\xfd\xc0\xcfC\xfe\xfc\xaf\x02\xe0TU\r-\xf7\x1d\xc6\xaa\xb7\xfb\xfe\xc3\xdf\xfe\xecd6\x1dE\xf5\x0fS>\x9f\x16z\x81~\xffwr{\xa8\x08\x1e\xd1\xe5\xa8\x94x\x94\xf3\x1fn\x1cH\xd5dn\x80\xf3R\x96\x8a\x0c$\xd5\x81|\xcf'
encrypted_without_passwd2_obscure = b"W\xfct'_\xe3\xbeN\xed\xaakySOB\xadlL\x11\xc8\xe8e\xe4\x1e&\x1a&t\x06;\xff^\xa8OX\xea\xc5]q\xd1\xed\xe67LY\xeb\xbc&\xbeK\x00\x98c\xcf\xde'\\\xb1:\x92\xadH\xf8\x1d\x85\xd8\x02\x8f\x11\xcfLO6\xc5\x93\xfb\xcd\xed\xf84em\x92\xcb\xb9\xf1R~\x0157\xe6\xbc\n\x87\xf2\xcc\xc0\xec\xb9\x0b%\x14\x93\x91\x9a\xb9\xf29\x06V\xa6\x93\xdcO}"

def test_byte_increment():
    assert byte_increment(1) == 2
    assert byte_increment(13) == 14
    assert byte_increment(254) == 255
    assert byte_increment(255) == 0
    with pytest.raises(ValueError):
        byte_increment(265)
    with pytest.raises(ValueError):
        byte_increment(256)

def test_nonce_increment():
    assert nonce_increment(b'\x00') == b'\x01'
    assert nonce_increment(b'\x00\x01') == b'\x01\x01'
    assert nonce_increment(b'\x01\x01') == b'\x02\x01'
    assert nonce_increment(b'\xff\x01') == b'\x00\x02'
    assert nonce_increment(b'\xff\xff') == b'\x00\x00'

def test_nonce_add():
    assert nonce_add(b'\xff\x01' + b'\x00' * 6, 0) == b'\xff\x01' + b'\x00' * 6
    assert nonce_add(b'\xff\x01' + b'\x00' * 9, 1) == b'\x00\x02' + b'\x00' * 9
    assert nonce_add(b'\xff\x01' + b'\x00' * 12, 0x0f) == b'\x0e\x02' + b'\x00' * 12
    assert nonce_add(b'\xff\x01' + b'\x00' * 12, 0x10) == b'\x0f\x02' + b'\x00' * 12
    assert nonce_add(b'\xff\x01' + b'\x00' * 12, 0xff) == b'\xfe\x02' + b'\x00' * 12
    with pytest.raises(ValueError):
        nonce_add(b'\x00\x00', 0)

def test_bytes_decrypt():
    assert b'' == crypt_with_passwd2.File.bytes_decrypt(b'', nonce, 0)
    assert b'' == crypt_without_passwd2.File.bytes_decrypt(b'', nonce, 0)
    assert origin_bytes == crypt_with_passwd2.File.bytes_decrypt(encrypted_with_passwd2, nonce, 0)
    assert origin_bytes == crypt_without_passwd2.File.bytes_decrypt(encrypted_without_passwd2, nonce, 0)

def test_bytes_decrypt_obscure():
    assert b'' == crypt_with_passwd2_obscure.File.bytes_decrypt(b'', nonce, 0)
    assert b'' == crypt_without_passwd2_obscure.File.bytes_decrypt(b'', nonce, 0)
    assert origin_bytes == crypt_with_passwd2_obscure.File.bytes_decrypt(encrypted_with_passwd2_obscure, nonce, 0)
    assert origin_bytes == crypt_without_passwd2_obscure.File.bytes_decrypt(encrypted_without_passwd2_obscure, nonce, 0)

def test_bytes_encrypt():
    assert crypt_with_passwd2.File.bytes_decrypt(b'', nonce, 0) == b''
    assert crypt_without_passwd2.File.bytes_decrypt(b'', nonce, 0) == b''
    assert crypt_with_passwd2.File.bytes_decrypt(encrypted_with_passwd2, nonce, 0) == origin_bytes
    assert crypt_without_passwd2.File.bytes_decrypt(encrypted_without_passwd2, nonce, 0) == origin_bytes

def test_bytes_encrypt_obscure():
    assert crypt_with_passwd2_obscure.File.bytes_decrypt(b'', nonce, 0) == b''
    assert crypt_without_passwd2_obscure.File.bytes_decrypt(b'', nonce, 0) == b''
    assert crypt_with_passwd2_obscure.File.bytes_decrypt(encrypted_with_passwd2_obscure, nonce, 0) == origin_bytes
    assert crypt_without_passwd2_obscure.File.bytes_decrypt(encrypted_without_passwd2_obscure, nonce, 0) == origin_bytes