import os
import shutil
import zipfile

from PIL import Image


class FileManager(object):
    """

        This class is used for file interactions.

        It has the following methods:

    """

    def __init__(self, epub_file):
        self.epub_file = epub_file
        self.zfile = None
        self.title = ''
        self.work_directory = ''

    def set_directory(self, path, directory):
        self.title = os.path.join(path, directory)
        self.work_directory = os.path.join(path, '.tempworkdir', directory)
        if not os.path.exists(self.work_directory):
            os.makedirs(self.work_directory)

    def img_handler(self, file, name):
        src = self.zfile.extract(file, self.work_directory)
        dst = os.path.join(self.work_directory, name)
        shutil.move(src, dst)
        # print(f'[src]: {src}  -->  [dst]: {dst}')
        img = Image.open(dst)
        w, h = img.size
        if w / h > 0.75:
            img.rotate(-90)
            img.save(dst)
        img.close()

    def package(self):
        zippath = self.title + '.cbz'
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
