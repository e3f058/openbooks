# -*- coding:utf-8 -*-

import fitz
from paddleocr import PaddleOCR
import tempfile
import os.path


def pdf_rec(pdf_path: str) -> str:
    """
    OCR 识别 PDF 中的文字
    :param pdf_path: 被识别文件的完整路径
    :return: 识别结果的保存路径，与被识别文件同名同路径，后缀为.txt
    """

    pdf = fitz.Document(pdf_path)
    ocr = PaddleOCR(use_gpu=False)

    with tempfile.TemporaryDirectory() as imgs_dir:

        # 将 PDF 的每一页渲染为图像，并保存到临时文件夹下
        imgs = []
        for page in pdf:
            pix = page.get_pixmap()
            pno = page.number
            img = f'{imgs_dir}/{pno}.png'
            pix.save(img)
            imgs.append(img)

        # 逐页识别文字
        text = []
        for img in imgs:
            results = ocr.ocr(img, cls=False)
            for line in results:
                text.append(line[1][0])

    # 将识别结果写入文件
    txt = f'{os.path.splitext(pdf_path)[0]}.txt'
    with open(txt, mode='w', encoding='utf-8') as f:
        for line in text:
            f.write(f'{line}\n')

    print('PDF文件转换完毕')
    return txt


if __name__ == '__main__':
    path1 = input('请输入 PDF 文件的路径：').strip("' ")
    pdf_rec(path1)
