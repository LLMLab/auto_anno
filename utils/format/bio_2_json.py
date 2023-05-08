def bio_2_json_one(anno_txt):
    ls = anno_txt.split('\n')
    text = ''
    anno = []
    now_label = ''
    for i, l in enumerate(ls):
        char, label = l.split('\t')
        text += char
        if 'B-' in label:
            start = i
            now_label = label.split('-')[1]
        if label == 'O':
            if now_label:
                anno.append([start, i, text[start:i], now_label])
                now_label = ''
                start = 0
    if now_label:
        i += 1
        anno.append([start, i, text[start:i], now_label])
    return {'text': text, 'anno': anno}


def bit_2_json(txt):
    anno_txts = txt.split('\n\n')
    annos = []
    for anno_txt in anno_txts:
        if anno_txt == '':
            continue
        anno_j = bio_2_json_one(anno_txt)
        annos.append(anno_j)
    return annos


if __name__ == '__main__':
    txt = '''你\tB-PER
是\tO
一\tO
个\tO
聪\tB-PER
明\tI-PER
的\tO
软\tB-ORG
件\tI-ORG
工\tI-ORG
程\tI-ORG
师\tI-ORG'''
    # txt = open('data/ner/weibo_ner/dev.txt', 'r', encoding='utf-8').read()
    annos = bit_2_json(txt)
    print(annos)
