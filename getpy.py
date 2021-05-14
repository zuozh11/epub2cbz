import io
import os
import re
import xml.dom.minidom


class GetEngine(object):
    """

        This class contains the methods to get the picture sequence , sorted name and other info.

        The class contains the following methods:

        get_info() --- Which gets the manga title and a sorted name list of pics.

        To create an instance of this object, pass in the Zipfile Object.

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
        imglist = list(filter(lambda x: x[1] is not None, imglist))
        return title, imglist

    # Get the opf file xml root node
    def __get_opf(self):
        # Get the file stream through io.SringIO()
        instream = io.StringIO(self.zfile.read(os.path.join('META-INF', 'container.xml')).decode("utf-8"))
        # Use xml.dom.minidom.parse () to convert a file (file object to DOM)
        dom_tree = xml.dom.minidom.parse(instream)
        # Get the root node
        root = dom_tree.documentElement
        rootfile = root.getElementsByTagName('rootfile')[0]
        # Opf file path
        path = rootfile.getAttribute('full-path')
        instream = io.StringIO(self.zfile.read(path).decode("utf-8"))
        dom_tree = xml.dom.minidom.parse(instream)
        self.opf = dom_tree.documentElement
        return self.opf

    # Get the name of the sorted picture like '015.jpg'
    def __gen_imgname(self, path):
        sname = os.path.split(path)[1]
        ssp = os.path.splitext(sname)
        if ssp[0] == 'cover' or ssp[0] == 'createby':
            return None
        self.n = self.n + 1
        return str(self.n).zfill(3) + ssp[1]

    # Parse the html file to get the corresponding picture path
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
