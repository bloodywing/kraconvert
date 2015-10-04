# kraconvert
Converts Krita .kra files into common used files


Convert a kra to a bunch of jpeg files:

    kraconvert $HOME/pictures/pepper_n_carrot.kra -p -w -s 1000 2000 40 -j 95 -i

* -p: extract the mergedimage.png, you need this exception if you want just the icc profile
* -w: webready, converts the jpeg files to sRGB
* -s: different sizes, maintains aspect ratio
* -j: jpeg quality, in that case 95
* -i: extract the icc profile, if you use -w (webready) you need that switch

# TL;DR
If you don't need anything fancy just run

    kraconvert pepper_n_carrot.kra -i -p -w

You can even omit the '-w' if you don't need a sRGB version.