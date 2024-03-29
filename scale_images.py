#!/usr/bin/env python3


from glob import glob
from PIL import Image, ImageOps
import os
import shutil
import sys
from tqdm import tqdm


img_extensions = '.JPG .jpg'.split()
bad_paths = '\\. /. ORIGINALS'.split()


def filter_bad(path):
    return any(s in path.upper() for s in bad_paths)


def list_files(dirname):
    wildcard = dirname.replace('\\', '/')
    wildcard = wildcard if wildcard.endswith('/') else wildcard+'/'
    wildcard = wildcard if wildcard.endswith('**') else wildcard+'**'
    fns = glob(wildcard, recursive=True)
    fns = [fn for fn in fns if any(fn.endswith(ext) for ext in img_extensions)]
    return fns


def scale_file(targetdir, filename, width, height, imgindex):
    if filter_bad(filename):
        return
    im = Image.open(filename)
    im = ImageOps.exif_transpose(im)
    ratio = min(width/float(im.size[0]), height/float(im.size[1]))
    im = im.resize(tuple(int(x*ratio) for x in im.size), Image.LANCZOS)
    subdir = os.path.join(targetdir, '%s' % (imgindex//100))
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    outname = '%i.jpg' % imgindex
    fullname = os.path.join(subdir, outname)
    im.save(fullname, 'JPEG', quality=98)


def scalefiles(files, targetdir, width, height):
    t = tqdm(files)
    for i,fn in enumerate(t):
        try:
            fn = fn.replace('\\', '/')
            scale_file(targetdir, fn, width, height, i)
            t.set_postfix(file=fn.rpartition('/')[2])
        except Exception as ex:
            print()
            print(type(ex), ex)
            break


def main():
    if len(sys.argv) == 5:
        srcdir = sys.argv[1]
        tgtdir = sys.argv[2]
        width = int(sys.argv[3])
        height = int(sys.argv[4])
        print('Listing files...')
        files = list_files(srcdir)
        print('Found %i images.' % len(files))
        try:
            shutil.rmtree(tgtdir)
        except:
            pass
        try:
            os.mkdir(tgtdir)
        except:
            pass
        scalefiles(files, tgtdir, width, height)
    else:
        print('Usage: %s <src dir> <tgt dir> <width> <height>' % sys.argv[0])
        print(sys.argv)
        sys.exit(1)


if __name__ == '__main__':
    main()
