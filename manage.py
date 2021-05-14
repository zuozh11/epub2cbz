import os
import shutil
import zipfile

from PIL import Image


class FileManager(object):
    """

        This class is used for file interactions.

        It has the following methods:

        set_directory() --- Which set up the working directory

        img_handler() --- Which xtract from the compressed file to the output directory and process the picture.

        package() --- Which packaged into a compressed file with a specific suffix.

        To create an instance of this object, pass in the name of epubfile and specified path.

    """

    def __init__(self, epub_file, path):
        # epub文件
        self.epub_file = epub_file
        # 指定的路径
        self.path = path
        self.zfile = None
        # 压缩档名称
        self.title = ''
        # 工作目录，任务结束后会删除
        self.work_directory = ''

    def set_directory(self, directory):
        self.title = directory
        self.work_directory = os.path.join(self.path, '.tempworkdir', directory)

    def img_handler(self, file, name):
        # 解压到工作目录
        src = self.zfile.extract(file, self.work_directory)
        dst = os.path.join(self.work_directory, name)
        # 移动到根工作目录，并按顺序改名
        shutil.move(src, dst)
        # 图片处理
        img = Image.open(dst)
        w, h = img.size
        # 修正图片方向
        if w / h > 0.75:
            rotate_img = img.transpose(Image.ROTATE_270)
            rotate_img.save(dst)
            # self.console.log('[修正图片方向]', '[bold red]-->[/bold red]', f'{self.title}/{name}')
        img.close()

    def package(self, suffix):
        zippath = os.path.join(self.path, self.title) + suffix
        with zipfile.ZipFile(zippath, mode='w', compression=zipfile.ZIP_STORED) as zf:
            file_names = list(filter(lambda x: os.path.isfile(x),
                                     [os.path.join(self.work_directory, x) for x in os.listdir(self.work_directory)]))
            for fn in file_names:
                zf.write(fn, arcname=os.path.split(fn)[1])
        os.chmod(zippath, 448)

    def __enter__(self):
        self.zfile = zipfile.ZipFile(self.epub_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.zfile is not None:
            self.zfile.close()
