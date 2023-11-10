# epub2cbz

Most comic reading software supports epub format comic books but does not support .cbz or .zip format. This project analyzes epub opf files to obtain standard book names and correct reading order.

Supports files that comply with the epub comic standard stipulated by the vol.moe website.

## Install

download the source code of epub2cbz, enter the source directory, and run `pip install -r requirements.txt`。

Then use `python epub2cbz.py`

## Usages

### Example Command

```shell
python epub2cbz.py /comics/batman/
```

### Full Usages

```console
Usage: epub2cbz.py [-options] path

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

<img src="./doc/before.png" alt="before" width="39%"/>
<img src="./doc/after.png" alt="after" width="59%"/>

## Other Open-Source Code Used

- https://github.com/python-pillow/Pillow for Imaging Library
- https://github.com/willmcgugan/rich for beautiful formatting in the terminal.
