# rclone_crypt_py

[简体中文](https://github.com/Ftbom/rclone_crypt_py/blob/main/README.md), [English](https://github.com/Ftbom/rclone_crypt_py/blob/main/README-en.md)

Python implementation of encryption/decryption for rclone (crypt storage)

## Usage

```python
from rclone import Crypt
# Initialize
# Pass in passwd1 and passwd2

# The password here is the password for creating the crypt, not the password in the rclone configuration file
# If passwd2 is not set, the second parameter can be omitted
crypt = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')

# To use passwords directly in the rclone configuration file(obscured password), you should set the passwd_obscured parameter to True.
# crypt = Crypt('SpnX0yEFxpNJjo9bxd3xAlVoXA7F4cr3C0SA-zmfzw', 'ziWH7jKYerB6o5vHnaXAvISTguFD6ZFJFbhT3BlLVQ', True)

# File encryption/decryption
crypt.File.file_decrypt(input_file_path, output_file_path)
crypt.File.file_encrypt(input_file_path, output_file_path)

# File path encryption/decryption
# obfuscate
crypt.Name.obfuscate_encrypt('Hello,Word')
crypt.Name.obfuscate_decrypt('188.Nkrru,cuxj')

#standard
crypt.Name.standard_encrypt('Hello,Word/你好，世界')
crypt.Name.standard_decrypt('tj0ivgsmd9vh4ccfov7f739in0/lb8g1ak1849smj6mlmpv2c5aio')
```

```python
# bytes decryption
from rclone import Crypt
crypt = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')

with open('D:/Download/test.bin', 'rb') as f:
    f.seek(8) # Skip the fixed file header b'RCLONE\x00\x00'
    init_nonce = f.read(24) # Read the nonce
    f.seek(5 * (1024 * 64 + 16), 1) # Skip 5 data blocks
    input_bytes = f.read(10 * (1024 * 64 + 16)) # Read 10 data blocks
    output_bytes = crypt.File.bytes_decrypt(input_bytes, init_nonce, 5) # Data block decryption
```