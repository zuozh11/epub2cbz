#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from getpy import GetEngine
from manage import FileManager

path = './test'


def process(epub_file):
    global path
    print('--- Epub to CBZ conversion started')

    with FileManager(epub_file) as fm:
        ge = GetEngine(fm.zfile)
        title, imglist = ge.get_info()
        fm.set_directory(os.path.join(path, title))
        for img in imglist:
            fm.img_handler(*img)
        fm.package()

    print('--- Epub to CBZ conversion successful')


def executor():
    epub_list = [os.path.join(path, x) for x in os.listdir(
        path) if os.path.splitext(x)[1] == '.epub']
    print(epub_list)
    for epub_file in epub_list:
        process(epub_file)


if __name__ == "__main__":
    executor()
