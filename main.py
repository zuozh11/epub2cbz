#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, \
    SpinnerColumn, TimeElapsedColumn

from getpy import GetEngine
from manage import FileManager

console = Console()
progress = Progress(
    SpinnerColumn(speed=1.5, finished_text='✔'),
    TextColumn("[bold blue]{task.description}", justify="right"),
    BarColumn(bar_width=40),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeRemainingColumn(),
    TimeElapsedColumn(),
    auto_refresh=False,
    console=console
)


def process(_epub, _suffix, _task_id):
    with FileManager(_epub, path) as fm:
        _title, _imglist = GetEngine(fm.zfile).get_info()
        fm.set_directory(_title)
        progress.update(_task_id, description=_title, total=len(_imglist) + 1)
        progress.start_task(_task_id)
        progress.refresh()
        for img in _imglist:
            fm.img_handler(*img)
            progress.advance(_task_id, 1)
            progress.refresh()
        fm.package(_suffix)
        progress.advance(_task_id, 1)
        progress.refresh()
        console.log('[bold green][转换完毕][/bold green]', '[bold red]-->[/bold red]',
                    f'{os.path.join(path, _title)}{_suffix}')


if __name__ == "__main__":
    # Root directory
    path = sys.argv[1:] if sys.argv[1:] else './test'
    # 需要打包成压缩文档的扩展名
    suffix = 'cbz'
    suffix = '.' + suffix if not suffix.startswith('.') else suffix
    with progress:
        console.rule("[bold red]开始运行epub2cbz", style='bold white')
        with ThreadPoolExecutor() as pool:
            epub_list = [os.path.join(path, x) for x in os.listdir(path) if os.path.splitext(x)[1] == '.epub']
            console.log(Panel(Pretty(epub_list), title='[bold blue]找到以下epub文件[/bold blue]', title_align='left'))
            for epub in epub_list:
                task_id = progress.add_task(description='正在读取...', start=False)
                future = pool.submit(process, epub, suffix, task_id)
            console.print('')
        console.rule('[bold red]所有任务执行完毕', style='bold white')
        console.print('')
    shutil.rmtree(os.path.join(path, '.tempworkdir'))
