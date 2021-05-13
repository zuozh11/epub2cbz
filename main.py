#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

from rich.progress import Progress

from getpy import GetEngine
from manage import FileManager

progress = Progress()
path = './'


def process(epub, title, imglist, task_id):
    with FileManager(epub) as fm:
        fm.set_directory(path, title)
        for img in imglist:
            fm.img_handler(*img)
            progress.update(task_id, advance=1)
        fm.package()


if __name__ == "__main__":
    path = sys.argv[1:] if sys.argv[1:] else './test'
    epub_list = [os.path.join(path, x) for x in os.listdir(path) if os.path.splitext(x)[1] == '.epub']
    with progress:
        with ThreadPoolExecutor() as pool:
            for epub in epub_list:
                with FileManager(epub) as fm:
                    ge = GetEngine(fm.zfile)
                    title, imglist = ge.get_info()
                task_id = progress.add_task(description=title, total=len(imglist))
                progress.start_task(task_id)
                future = pool.submit(process, epub, title, imglist, task_id)
        shutil.rmtree(os.path.join(path, '.tempworkdir'))
