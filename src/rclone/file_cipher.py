from nacl.secret import SecretBox
import nacl.utils

FILEMAGIC_SIZE = 8  # 文化magic大小
FILENONCE_SIZE = 24 # nonce大小
BLOCKHEADER_SIZE = 16 # 文件块头大小
BLOCKDATA_SIZE = 64 * 1024 # 文件块数据大小

# 单byte加1
def byte_increment(byte: int) -> int:
    if (byte > 255):
        raise ValueError('byte must be in range(0, 256)')
    return (byte + 1) if (byte < 255) else 0

# nonce加1
def nonce_increment(nonce: bytes, start: int = 0) -> bytes:
    nonce_array = bytearray(nonce) # 转为数组
    # 加1操作
    for i in range(start, len(nonce)):
        digit = nonce_array[i]
        newDigit = byte_increment(digit)
        nonce_array[i] = newDigit
        if newDigit >= digit:
            break
    return bytes(nonce_array) #转回bytes

# nonce添加指定值
def nonce_add(nonce: bytes, x: int) -> bytes:
    if len(nonce) < 8:
        raise ValueError('the length of nonce should greater than 8')
    if x <= 0:
        return nonce
    nonce_array = bytearray(nonce)
    carry = 0
    for i in range(8):
        digit = nonce_array[i]
        xDigit = x & 255 # 仅保留后8位
        x = x >> 8
        carry = carry + (digit & 65535) + (xDigit & 65535)
        nonce_array[i] = carry & 255
        carry = carry >> 8
    newNonce = bytes(nonce_array)
    if not carry == 0:
        newNonce = nonce_increment(newNonce, 8)
    return newNonce

class File:
    """
    rclone文件加密/解密
    :param `box`: 用于解密bytes的nacl SecretBox，`nacl.secret.SecretBox(key)`
    """
    def __init__(self, box: SecretBox) -> None:
        self.__box = box

    def file_decrypt(self, input_file_path: str, output_file_path: str) -> None:
        """
        文件解密
        :param `input_file_path`: 待解密文件路径
        :param `output_file_path`: 输出文件路径
        """
        try:
            input_file = open(input_file_path, 'rb')
        except:
            raise FileNotFoundError('input file not found')
        try:
            output_file = open(output_file_path, 'wb')
        except:
            input_file.close()
            raise ValueError('failed to write output file')
        # 读取头
        if not input_file.read(FILEMAGIC_SIZE) == b'RCLONE\x00\x00': # 标准头
            input_file.close()
            output_file.close()
            raise ValueError('not encrypted rclone file')
        Nonce = input_file.read(FILENONCE_SIZE)
        # 读取文件块
        # 16为头
        # 64kb数据
        input_bytes = input_file.read((BLOCKDATA_SIZE + BLOCKHEADER_SIZE) * 10)
        try:
            while (input_bytes):
                output_file.write(self.bytes_decrypt(input_bytes, Nonce))
                Nonce = nonce_add(Nonce, 10)
                input_bytes = input_file.read((BLOCKDATA_SIZE + BLOCKHEADER_SIZE) * 10)
        except:
            input_file.close()
            output_file.close()
            raise RuntimeError('failed to decrypt file')
        input_file.close()
        output_file.close()
    
    def file_encrypt(self, input_file_path: str, output_file_path: str) -> None:
        """
        文件加密
        :param `input_file_path`: 待加密文件路径
        :param `output_file_path`: 输出文件路径
        """
        try:
            input_file = open(input_file_path, 'rb')
        except:
            raise FileNotFoundError('input file not found')
        try:
            output_file = open(output_file_path, 'wb')
        except:
            input_file.close()
            raise ValueError('failed to write output file')
        # 写入头
        output_file.write(b'RCLONE\x00\x00') # 标准头
        Nonce = nacl.utils.random(FILENONCE_SIZE) # 生成nonce
        output_file.write(Nonce)
        # 读取文件块
        # 10 * 64kb数据
        input_bytes = input_file.read(BLOCKDATA_SIZE * 10)
        try:
            while (input_bytes):
                output_file.write(self.bytes_encrypt(input_bytes, Nonce))
                Nonce = nonce_add(Nonce, 10)
                input_bytes = input_file.read(BLOCKDATA_SIZE * 10)
        except:
            input_file.close()
            output_file.close()
            raise RuntimeError('failed to encrypt file')
        input_file.close()
        output_file.close()

    def bytes_decrypt(self, input_bytes: bytes, nonce: bytes, block_offset: int = 0) -> bytes:
        """
        bytes解密
        :param `input_bytes`: 输入bytes
        :param `nonce`: 用于解密的nonce
        :param `blockoffset`: input_bytes相对于输入nonce的偏移
        """
        if input_bytes == b'':
            return b''
        output_bytes = b''
        block_size = BLOCKDATA_SIZE + BLOCKHEADER_SIZE # 文件块大小
        nonce = nonce_add(nonce, block_offset) # 根据初始文件块偏移位，调整nonce
        block_num = len(input_bytes) // block_size # 完整文件块数量
        bytes_remain = len(input_bytes) % block_size # 剩余bytes
        try:
            for i in range(block_num):
                pos = i * block_size
                output_bytes = output_bytes + self.__box.decrypt(input_bytes[pos : pos + block_size], nonce)
                nonce = nonce_increment(nonce)
            if not bytes_remain == 0:
                output_bytes = output_bytes + self.__box.decrypt(input_bytes[block_num * block_size :], nonce)
        except:
            raise ValueError('failed to decrypt bytes')
        return output_bytes

    def bytes_encrypt(self, input_bytes: bytes, nonce: bytes, block_offset: int = 0) -> bytes:
        """
        bytes加密
        :param `input_bytes`: 输入bytes
        :param `nonce`: 用于加密的nonce，24位
        :param `blockoffset`: input_bytes相对于输入nonce的偏移
        """
        if input_bytes == b'':
            return b''
        output_bytes = b''
        block_size = BLOCKDATA_SIZE # 文件块大小
        nonce = nonce_add(nonce, block_offset) # 根据初始文件块偏移位，调整nonce
        block_num = len(input_bytes) // block_size
        bytes_remain = len(input_bytes) % block_size
        try:
            for i in range(block_num):
                pos = i * block_size
                output_bytes = output_bytes + self.__box.encrypt(input_bytes[pos : pos + block_size], nonce).ciphertext
                nonce = nonce_increment(nonce)
            if not bytes_remain == 0:
                output_bytes = output_bytes + self.__box.encrypt(input_bytes[block_num * block_size :], nonce).ciphertext
        except:
            raise ValueError('failed to encrypt bytes')
        return output_bytes