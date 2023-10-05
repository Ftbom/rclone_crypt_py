import base64
from .eme import Decrypt, Encrypt
from Crypto.Util.Padding import unpad, pad
from Crypto.Cipher._mode_ecb import EcbMode

class Name:
    """
    rclone文件名加密/解密，支持standard和obfuscate形式
    :param `nameKey`: 通过passwd生成的nameKey
    :param `nameTweak`: 通过passwd生成的nameTweak
    :param `aes_cipher`: ECB模式的AES Cipher，`AES.new(nameKey, AES.MODE_ECB)`
    """
    def __init__(self, nameKey: bytes, nameTweak: bytes, aes_cipher: EcbMode) -> None:
        self.__nameKey = nameKey
        self.__nameTweak = nameTweak
        self.__cipher = aes_cipher
        # https://stackoverflow.com/questions/73144204/base32encode-in-python3-8-compliant-with-rfc2938
        # base32hexencode/decode 适配更低的python版本（小于3.10）
        base32_bytes = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567='
        base32hex_bytes = b'0123456789ABCDEFGHIJKLMNOPQRSTUV='
        self.trans_to_hex = bytes.maketrans(base32_bytes, base32hex_bytes)
        self.trans_from_hex = bytes.maketrans(base32hex_bytes, base32_bytes)
    
    def standard_encrypt(self, filepath: str) -> str:
        """
        文件名standard加密
        :param `filepath`: 待加密文件路径
        """
        return '/'.join(map(self.__name_standard_encrypt, filepath.split('/')))
    
    def standard_decrypt(self, filepath: str) -> str:
        """
        文件名standard解密
        :param `filepath`: 待解密文件路径
        """
        return '/'.join(map(self.__name_standard_decrypt, filepath.split('/')))
    
    def obfuscate_encrypt(self, filepath: str) -> str:
        """
        文件名obfuscate加密
        :param `filepath`: 待加密文件路径
        """
        return '/'.join(map(self.__name_obfuscate_encrypt, filepath.split('/')))
    
    def obfuscate_decrypt(self, filepath: str) -> str:
        """
        文件名obfuscate解密
        :param `filepath`: 待解密文件路径
        """
        return '/'.join(map(self.__name_obfuscate_decrypt, filepath.split('/')))
    
    def __name_standard_decrypt(self, filename: str) -> str:
        if filename == '':
            return ''
        padding_num = 8 - len(filename) % 8
        filename = filename + padding_num * '=' # 添加padding
        filename = base64.b32decode(filename.upper().encode('utf-8').translate(self.trans_from_hex)) # base32hex解码
        if len(filename) == 0:
            raise ValueError('too short to decrypt')
        if len(filename) >= 2048:
            raise ValueError('too long to decrypt')
        return unpad(Decrypt(self.__cipher, self.__nameTweak, filename), 16, style = 'pkcs7').decode('utf-8') # EME解密 & pkcs7 unpad
    
    def __name_standard_encrypt(self, filename: str) -> str:
        if filename == '':
            return ''
        filename = pad(filename.encode('utf-8'), 16, style = 'pkcs7')
        filename = Encrypt(self.__cipher, self.__nameTweak, filename)
        return base64.b32encode(filename).translate(self.trans_to_hex).decode('utf-8').strip('=').lower()
    
    def __name_obfuscate_encrypt(self, filename: str) -> str:
        if filename == '':
            return ''
        out_filename = ''
        filename_code = []
        try:
            for str_ in filename:
                filename_code.append(ord(str_))
        except:
            return '!.' + filename
        dir_ = 0
        for code in filename_code:
            dir_ = dir_ + code
        dir_ = dir_ % 256
        out_filename = out_filename + f'{dir_}.'
        for i in self.__nameKey:
            dir_ = dir_ + i
        for code in filename_code:
            if (code == ord('!')):
                out_filename = out_filename + '!!'
            elif code >= ord('0') and code <= ord('9'):
                thisdir = (dir_ % 9) + 1
                out_filename = out_filename + chr(ord('0') + (code - ord('0') + thisdir) % 10)
            elif (code >= ord('A') and code <= ord('Z')) or (code >= ord('a') and code <= ord('z')):
                thisdir = dir_ % 25 + 1
                pos = code - ord('A')
                if pos >= 26:
                    pos = pos - 6
                pos = (pos + thisdir) % 52
                if pos >= 26:
                    pos = pos + 6
                out_filename = out_filename + chr(ord('A') + pos)
            elif code >= 0xa0 and code <= 0xff:
                thisdir = (dir_ % 95) + 1
                out_filename = out_filename + chr(0xa0 + (code - 0xa0 + thisdir) % 96)
            elif code >= 0x100:
                thisdir = (dir_ % 127) + 1
                base = code - code % 256
                try:
                    out_filename = out_filename + chr(base + (code - base + thisdir) % 256)
                except:
                    out_filename = out_filename + f'!{chr(code)}'
            else:
                out_filename = out_filename + chr(code)
        return out_filename
    
    def __name_obfuscate_decrypt(self, filename: str) -> str:
        if filename == '':
            return ''
        pos = filename.find('.')
        if pos == -1:
            raise ValueError('not obfuscate encrypted filename')
        num = filename[: pos]
        if num == '!':
            return filename[pos + 1 :]
        try:
            dir_ = int(num)
        except:
            raise ValueError('not obfuscate encrypted filename')
        for i in self.__nameKey:
            dir_ = dir_ + i
        inQuote = False
        out_filename = ''
        for str_ in filename[pos + 1 :]:
            code = ord(str_)
            if inQuote:
                out_filename = out_filename + str_
            elif code == ord('!'):
                inQuote = True
            elif code >= ord('0') and code <= ord('9'):
                thisdir = (dir_ % 9) + 1
                newRune = ord('0') + code - ord('0') - thisdir
                if newRune < ord('0'):
                    newRune = newRune + 10
                out_filename = out_filename + chr(newRune)
            elif (code >= ord('A') and code <= ord('Z')) or (code >= ord('a') and code <= ord('z')):
                thisdir = dir_ % 25 + 1
                pos = code - ord('A')
                if pos >= 26:
                    pos = pos -6
                pos = pos - thisdir
                if pos < 0:
                    pos = pos + 52
                if pos >= 26:
                    pos = pos + 6
                out_filename = out_filename + chr(ord('A') + pos)
            elif code >= 0xa0 and code <= 0xff:
                thisdir = (dir_ % 95) + 1
                newRune = 0xa0 + code - 0xa0 - thisdir
                if newRune < 0xa0:
                    newRune = newRune + 96
                out_filename = out_filename + chr(newRune)
            elif code >= 0x100:
                thisdir = (dir_ % 127) + 1
                base = code - code % 256
                newRune = base + code - base - thisdir
                if newRune < base:
                    newRune = newRune + 256
                out_filename = out_filename + chr(newRune)
            else:
                out_filename = out_filename + chr(code)
        return out_filename