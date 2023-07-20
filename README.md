# rclone_crypt_py

python实现的针对rclone(crypt storage)的加密/解密

## 使用

```python
from rclone import Crypt
# 初始化
crypt = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')

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
# bytes解密
from rclone import Crypt
crypt = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')

with open('D:/Download/test.bin', 'rb') as f:
    f.seek(8) # 跳过固定文件头 b'RCLONE\x00\x00'
    init_nonce = f.read(24) # 读取nonce
    f.seek(5 * (1024 * 64 + 16), 1) # 跳过5个数据块
    input_bytes = f.read(10 * (1024 * 64 + 16)) # 读取10个数据块
    output_bytes = crypt.File.bytes_decrypt(input_bytes, init_nonce, 5) # 数据块解密
```
