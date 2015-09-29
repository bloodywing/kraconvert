from kraconvert import kra
import os
import argparse
from PIL import Image, ImageCms

__author__ = 'pierre'


class Main(object):

    args = None
    kras = []
    outdir = None


    def __init__(self):
        parser = argparse.ArgumentParser(description='Krita .kra file batch processing')

        parser.add_argument(
            'kras', metavar='kra', type=str, nargs='+', help='list of .kra files to convert'
        )

        parser.add_argument(
            '-i', '--icc', action='store_true', help='Extract icc colour profile'
        )

        parser.add_argument(
            '-o', '--output', type=str, nargs=1, required=False, help='output directory, if you convert multiple kra files, each'
                                                      'gets it\'s own directory', default=os.curdir
        )

        parser.add_argument(
            '-p', '--png', action='store_true', required=False, help='extract the merged PNG file'
        )

        jpeg = parser.add_argument_group('JPEG Options')

        jpeg.add_argument(
            '-j', '--jpeg', type=int, default=90, required=False
        )

        jpeg.add_argument(
            '-s', '--sizes', type=int, nargs='*', default=[1600, 1000, 800, 600], help='Desired sizes for your JPEG files'
        )

        jpeg.add_argument(
            '-w', '--webready', action='store_true', help='Try to convert jpeg files to sRGB-builtin'
        )

        args = parser.parse_args()

        self.args = args

        if self.args.output:
            self.outdir = self.args.output


        if self.args.kras:
            for krafile in self.args.kras:
                self.kras.append(kra.Kra(krafile))

        if self.args.png:
            self.extract_png()

        if self.args.icc:
            self.extract_icc()

        if self.args.webready and not self.args.icc:
            raise SystemExit('I need -i to get the source icc profile')

        if self.args.jpeg:
            self.export_as_jpegs()


    def extract_png(self):

        for kra in self.kras:
            png = kra.get_merged_image()
            png_name = kra.get_basename() + '.png'

            png_dir = os.path.join(self.outdir, kra.get_basename(), 'png')
            os.makedirs(png_dir, exist_ok=True)
            kra.merged_image_path = os.path.join(png_dir, png_name)

            with open(os.path.join(png_dir, png_name), 'w+b') as f:
                f.write(png)
                f.close()

    def extract_icc(self):

        for kra in self.kras:
            icc = kra.get_icc()
            icc_dir = os.path.join(self.outdir, kra.get_basename(), 'icc')
            os.makedirs(icc_dir, exist_ok=True)
            kra.icc_path = os.path.join(icc_dir, icc['name'])

            with open(os.path.join(icc_dir, icc['name']), 'w+b') as f:
                f.write(icc['data'])
                f.close()

    def export_as_jpegs(self):
        for kra in self.kras:
            for size in self.args.sizes:
                jpeg_dir = os.path.join(self.outdir, kra.get_basename(), 'jpeg')
                os.makedirs(jpeg_dir, exist_ok=True)

                im = Image.open(kra.merged_image_path)

                jpeg_name = kra.get_basename() + '{0}.jpeg'.format(size)

                new_im = im.thumbnail((size, size), Image.ANTIALIAS)
                srgb = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'sRGB.icc')

                if self.args.webready:
                    im = ImageCms.profileToProfile(im, kra.icc_path, srgb)
                    im.save(os.path.join(jpeg_dir, jpeg_name), quality=self.args.jpeg)
                else:
                    im.save(os.path.join(jpeg_dir, jpeg_name), quality=self.args.jpeg, icc_profile=kra.icc)



if __name__ == '__main__':
    m = Main()

def run():
    Main()
