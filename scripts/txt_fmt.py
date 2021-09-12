# -*- coding:utf-8 -*-

from statistics import median
import re
import os.path


def txt_fmt(txt_path: str, pat_path: str, cor_path: str) -> str:
    """
    人工校对前对 TXT 文本进行预处理
    :param pat_path: 正则路径
    :param cor_path: 语料路径
    :param txt_path: OCR 的识别结果文本
    :return: 预处理后的文本
    """

    # 合并段落
    lines = []
    with open(txt_path, mode='r', encoding='utf-8', errors='ignore') as f0:
        std_len = median(len(l) for lno, l in enumerate(f0) if lno <= 50) * 0.85
    with open(txt_path, mode='r', encoding='utf-8', errors='ignore') as f0:
        for line in f0:
            if len(line) < std_len:
                el = f'{line}\n'
            else:
                el = line.rstrip('\n')
            lines.append(el)
    text = ''.join(lines)

    # 导入预设正则，多对一，顺序不可变
    patterns = {}
    with open(pat_path, mode='r', encoding='utf-8', errors='ignore') as fp:
        for line in fp:
            if ' ' in line:
                k, v = line.split(' ')
                patterns[k] = v.rstrip('\n')
            else:
                k = line.rstrip('\n')
                patterns[k] = ''

    # 导入语料，合成正则，一对一，需消重
    corpus = {}
    with open(cor_path, mode='r', encoding='utf-8', errors='ignore') as fc:
        for line in fc:
            k, v = line.split(' ')
            corpus[k] = v.rstrip('\n')

    def typo_repl(match_obj):
        typo = match_obj.group(0)
        return corpus[typo]
    typos = '|'.join(corpus)
    patterns[typos] = typo_repl

    # 正则匹配和替换
    for k, v in patterns.items():
        re_obj = re.compile(k)
        text = re_obj.sub(v, text)

    # 替换结果写入文件
    fmt_path = f'{os.path.splitext(txt_path)[0]}_fmt.txt'
    with open(fmt_path, mode='w', encoding='utf-8', errors='ignore') as f1:
        f1.write(text)

    print('文本预处理完毕')
    return fmt_path


if __name__ == '__main__':
    path1 = input('请输入 TXT 文件的路径：').strip("' ")
    path2 = input('请输入 PAT 文件的路径：').strip("' ")
    path3 = input('请输入 COR 文件的路径：').strip("' ")
    txt_fmt(path1, path2, path3)

