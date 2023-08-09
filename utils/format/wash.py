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

if __name__ == '__main__':
    print(wash_tel('12345678901'))
    print(wash_tel('手机号：123-4567-8901'))
    print(wash_idcard('123456789012345678'))
    print(wash_idcard('我的身份证是33068119901214567X'))
    print(wash_tel('我的身份证是33068119901214567X'))
