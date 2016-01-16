from __future__ import print_function

import PIL
import Image
import argparse

class Asciify(object):
    img      = None
    size     = 128
    rgb_max  = 255
    gradient = '#&O/+:-. ' # '@8OCoc:. '

    def __init__(self, **kwargs):

        try:
            self.size = int(kwargs.get('size'))
        except:
            pass # resort to default

        try:
            self.img = Image.open(kwargs.get('file', ''))
        except:
            print("Couldn't open image.")
            return

        self.run()

    def map_to_ascii(self, v):
        step = self.rgb_max/len(self.gradient)
        for x in range(len(self.gradient)):
            if (v <= x*step):
                return self.gradient[x]
        return self.gradient[-1]

    def get_size(self, w, h):
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
                self.get_size(*rgb_img.size),
                PIL.Image.ANTIALIAS)

        # (column, row) = (width, height)
        (col, row) = rgb_img.size

        # Write to file
        with open('ascii.txt', 'w+') as FD:
            for ii in range(row):
                for jj in range(col):
                    # For greyscale RGB, r = g = b
                    (r, g, b) = rgb_img.getpixel((jj, ii))
                    FD.write(self.map_to_ascii(r))
                FD.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f','--file', help='Input file name', required=True)
    parser.add_argument('-s','--size', help='Max number of characters per row/col', required=False)
    args = parser.parse_args()
    asciify = Asciify(file=args.file, size=args.size)
