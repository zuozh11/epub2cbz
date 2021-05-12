import os
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
        self.directory = ''

    def set_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.directory = directory

    def img_handler(self, file, name):
        temp = os.path.join(self.directory, 'temp')
        self.zfile.extract(file, temp)
        path = os.path.join(temp, file)
        img = Image.open(path)
        w, h = img.size
        if w / h > 0.75:
            print(f"{name}  {file}  {w}  {h}")
            img.rotate(-90)
        img.save(os.path.join(self.directory, name), 'jpeg')
        img.close()

    def __enter__(self):
        self.zfile = zipfile.ZipFile(self.epub_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.zfile is not None:
            self.zfile.close()
