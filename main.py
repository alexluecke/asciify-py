from __future__ import print_function

import PIL
import Image
import argparse

class Asciify(object):
    img = None
    size = 128

    def __init__(self, **kwargs):
        try:
            self.img = Image.open(kwargs.get('file', ''))
        except:
            print("Couldn't open image.")

        if (kwargs.get('size') is not None):
            self.size = int(kwargs.get('size'))

        self.run()

    def ascii_map(self, v):
        grad = '@8OCoc:. '
        step = 255/(len(grad)-1)
        c = 0
        for x in range(0, 255, step):
            if (v <= x):
                return grad[c]
            c += 1
        return grad[-1]

    def run(self):

        img_out = self.img.convert(colors=256)
        rgb_img = img_out.convert('L').convert('RGB')
        (w, h) = rgb_img.size

        # Shrink to proper size to display on screen:
        if w > self.size or h > self.size:
            if h > w:
                f = self.size / float(h)
            else:
                f = self.size / float(w)
            rgb_img = rgb_img.resize((int(w*f), int(h*f)), PIL.Image.ANTIALIAS)

        (row, col) = rgb_img.size

        # Write to file
        with open('ascii.txt', 'w+') as FD:
            for jj in range(col):
                for ii in range(row):
                    (r, g, b) = rgb_img.getpixel((ii, jj))
                    FD.write(self.ascii_map(r))
                FD.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f','--file', help='Input file name', required=True)
    parser.add_argument('-s','--size', help='Max number of characters per row/col', required=False)
    args = parser.parse_args()
    asciify = Asciify(file=args.file, size=args.size)
