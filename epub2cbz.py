#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import getopt
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

from rich.panel import Panel
from rich.pretty import Pretty

from getpy import GetEngine
from manage import FileManager
from parent import console, progress, help_text


def process(_epub, _task_id):
    with FileManager(_epub, root) as fm:
        title, imglist = GetEngine(fm.zfile).get_info()
        fm.set_directory(title)
        progress.update(_task_id, description=title, total=100)
        progress.start_task(_task_id)
        progress.refresh()
        for img in imglist:
            fm.img_handler(*img, rotate_flag=rotate_flag)
            progress.advance(_task_id, 70 / len(imglist))
        if folder_flag:
            fm.package_folder(_task_id)
        else:
            fm.package(suffix, _task_id)
        progress.update(_task_id, completed=100)
        console.log('[bold green][Task completed][/bold green]', '[bold red]-->[/bold red]',
                    f"{os.path.join(root, title)}{'' if folder_flag else suffix}")


def executor():
    with progress:
        console.rule("[bold blue]Start running epub2cbz")
        with ThreadPoolExecutor() as pool:
            epub_list = [os.path.join(root, x) for x in os.listdir(root) if os.path.splitext(x)[1] == '.epub']
            if len(epub_list) == 0:
                console.print('')
                console.log(
                    f'[bold red]No epub files were found in {os.path.abspath(root)}, the program will exit.\n')
                console.rule('[bold blue]All tasks completed')
                return
            console.log(Panel(Pretty(epub_list), title='[bold blue]Find the following epub file[/bold blue]',
                              title_align='left'))
            for epub in epub_list:
                task_id = progress.add_task(description='Loading...', start=False)
                pool.submit(process, epub, task_id)
        if os.path.exists(os.path.join(root, '.tempworkdir')):
            shutil.rmtree(os.path.join(root, '.tempworkdir'))
        console.rule('[bold blue]All tasks completed')


def executor_file():
    global root
    with progress:
        console.rule("[bold blue]Start running epub2cbz")
        if os.path.splitext(root)[1] != '.epub':
            console.print('')
            console.log(
                f'[bold red]It\'s not an epub file at {os.path.abspath(root)}, the program will exit.\n')
            console.rule('[bold blue]All tasks completed')
            return
        console.log(Panel(f'[bold blue][Start converting file][/bold blue] [bold red]-->[/bold red] {root}'))
        task_id = progress.add_task(description='Loading...', start=False)
        epub = root
        root = os.path.split(root)[0]
        process(epub, task_id)
        if os.path.exists(os.path.join(root, '.tempworkdir')):
            shutil.rmtree(os.path.join(root, '.tempworkdir'))
        console.rule('[bold blue]All tasks completed')


if __name__ == "__main__":
    ifexecute = True
    isfile = False
    rotate_flag = False
    folder_flag = False
    opts, args = getopt.getopt(sys.argv[1:], 'frhs:', ['folder', 'rotate', 'help', 'suffix='])
    # epub文件所在目录/epub路径
    root = './'
    # 需要打包成压缩文档的扩展名
    suffix = '.cbz'
    root = args[0] if args else root
    isfile = not os.path.isdir(os.path.abspath(root))
    for k, v in opts:
        if k in ['-s', '--suffix'] and v != '':
            suffix = '.' + v if not v.startswith('.') else v
        if k in ['-r', '--rotate']:
            rotate_flag = True
        if k == '--folder':
            folder_flag = True
        if k in ['-h', '--help']:
            console.print(help_text)
            ifexecute = False
    if ifexecute:
        if isfile:
            executor_file()
        else:
            executor()
