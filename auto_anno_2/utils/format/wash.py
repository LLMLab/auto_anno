import re

def wash_tel(txt):
    _txt = ' ' + txt + ' '
    tels = re.findall(r'[^\d]\d{3}[\d-]{,8}\d{2}[^\d]', _txt)
    washed_txt = txt
    for tel in tels:
      tel = tel[1:-1]
      star = '*' * len(tel[3:-2])
      washed_txt = washed_txt.replace(tel, tel[:3] + star + tel[-2:])
    return washed_txt

def wash_idcard(txt):
    star = '*' * 13
    washed_txt = re.sub(r'(\d{3})(\d{13})([\dXx]{2})', rf'\1{star}\3', txt)
    return washed_txt

# 参考地址 https://www.jianshu.com/p/152e081fec1b
def q_2_b(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e: #转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)

def wash_q_2_b(txt):
    """把字符串全角转半角"""
    return "".join([q_2_b(uchar) for uchar in txt])

if __name__ == '__main__':
    print(wash_tel('12345678901'))
    print(wash_tel('手机号：123-4567-8901'))
    print(wash_idcard('123456789012345678'))
    print(wash_idcard('我的身份证是33068119901214567X'))
    print(wash_tel('我的身份证是33068119901214567X'))
    print(wash_q_2_b('＂第　３　题，Ａ选项是对的．＂'))
