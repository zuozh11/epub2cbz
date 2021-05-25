# epub2cbz

大部分漫画阅读软件对epub格式的漫画书支持没有对.cbz或.zip格式的支持完善，此项目通过分析epub的opf文件，获取标准的书籍名称，以及正确的阅读顺序

支持遵从vol.moe网站规定的epub漫画标准的文件

## 安装

epub2cbz已注册到pip,你可以使用pip包管理工具来进行快速安装

```shell
pip install epub2cbz
```

或者你可以下载epub2cbz的源码，进入到源码目录，运行`pip install requirements.txt`。

之后使用`python ./epub2cbz.py`来代替`epub2cbz`命令

**https://github.com/nihui/waifu2x-ncnn-vulkan/releases**

## 使用方法

### 示例

```shell
epb2cbz /comics/batman/
```

### 参数说明

```console
Usage: epub2cbz [-options] path

      -h --help               显示此帮助
      -r --rotate             正确的方向。此功能仅适用于标准像素宽度为1200的图片
      -s: --suffix: <value>   指定输出文件后缀，默认为.cbz
      --folder                输出到文件夹而不是压缩文件
```

- `path` 接受文件路径或目录路径
- `--folder` 如果你在打包前还需要对图片进行自己的处理，你可以使用此命令来将排序好的图片输出到文件夹，而不是打包成.cbz
- `-s` 你可以指定打包文件的后缀名，例如你需要的是一个.zip格式的包，你可以使用 `epb2cbz -s .zip /comics/batman/`

### rotate

如果你经常在vol.moe上下载漫画，你可能会发现有一些双页的宽图被合并成一个文件，并且方向被旋转了90°。

为此你可能需要频繁的旋转你的设备来观看书籍，并且还得锁定你的设备的旋转方向。

如果这使你困扰，你可以加上`-r`或`--rotate`参数来自动监测宽图并将它旋转至正常的方向。

<img src="/Users/zuozhi/workspase/python/epub2cbz/doc/before.png" alt="before" style="width:39%;" />

<img src="/Users/zuozhi/workspase/python/epub2cbz/doc/after.png" alt="after" style="width:59%;" />

## 其它使用到的开源项目

- https://github.com/python-pillow/Pillow 用于成像库。
- https://github.com/willmcgugan/rich 在终端中进行漂亮的格式化。
