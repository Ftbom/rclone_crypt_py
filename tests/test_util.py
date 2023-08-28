import pytest
from src.rclone import util

def test_count_size():
    assert util.count_size(32) == 0
    assert util.count_size(5432) == 5384
    assert util.count_size(4111940) == 4110900
    assert util.count_size(1689079215) == 1688666895
    with pytest.raises(ValueError):
        util.count_size(24)
    with pytest.raises(ValueError):
        util.count_size(48)

def test_count_pos():
    assert util.count_pos(0) == 32
    assert util.count_pos(1) == 32
    assert util.count_pos(1000000) == 983312
    assert util.count_pos(0, False) == 65584
    assert util.count_pos(1, False) == 65584
    assert util.count_pos(1000000, False) == 1048864

def test_count_block_num():
    assert util.count_block_num(32) == 0
    assert util.count_block_num(65584) == 1
    assert util.count_block_num(983312) == 15
    assert util.count_block_num(1048864) == 16
    with pytest.raises(ValueError):
        util.count_block_num(24)