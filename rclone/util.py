FILEMAGIC_SIZE = 8  # 文化magic大小
FILENONCE_SIZE = 24 # nonce大小
BLOCKHEADER_SIZE = 16 # 文件块头大小
BLOCKDATA_SIZE = 64 * 1024 # 文件块数据大小

def count_size(size: int) -> int:
    """
    通过加密后文件大小计算加密前文件大小
    :param `size`: 加密后文件大小
    """
    if size < (FILEMAGIC_SIZE + FILENONCE_SIZE):
        raise ValueError('not encrypted rclone file')
    size = size - FILEMAGIC_SIZE - FILENONCE_SIZE
    if size == 0:
        return 0
    block_num = size // (BLOCKDATA_SIZE + BLOCKHEADER_SIZE)
    remain_size = size % (BLOCKDATA_SIZE + BLOCKHEADER_SIZE)
    if remain_size <= BLOCKHEADER_SIZE:
        raise ValueError('not encrypted rclone file')
    return block_num * BLOCKDATA_SIZE + remain_size - BLOCKHEADER_SIZE

def count_pos(pos: int, round_forward: bool = True) -> int:
    """
    通过解密后的文件读取位置计算加密文件对应的读取位置\n
    返回应读取的位置，返回值总是对应整数个文件块（BLOCKDATA_SIZE + BLOCKHEADER_SIZE）\n
    向前取整：文件块对应的数据不多于pos\n
    向后取整：文件块对应的数据不少于pos\n
    :param `pos`: 加密前文件的读取位置
    :param `round_forward`: 向前或向后取整
    """
    num = pos // BLOCKDATA_SIZE
    if not round_forward:
        num = num + 1
    return FILEMAGIC_SIZE + FILENONCE_SIZE + num * (BLOCKDATA_SIZE + BLOCKHEADER_SIZE)

def count_block_num(pos: int) -> int:
    """
    通过加密文件的读取位置计算文件块数量
    :param `pos`: 加密后文件的读取位置
    """
    if pos < (FILEMAGIC_SIZE + FILENONCE_SIZE):
        raise ValueError('pos less than head size')
    return (pos - FILEMAGIC_SIZE - FILENONCE_SIZE) // (BLOCKDATA_SIZE + BLOCKHEADER_SIZE)