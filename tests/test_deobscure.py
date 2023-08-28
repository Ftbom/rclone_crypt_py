from src.rclone import passwd_deobscure

def test_passwd_obscure():
    assert passwd_deobscure(b'') == b''
    assert passwd_deobscure(b'KhhUMRgBkIurpARiD2YzbxlyiSc') == b'test'
    assert passwd_deobscure(b'dLpeAk5lH95CK1RBcS1DxoHjEYCjA5aOEXPsX0DoIxSE7po') == b'iuergkldg02984ugial'
    assert passwd_deobscure(b'MPVqYephEbgJG0FYWzSwYpLAEq1x8w') == '你好'.encode('utf-8')