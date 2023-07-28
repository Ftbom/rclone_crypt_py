import os
import pytest
import hashlib
from rclone import Crypt
from rclone.file_cipher import byte_increment, nonce_increment, nonce_add

TEST_FILE_PATH = 'test_files'

crypt_with_passwd2 = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')
crypt_without_passwd2 = Crypt('Z2rCKxxvrm6pQMW')
crypt_with_passwd2_obscure = Crypt('SpnX0yEFxpNJjo9bxd3xAlVoXA7F4cr3C0SA-zmfzw', 'ziWH7jKYerB6o5vHnaXAvISTguFD6ZFJFbhT3BlLVQ', True)
crypt_without_passwd2_obscure = Crypt('MgfGDnK6S3la2nrxfSx6Qk01oTyErIXvu_pRrnPfLw', passwd_obscured = True)

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

def test_file_decrypt():
    crypt_with_passwd2.File.file_decrypt(f'{TEST_FILE_PATH}/rclone_encrypted_with_passwd2', f'{TEST_FILE_PATH}/test')
    assert hashlib.md5(open(f'{TEST_FILE_PATH}/test', 'rb').read()).hexdigest() == hashlib.md5(open(f'{TEST_FILE_PATH}/origin_file', 'rb').read()).hexdigest()
    os.remove(f'{TEST_FILE_PATH}/test')
    crypt_without_passwd2.File.file_decrypt(f'{TEST_FILE_PATH}/rclone_encrypted_without_passwd2', f'{TEST_FILE_PATH}/test')
    assert hashlib.md5(open(f'{TEST_FILE_PATH}/test', 'rb').read()).hexdigest() == hashlib.md5(open(f'{TEST_FILE_PATH}/origin_file', 'rb').read()).hexdigest()
    os.remove(f'{TEST_FILE_PATH}/test')

def test_file_decrypt_obscure():
    crypt_with_passwd2_obscure.File.file_decrypt(f'{TEST_FILE_PATH}/rclone_encrypted_with_passwd2', f'{TEST_FILE_PATH}/test')
    assert hashlib.md5(open(f'{TEST_FILE_PATH}/test', 'rb').read()).hexdigest() == hashlib.md5(open(f'{TEST_FILE_PATH}/origin_file', 'rb').read()).hexdigest()
    os.remove(f'{TEST_FILE_PATH}/test')
    crypt_without_passwd2_obscure.File.file_decrypt(f'{TEST_FILE_PATH}/rclone_encrypted_without_passwd2', f'{TEST_FILE_PATH}/test')
    assert hashlib.md5(open(f'{TEST_FILE_PATH}/test', 'rb').read()).hexdigest() == hashlib.md5(open(f'{TEST_FILE_PATH}/origin_file', 'rb').read()).hexdigest()
    os.remove(f'{TEST_FILE_PATH}/test')

def test_file_encrypt():
    crypt_with_passwd2.File.file_encrypt(f'{TEST_FILE_PATH}/origin_file', f'{TEST_FILE_PATH}/test')
    crypt_with_passwd2.File.file_decrypt(f'{TEST_FILE_PATH}/test', f'{TEST_FILE_PATH}/test1')
    assert hashlib.md5(open(f'{TEST_FILE_PATH}/test1', 'rb').read()).hexdigest() == hashlib.md5(open(f'{TEST_FILE_PATH}/origin_file', 'rb').read()).hexdigest()
    os.remove(f'{TEST_FILE_PATH}/test')
    os.remove(f'{TEST_FILE_PATH}/test1')
    crypt_without_passwd2.File.file_encrypt(f'{TEST_FILE_PATH}/origin_file', f'{TEST_FILE_PATH}/test')
    crypt_without_passwd2.File.file_decrypt(f'{TEST_FILE_PATH}/test', f'{TEST_FILE_PATH}/test1')
    assert hashlib.md5(open(f'{TEST_FILE_PATH}/test1', 'rb').read()).hexdigest() == hashlib.md5(open(f'{TEST_FILE_PATH}/origin_file', 'rb').read()).hexdigest()
    os.remove(f'{TEST_FILE_PATH}/test')
    os.remove(f'{TEST_FILE_PATH}/test1')

def test_file_encrypt_obscure():
    crypt_with_passwd2_obscure.File.file_encrypt(f'{TEST_FILE_PATH}/origin_file', f'{TEST_FILE_PATH}/test')
    crypt_with_passwd2_obscure.File.file_decrypt(f'{TEST_FILE_PATH}/test', f'{TEST_FILE_PATH}/test1')
    assert hashlib.md5(open(f'{TEST_FILE_PATH}/test1', 'rb').read()).hexdigest() == hashlib.md5(open(f'{TEST_FILE_PATH}/origin_file', 'rb').read()).hexdigest()
    os.remove(f'{TEST_FILE_PATH}/test')
    os.remove(f'{TEST_FILE_PATH}/test1')
    crypt_without_passwd2_obscure.File.file_encrypt(f'{TEST_FILE_PATH}/origin_file', f'{TEST_FILE_PATH}/test')
    crypt_without_passwd2_obscure.File.file_decrypt(f'{TEST_FILE_PATH}/test', f'{TEST_FILE_PATH}/test1')
    assert hashlib.md5(open(f'{TEST_FILE_PATH}/test1', 'rb').read()).hexdigest() == hashlib.md5(open(f'{TEST_FILE_PATH}/origin_file', 'rb').read()).hexdigest()
    os.remove(f'{TEST_FILE_PATH}/test')
    os.remove(f'{TEST_FILE_PATH}/test1')

def test_bytes_decrypt():
    with open(f'{TEST_FILE_PATH}/origin_file', 'rb') as f:
        origin_data = f.read()
    with open(f'{TEST_FILE_PATH}/rclone_encrypted_with_passwd2', 'rb') as f:
        f.seek(8)
        nonce_with_passwd2 = f.read(24)
        encrypted_data_with_passwd2 = f.read()
    with open(f'{TEST_FILE_PATH}/rclone_encrypted_without_passwd2', 'rb') as f:
        f.seek(8)
        nonce_without_passwd2 = f.read(24)
        encrypted_data_without_passwd2 = f.read()
    assert origin_data == crypt_with_passwd2.File.bytes_decrypt(encrypted_data_with_passwd2, nonce_with_passwd2, 0)
    assert origin_data == crypt_without_passwd2.File.bytes_decrypt(encrypted_data_without_passwd2, nonce_without_passwd2, 0)

def test_bytes_decrypt_obscure():
    with open(f'{TEST_FILE_PATH}/origin_file', 'rb') as f:
        origin_data = f.read()
    with open(f'{TEST_FILE_PATH}/rclone_encrypted_with_passwd2', 'rb') as f:
        f.seek(8)
        nonce_with_passwd2 = f.read(24)
        encrypted_data_with_passwd2 = f.read()
    with open(f'{TEST_FILE_PATH}/rclone_encrypted_without_passwd2', 'rb') as f:
        f.seek(8)
        nonce_without_passwd2 = f.read(24)
        encrypted_data_without_passwd2 = f.read()
    assert origin_data == crypt_with_passwd2_obscure.File.bytes_decrypt(encrypted_data_with_passwd2, nonce_with_passwd2, 0)
    assert origin_data == crypt_without_passwd2_obscure.File.bytes_decrypt(encrypted_data_without_passwd2, nonce_without_passwd2, 0)