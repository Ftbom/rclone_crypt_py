# rclone_crypt_py

[简体中文](https://github.com/Ftbom/rclone_crypt_py/blob/main/README.md), [English](https://github.com/Ftbom/rclone_crypt_py/blob/main/README-en.md)

python实现的针对rclone(crypt storage)的加密/解密

## 使用

```python
from rclone import Crypt
# 初始化
# 分别传入passwd1和passwd2

# 此处的passwd是创建crypt时的密码，而不是rclone配置文件中的密码
# 若未设置passwd2，可省略第二个参数
crypt = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')

# 若直接传入rclone配置文件中的密码（混淆后的密码），需将passwd_obscured参数设为True
# crypt = Crypt('SpnX0yEFxpNJjo9bxd3xAlVoXA7F4cr3C0SA-zmfzw', 'ziWH7jKYerB6o5vHnaXAvISTguFD6ZFJFbhT3BlLVQ', True)

# 文件加密/解密
crypt.File.file_decrypt(input_file_path, output_file_path)
crypt.File.file_encrypt(input_file_path, output_file_path)

# 文件路径加密/解密
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

# bytes解密
with open('test.bin', 'rb') as f:
    f.seek(8) # 跳过固定文件头 b'RCLONE\x00\x00'
    init_nonce = f.read(24) # 读取nonce
    f.seek(5 * (1024 * 64 + 16), 1) # 跳过5个数据块
    input_bytes = f.read(10 * (1024 * 64 + 16)) # 读取10个数据块
    output_bytes = crypt.File.bytes_decrypt(input_bytes, init_nonce, 5) # 数据块解密

# bytes加密
import nacl
with open('test.bin', 'wb') as f:
    f.write(b'RCLONE\x00\x00') # 写入标准头
    init_nonce = nacl.utils.random(24) # 生成随机nonce（24位）
    f.write(init_nonce) # 写入nonce
    with open('origin.bin', 'rb') as fl:
        origin_bytes = fl.read(1024 * 64 * 10) # 读取10个数据块
        i = 0
        while origin_bytes:
            f.write(crypt.File.bytes_encrypt(origin_bytes, init_nonce, i))
            origin_bytes = fl.read(1024 * 64 * 10)
            i = i + 10
```
