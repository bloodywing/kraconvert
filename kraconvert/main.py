from kraconvert import kra
import os
import argparse

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

        args = parser.parse_args()

        self.args = args

        if self.args.output:
            self.outdir = self.args.output

        if self.args.kras:
            for krafile in self.args.kras:
                self.kras.append(kra.Kra(krafile))

        if self.args.icc:
            self.extract_icc()

        if self.args.png:
            self.extract_png()

    def extract_png(self):

        for kra in self.kras:
            png = kra.get_merged_image()
            png_name = kra.get_basename() + '.png'

            png_dir = os.path.join(self.outdir, kra.get_basename(), 'png')
            os.makedirs(png_dir, exist_ok=True)
            with open(os.path.join(png_dir, png_name), 'w+b') as f:
                f.write(png)
                f.close()

    def extract_icc(self):

        for kra in self.kras:
            icc = kra.get_icc()
            icc_dir = os.path.join(self.outdir, kra.get_basename(), 'icc')
            os.makedirs(icc_dir, exist_ok=True)

            with open(os.path.join(icc_dir, icc['name']), 'w+b') as f:
                f.write(icc['data'])
                f.close()


if __name__ == '__main__':
    m = Main()

def run():
    Main()
