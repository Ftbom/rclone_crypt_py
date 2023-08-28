from src.rclone import Crypt

crypt_with_passwd2 = Crypt('PvrhK9lOaJMdJO2', 'bjnW66SNkUuV4hX')
crypt_without_passwd2 = Crypt('Z2rCKxxvrm6pQMW')
crypt_with_passwd2_obscure = Crypt('SpnX0yEFxpNJjo9bxd3xAlVoXA7F4cr3C0SA-zmfzw', 'ziWH7jKYerB6o5vHnaXAvISTguFD6ZFJFbhT3BlLVQ', True)
crypt_without_passwd2_obscure = Crypt('MgfGDnK6S3la2nrxfSx6Qk01oTyErIXvu_pRrnPfLw', passwd_obscured = True)

def test_obfuscate_encrypt():
    assert crypt_with_passwd2.Name.obfuscate_encrypt('') == ''
    assert crypt_with_passwd2.Name.obfuscate_encrypt('Hello,Word') == '188.Nkrru,cuxj'
    assert crypt_with_passwd2.Name.obfuscate_encrypt('你好，世界') == '75.侫姈ｗ乡疗'
    assert crypt_with_passwd2.Name.obfuscate_encrypt('Hello,Word/你好，世界') == '188.Nkrru,cuxj/75.侫姈ｗ乡疗'
    assert crypt_with_passwd2.Name.obfuscate_encrypt('🎈😀௹〓') == '148.🎝😕଎〨'
    assert crypt_without_passwd2.Name.obfuscate_encrypt('') == ''
    assert crypt_without_passwd2.Name.obfuscate_encrypt('Hello,Word') == '188.dAHHK,sKNz'
    assert crypt_without_passwd2.Name.obfuscate_encrypt('你好，世界') == '75.俐姭ｼ了疼'
    assert crypt_without_passwd2.Name.obfuscate_encrypt('Hello,Word/你好，世界') == '188.dAHHK,sKNz/75.俐姭ｼ了疼'
    assert crypt_without_passwd2.Name.obfuscate_encrypt('🎈😀௹〓') == '148.🏂😺ଳき'

def test_obfuscate_encrypt_obscure():
    assert crypt_with_passwd2_obscure.Name.obfuscate_encrypt('') == ''
    assert crypt_with_passwd2_obscure.Name.obfuscate_encrypt('Hello,Word') == '188.Nkrru,cuxj'
    assert crypt_with_passwd2_obscure.Name.obfuscate_encrypt('你好，世界') == '75.侫姈ｗ乡疗'
    assert crypt_with_passwd2_obscure.Name.obfuscate_encrypt('Hello,Word/你好，世界') == '188.Nkrru,cuxj/75.侫姈ｗ乡疗'
    assert crypt_with_passwd2_obscure.Name.obfuscate_encrypt('🎈😀௹〓') == '148.🎝😕଎〨'
    assert crypt_without_passwd2_obscure.Name.obfuscate_encrypt('') == ''
    assert crypt_without_passwd2_obscure.Name.obfuscate_encrypt('Hello,Word') == '188.dAHHK,sKNz'
    assert crypt_without_passwd2_obscure.Name.obfuscate_encrypt('你好，世界') == '75.俐姭ｼ了疼'
    assert crypt_without_passwd2_obscure.Name.obfuscate_encrypt('Hello,Word/你好，世界') == '188.dAHHK,sKNz/75.俐姭ｼ了疼'
    assert crypt_without_passwd2_obscure.Name.obfuscate_encrypt('🎈😀௹〓') == '148.🏂😺ଳき'

def test_obfuscate_decrypt():
    assert crypt_with_passwd2.Name.obfuscate_decrypt('') == ''
    assert crypt_with_passwd2.Name.obfuscate_decrypt('188.Nkrru,cuxj') == 'Hello,Word'
    assert crypt_with_passwd2.Name.obfuscate_decrypt('75.侫姈ｗ乡疗') == '你好，世界'
    assert crypt_with_passwd2.Name.obfuscate_decrypt('188.Nkrru,cuxj/75.侫姈ｗ乡疗') == 'Hello,Word/你好，世界'
    assert crypt_with_passwd2.Name.obfuscate_decrypt('148.🎝😕଎〨') == '🎈😀௹〓'
    assert crypt_without_passwd2.Name.obfuscate_decrypt('') == ''
    assert crypt_without_passwd2.Name.obfuscate_decrypt('188.dAHHK,sKNz') == 'Hello,Word'
    assert crypt_without_passwd2.Name.obfuscate_decrypt('75.俐姭ｼ了疼') == '你好，世界'
    assert crypt_without_passwd2.Name.obfuscate_decrypt('188.dAHHK,sKNz/75.俐姭ｼ了疼') == 'Hello,Word/你好，世界'
    assert crypt_without_passwd2.Name.obfuscate_decrypt('148.🏂😺ଳき') == '🎈😀௹〓'

def test_obfuscate_decrypt_obscure():
    assert crypt_with_passwd2_obscure.Name.obfuscate_decrypt('') == ''
    assert crypt_with_passwd2_obscure.Name.obfuscate_decrypt('188.Nkrru,cuxj') == 'Hello,Word'
    assert crypt_with_passwd2_obscure.Name.obfuscate_decrypt('75.侫姈ｗ乡疗') == '你好，世界'
    assert crypt_with_passwd2_obscure.Name.obfuscate_decrypt('188.Nkrru,cuxj/75.侫姈ｗ乡疗') == 'Hello,Word/你好，世界'
    assert crypt_with_passwd2_obscure.Name.obfuscate_decrypt('148.🎝😕଎〨') == '🎈😀௹〓'
    assert crypt_without_passwd2_obscure.Name.obfuscate_decrypt('') == ''
    assert crypt_without_passwd2_obscure.Name.obfuscate_decrypt('188.dAHHK,sKNz') == 'Hello,Word'
    assert crypt_without_passwd2_obscure.Name.obfuscate_decrypt('75.俐姭ｼ了疼') == '你好，世界'
    assert crypt_without_passwd2_obscure.Name.obfuscate_decrypt('188.dAHHK,sKNz/75.俐姭ｼ了疼') == 'Hello,Word/你好，世界'
    assert crypt_without_passwd2_obscure.Name.obfuscate_decrypt('148.🏂😺ଳき') == '🎈😀௹〓'

def test_standard_encrypt():
    assert crypt_with_passwd2.Name.standard_encrypt('') == ''
    assert crypt_with_passwd2.Name.standard_encrypt('Hello,Word') == 'tj0ivgsmd9vh4ccfov7f739in0'
    assert crypt_with_passwd2.Name.standard_encrypt('你好，世界') == 'lb8g1ak1849smj6mlmpv2c5aio'
    assert crypt_with_passwd2.Name.standard_encrypt('Hello,Word/你好，世界') == 'tj0ivgsmd9vh4ccfov7f739in0/lb8g1ak1849smj6mlmpv2c5aio'
    assert crypt_with_passwd2.Name.standard_encrypt('🎈😀௹〓') == 'a6603j02fga7padgh0lsrv4ca0'
    assert crypt_without_passwd2.Name.standard_encrypt('') == ''
    assert crypt_without_passwd2.Name.standard_encrypt('Hello,Word') == 'gfcoee69bhe3qpq30aqmur0a88'
    assert crypt_without_passwd2.Name.standard_encrypt('你好，世界') == 'ahjb6djdnlgr2bce4bablmlvl8'
    assert crypt_without_passwd2.Name.standard_encrypt('Hello,Word/你好，世界') == 'gfcoee69bhe3qpq30aqmur0a88/ahjb6djdnlgr2bce4bablmlvl8'
    assert crypt_without_passwd2.Name.standard_encrypt('🎈😀௹〓') == 'aqvo2skqf51oe1dikf33n5k85o'

def test_standard_encrypt_obscure():
    assert crypt_with_passwd2_obscure.Name.standard_encrypt('') == ''
    assert crypt_with_passwd2_obscure.Name.standard_encrypt('Hello,Word') == 'tj0ivgsmd9vh4ccfov7f739in0'
    assert crypt_with_passwd2_obscure.Name.standard_encrypt('你好，世界') == 'lb8g1ak1849smj6mlmpv2c5aio'
    assert crypt_with_passwd2_obscure.Name.standard_encrypt('Hello,Word/你好，世界') == 'tj0ivgsmd9vh4ccfov7f739in0/lb8g1ak1849smj6mlmpv2c5aio'
    assert crypt_with_passwd2_obscure.Name.standard_encrypt('🎈😀௹〓') == 'a6603j02fga7padgh0lsrv4ca0'
    assert crypt_without_passwd2_obscure.Name.standard_encrypt('') == ''
    assert crypt_without_passwd2_obscure.Name.standard_encrypt('Hello,Word') == 'gfcoee69bhe3qpq30aqmur0a88'
    assert crypt_without_passwd2_obscure.Name.standard_encrypt('你好，世界') == 'ahjb6djdnlgr2bce4bablmlvl8'
    assert crypt_without_passwd2_obscure.Name.standard_encrypt('Hello,Word/你好，世界') == 'gfcoee69bhe3qpq30aqmur0a88/ahjb6djdnlgr2bce4bablmlvl8'
    assert crypt_without_passwd2_obscure.Name.standard_encrypt('🎈😀௹〓') == 'aqvo2skqf51oe1dikf33n5k85o'

def test_standard_decrypt():
    assert crypt_with_passwd2.Name.standard_decrypt('') == ''
    assert crypt_with_passwd2.Name.standard_decrypt('tj0ivgsmd9vh4ccfov7f739in0') == 'Hello,Word'
    assert crypt_with_passwd2.Name.standard_decrypt('lb8g1ak1849smj6mlmpv2c5aio') == '你好，世界'
    assert crypt_with_passwd2.Name.standard_decrypt('tj0ivgsmd9vh4ccfov7f739in0/lb8g1ak1849smj6mlmpv2c5aio') == 'Hello,Word/你好，世界'
    assert crypt_with_passwd2.Name.standard_decrypt('a6603j02fga7padgh0lsrv4ca0') == '🎈😀௹〓'
    assert crypt_without_passwd2.Name.standard_decrypt('') == ''
    assert crypt_without_passwd2.Name.standard_decrypt('gfcoee69bhe3qpq30aqmur0a88') == 'Hello,Word'
    assert crypt_without_passwd2.Name.standard_decrypt('ahjb6djdnlgr2bce4bablmlvl8') == '你好，世界'
    assert crypt_without_passwd2.Name.standard_decrypt('gfcoee69bhe3qpq30aqmur0a88/ahjb6djdnlgr2bce4bablmlvl8') == 'Hello,Word/你好，世界'
    assert crypt_without_passwd2.Name.standard_decrypt('aqvo2skqf51oe1dikf33n5k85o') == '🎈😀௹〓'

def test_standard_decrypt_obscure():
    assert crypt_with_passwd2_obscure.Name.standard_decrypt('') == ''
    assert crypt_with_passwd2_obscure.Name.standard_decrypt('tj0ivgsmd9vh4ccfov7f739in0') == 'Hello,Word'
    assert crypt_with_passwd2_obscure.Name.standard_decrypt('lb8g1ak1849smj6mlmpv2c5aio') == '你好，世界'
    assert crypt_with_passwd2_obscure.Name.standard_decrypt('tj0ivgsmd9vh4ccfov7f739in0/lb8g1ak1849smj6mlmpv2c5aio') == 'Hello,Word/你好，世界'
    assert crypt_with_passwd2_obscure.Name.standard_decrypt('a6603j02fga7padgh0lsrv4ca0') == '🎈😀௹〓'
    assert crypt_without_passwd2_obscure.Name.standard_decrypt('') == ''
    assert crypt_without_passwd2_obscure.Name.standard_decrypt('gfcoee69bhe3qpq30aqmur0a88') == 'Hello,Word'
    assert crypt_without_passwd2_obscure.Name.standard_decrypt('ahjb6djdnlgr2bce4bablmlvl8') == '你好，世界'
    assert crypt_without_passwd2_obscure.Name.standard_decrypt('gfcoee69bhe3qpq30aqmur0a88/ahjb6djdnlgr2bce4bablmlvl8') == 'Hello,Word/你好，世界'
    assert crypt_without_passwd2_obscure.Name.standard_decrypt('aqvo2skqf51oe1dikf33n5k85o') == '🎈😀௹〓'