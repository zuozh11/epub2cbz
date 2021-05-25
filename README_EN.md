# epub2cbz

Most comic reading software supports epub format comic books but does not support .cbz or .zip format. This project analyzes epub opf files to obtain standard book names and correct reading order.

Supports files that comply with the epub comic standard stipulated by the vol.moe website.

## Install

epub2cbz has been registered with pip, you can use the pip package management tool for quick installation.

```shell
pip install epub2cbz
```

Or you can download the source code of epub2cbz, enter the source directory, and run `pip install requirements.txt`。

Then use `python ./epub2cbz.py` instead of `epub2cbz` command

**https://github.com/nihui/waifu2x-ncnn-vulkan/releases**

## Usages

### Example Command

```shell
epb2cbz /comics/batman/
```

### Full Usages

```console
Usage: epub2cbz [-options] path

      -h --help               show this help
      -r --rotate             correct orientation.This feature may only be applicable 
                              to picture with 1200 pixel width standard.
      -s: --suffix: <value>   specify the output file suffix, default is .cbz
      --folder                output to a folder instead of the compressed file
```

- `path` accept either file path or directory path
- `--folder`
  If you need to process the pictures yourself before packaging, you can use this command to output the sorted pictures to a folder instead of packaging them into .cbz
- `-s`
  You can specify the suffix of the packaged file. For example, if you need a package in .zip format, you can use `epb2cbz -s .zip /comics/batman/`

### rotate

If you often download comics on vol.moe, you may find that some two-page wide images are merged into one file, and the direction is rotated by 90°.

For this you may need to rotate your device frequently to watch books, and also lock the direction of rotation of your device.

If this bothers you, you can add the `-r` or `--rotate` parameter to automatically monitor the wide image and rotate it to the normal direction.

<img src="/Users/zuozhi/workspase/python/epub2cbz/doc/before.png" alt="before" style="width:39%;" />

<img src="/Users/zuozhi/workspase/python/epub2cbz/doc/after.png" alt="after" style="width:59%;" />

## Other Open-Source Code Used

- https://github.com/python-pillow/Pillow for Imaging Library
- https://github.com/willmcgugan/rich for beautiful formatting in the terminal.
