#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, \
    SpinnerColumn, TimeElapsedColumn

from getpy import GetEngine
from manage import FileManager

progress = Progress(
    SpinnerColumn(speed=1.5, finished_text='✔'),
    TextColumn("[bold blue]{task.description}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeRemainingColumn(),
    TimeElapsedColumn(),
    auto_refresh=False
)
path = ''


def process(_epub, _task_id):
    with FileManager(_epub) as fm:
        _title, _imglist = GetEngine(fm.zfile).get_info()
        fm.set_directory(path, _title)
        progress.update(_task_id, description=_title, total=len(_imglist) + 1)
        progress.start_task(_task_id)
        progress.refresh()
        for img in _imglist:
            fm.img_handler(*img)
            progress.advance(_task_id, 1)
            progress.refresh()
        fm.package()
        progress.advance(_task_id, 1)
        progress.refresh()


if __name__ == "__main__":
    path = sys.argv[1:] if sys.argv[1:] else './test'
    with progress:
        with ThreadPoolExecutor() as pool:
            epub_list = [os.path.join(path, x) for x in os.listdir(path) if os.path.splitext(x)[1] == '.epub']
            for epub in epub_list:
                task_id = progress.add_task(description='正在读取...', start=False)
                future = pool.submit(process, epub, task_id)
    shutil.rmtree(os.path.join(path, '.tempworkdir'))
