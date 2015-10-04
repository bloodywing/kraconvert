from kraconvert import kra
import os
import argparse
from PIL import Image, ImageCms

__author__ = 'pierre'

parser = argparse.ArgumentParser(prog='kraconvert', description='Krita .kra file batch processing')

parser.add_argument(
    'kras', metavar='kra', type=str, nargs='+', help='list of .kra files to convert'
)

parser.add_argument(
    '-i', '--icc', action='store_true', help='Extract icc colour profile'
)

parser.add_argument(
    '-o', '--output', type=str, nargs=1, required=False,
    help='output directory, if you convert multiple kra files, each'
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

srgb = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'sRGB.icc')


def extract_png(kras, outdir):
    for kra in kras:
        png = kra.get_merged_image()
        png_name = kra.get_basename() + '.png'
        png_name_web = kra.get_basename() + '_srgb.png'

        png_dir = os.path.join(outdir, kra.get_basename(), 'png')
        os.makedirs(png_dir, exist_ok=True)
        kra.merged_image_path = os.path.join(png_dir, png_name)

        with open(kra.merged_image_path, 'w+b') as f:
            f.write(png)
            f.close()

        if args.webready:
            im = Image.open(kra.merged_image_path)

            # BUG: I don't know why but I need to use inPlace here or else
            # my test png was just transparent
            ImageCms.profileToProfile(im, kra.icc_path, srgb, inPlace=True)
            im.save(os.path.join(png_dir, png_name_web), optimize=True)


def extract_icc(kras, outdir):
    for kra in kras:
        icc = kra.get_icc()
        icc_dir = os.path.join(outdir, kra.get_basename(), 'icc')
        os.makedirs(icc_dir, exist_ok=True)
        kra.icc_path = os.path.join(icc_dir, icc['name'])

        with open(kra.icc_path, 'w+b') as f:
            f.write(icc['data'])
            f.close()


def save_as_jpeg(im, kra, jpeg_name, jpeg_dir):
    if args.webready:
        im = ImageCms.profileToProfile(im, kra.icc_path, srgb)
        im.save(os.path.join(jpeg_dir, jpeg_name), quality=args.jpeg, optimize=True)
    else:
        im.save(os.path.join(jpeg_dir, jpeg_name), quality=args.jpeg, optimize=True, icc_profile=kra.icc)

def export_as_jpegs(kras, outdir):
    for kra in kras:
        """
        Create one jpeg with the original size
        """
        jpeg_dir = os.path.join(outdir, kra.get_basename(), 'jpeg')
        os.makedirs(jpeg_dir, exist_ok=True)
        im = Image.open(kra.merged_image_path)
        jpeg_name = kra.get_basename() + '_original.jpeg'
        save_as_jpeg(im, kra, jpeg_name, jpeg_dir)

        for size in args.sizes:
            im = Image.open(kra.merged_image_path)
            jpeg_name = kra.get_basename() + '{0}.jpeg'.format(size)
            im.thumbnail((size, size), Image.ANTIALIAS)
            save_as_jpeg(im, kra, jpeg_name, jpeg_dir)

def main():
    kras = []

    outdir = args.output

    depend_on_png = (args.jpeg,)

    if args.webready and not args.icc:
        raise SystemExit('I need -i to get the source icc profile')

    if not args.png and any(depend_on_png):
        raise SystemExit('Some options work only if you specify -p')

    if args.kras:
        for krafile in args.kras:
            kras.append(kra.Kra(krafile))

    if args.icc:
        extract_icc(kras, outdir)

    if args.png:
        extract_png(kras, outdir)

    if args.jpeg:
        export_as_jpegs(kras, outdir)


if __name__ == '__main__':
    main()
