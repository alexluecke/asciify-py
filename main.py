from __future__ import print_function
from PIL import Image

import PIL
import argparse

class Asciify(object):
    img      = None
    size     = 128
    rgb_max  = 255
    gradient = '#&O/+:-. '

    # Other gradient examples:
    # '@8OCoc:. '
    # '#/+-. '

    def __init__(self, **kwargs):

        # Gradient is always passed in kwargs but might be None so I can't
        # use standard kwargs.get('name', default).
        self.gradient = kwargs.get('gradient') \
                if kwargs.get('gradient') \
                else self.gradient

        try:
            self.size = int(kwargs.get('size'))
        except:
            pass # resort to default

        try:
            self.img = Image.open(kwargs.get('file', ''))
        except:
            print("Couldn't open image.")
            exit

    def map_to_ascii(self, v):
        step = self.rgb_max/len(self.gradient)
        for x in range(len(self.gradient)):
            if (v <= x*step):
                return self.gradient[x]
        return self.gradient[-1]

    def get_resize(self, w, h):
        # Shrink to proper size to display on screen:
        if w > self.size or h > self.size:
            if h > w:
                f = self.size / float(h)
            else:
                f = self.size / float(w)
            return (int(w*f), int(h*f))
        return (w, h)

    def run(self):

        # Convert the image to greyscale then get RGB values
        rgb_img = self.img.convert('L').convert('RGB')

        # Resize image to constraint
        rgb_img = rgb_img.resize(
                self.get_resize(*rgb_img.size),
                PIL.Image.ANTIALIAS)

        # (column, row) = (width, height)
        (col, row) = rgb_img.size

        # return value:
        ret=''
        for ii in range(row):
            for jj in range(col):
                # For greyscale RGB, r = g = b
                (r, g, b) = rgb_img.getpixel((jj, ii))
                ret += self.map_to_ascii(r)
            ret += "\n"

        return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f','--file', help='Input file name', required=True)
    parser.add_argument('-s','--size', help='Max number of characters per row/col', required=False)
    parser.add_argument('-g','--gradient', help='Custom character gradient (dark->light)', required=False)
    args = parser.parse_args()
    asciified = Asciify(file=args.file, size=args.size, gradient=args.gradient).run()
    print(asciified)
