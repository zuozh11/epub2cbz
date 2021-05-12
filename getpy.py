import io
import os
import re
import xml.dom.minidom


class GetEngine(object):
    """

        This class contains the methods needed to get the files,
        to help make the pdf file.

        The class contains the following methods:

        get_html() --- Which gets the html file names.

        get_pdf() --- Which gets the pdf file names.

        get_css() --- Which gets the css file names.

        get_images() --- Which gets the image file names.

        To create an instance of this object, pass in the name of the directory
        that stores all the extracted files from the epub file.

    """

    def __init__(self, zfile):
        if zfile is None:
            print('ERROR: zfile is None')
        self.zfile = zfile
        self.opf = ''
        self.n = 0

    def get_info(self):
        root = self.__get_opf()
        title = root.getElementsByTagName('dc:title')[0].firstChild.data

        page_order = [x.getAttribute('idref') for x in root.getElementsByTagName('itemref')]
        imgpath = [[self.__get_imgpath(x.getAttribute('href')) for x in root.getElementsByTagName('item')
                    if x.getAttribute('id') == pid][0]
                   for pid in page_order]
        imglist = [(x, self.__gen_imgname(x)) for x in imgpath]
        imglist = filter(lambda x: x[1] is not None, imglist)
        return title, imglist

    # 获取opf文件xml根节点
    def __get_opf(self):
        # 通过io.SringIO()获取文件流（file对象）
        instream = io.StringIO(self.zfile.read(os.path.join('META-INF', 'container.xml')).decode("utf-8"))
        # 利用 xml.dom.minidom.parse() 将文件（file对象转为DOM）
        dom_tree = xml.dom.minidom.parse(instream)
        # 获取根节点
        root = dom_tree.documentElement
        rootfile = root.getElementsByTagName('rootfile')[0]
        path = rootfile.getAttribute('full-path')
        instream = io.StringIO(self.zfile.read(path).decode("utf-8"))
        dom_tree = xml.dom.minidom.parse(instream)
        self.opf = dom_tree.documentElement
        return self.opf

    def __gen_imgname(self, path):
        sname = os.path.split(path)[1]
        ssp = os.path.splitext(sname)
        if ssp[0] == 'cover' or ssp[0] == 'createby':
            return None
        self.n = self.n + 1
        return str(self.n).zfill(3) + ssp[1]

    def __get_imgpath(self, htmlpath):
        with self.zfile.open(htmlpath) as f:
            line = f.readline().decode("utf-8")
            while line:
                match = re.search(r'<img.*src=\s*([\"\'].*?[\"\'])( |/>)', line)
                if match:
                    imgpath = (re.search(r'src=\s*([\"\'].*?[\"\'])( |/>)', match[0])[0]
                               .replace(' ', '').replace('src=', '')
                               .replace('\"', '').replace('\'', ''))
                    if imgpath.startswith('../') or imgpath.startswith('./'):
                        imgpath = os.path.normpath(os.path.join(os.path.split(htmlpath)[0], imgpath))
                    return imgpath
                line = f.readline().decode("utf-8")
