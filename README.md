# rclone_crypt_py

[English](https://github.com/Ftbom/rclone_crypt_py/blob/main/README.md), [简体中文](https://github.com/Ftbom/rclone_crypt_py/blob/main/README-zh.md)

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
from rclone import Crypt
crypt = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')

# bytes decryption
with open('test.bin', 'rb') as f:
    f.seek(8) # Skip the fixed file header b'RCLONE\x00\x00'
    init_nonce = f.read(24) # Read the nonce
    f.seek(5 * (1024 * 64 + 16), 1) # Skip 5 data blocks
    input_bytes = f.read(10 * (1024 * 64 + 16)) # Read 10 data blocks
    output_bytes = crypt.File.bytes_decrypt(input_bytes, init_nonce, 5) # Decrypt the data blocks

# bytes encryption
import nacl
with open('test.bin', 'wb') as f:
    f.write(b'RCLONE\x00\x00') # Write the standard header
    init_nonce = nacl.utils.random(24) # Generate a random nonce (24 bits)
    f.write(init_nonce) # Write the nonce
    with open('origin.bin', 'rb') as fl:
        origin_bytes = fl.read(1024 * 64 * 10) # Read 10 data blocks
        i = 0
        while origin_bytes:
            f.write(crypt.File.bytes_encrypt(origin_bytes, init_nonce, i))
            origin_bytes = fl.read(1024 * 64 * 10)
            i = i + 10
```