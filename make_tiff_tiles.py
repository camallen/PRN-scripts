'''

make_tiff_tiles.py takes a tiff file and tiles it, plus exports some information.
It basically runs gdal_retile.py but does so in a way that standardizes the format of filenames and folders etc
so that you can feed this information into convert_tiles_to_jpg.py.

gdal_retile options at http://www.gdal.org/gdal_retile.html

'''

import sys, os
import numpy as np
import pandas as pd
import ujson
import scipy.interpolate
import scipy.ndimage
from pyproj import Proj, transform
#import urllib
#from PIL import ImageFile
from PIL import Image

executable = sys.argv[0]

try:
    infile = sys.argv[1]
except:
    #infile = "test_gdal_retile_output.csv"
    print("\nUsage: %s image_name.tif which_epoch" % executable)
    print("      image_name.tif (or .tiff) is the name of the mosaic you want to tile")
    print("      which_epoch is either \"before\" or \"after\".")
    print("  Optional extra inputs (no spaces):")
    print("    x=size_x")
    print("    y=size_y")
    print("       image dimensions in x and y (default: x=500 y=500)")
    print("    overlap=N")
    print("       number of pixels by which you want the tiles to overlap (default: 250)")
    sys.exit(0)


if infile.endswith(".tif"):
    infile_stem = infile.replace(".tif", "")

elif infile.endswith(".tiff"):
    infile_stem = infile.replace(".tiff", "")
    os.path.basename(path)
else:
    sys.exit("ERROR: input file must be a .tiff or .tif file")

infile_base_name = os.path.basename(infile_stem)


try:
    before_or_after = sys.argv[2]
except:
    exit_program("ERROR: Must specify which epoch (before/after) - and you should triple-check this!")

epoch_l = before_or_after.lower()
epoch_t = before_or_after.capitalize()

tiledir_tiff  = "data/tiles_%s_tiff" % epoch_l
tiledir_jpg = "data/tiles_%s_jpg"  % epoch_l

if not os.path.exists(tiledir_tiff):
    os.mkdir(tiledir_tiff)
if not os.path.exists(tiledir_jpg):
    os.mkdir(tiledir_jpg)

size_x = 500
size_y = 500
overlap = 250

# check for other command-line arguments
if len(sys.argv) > 3:
    # if there are additional arguments, loop through them
    for i_arg, argstr in enumerate(sys.argv[3:]):
        arg = argstr.split('=')

        if arg[0] == "x":
            size_x = int(arg[1])
        if arg[0] == "y":
            size_y = int(arg[1])
        if (arg[0] == "overlap") | (arg[0] == "offset"):
            overlap = int(arg[1])

# this is just for suggesting parameters in the next step
# no magnification happens in the gdal_retile step
if size_x < 350:
    magnify = " cparams=\"-magnify\""
else:
    magnify = ""

if overlap > 0:
    overlapstr = "-overlap %d" % overlap
else:
    overlapstr = ''

#gdal_retile.py -v -ps 300 300 -overlap 150 -co COMPRESS=JPEG -co TILED=YES -csv st_thomas_before.csv -csvDelim "," -tileIndex st_thomas_before.shp -targetDir ./st_thomas_before_tiles_tiff/ st_thomas_before.tif
retile_command = "gdal_retile.py -v -ps %d %d %s -co COMPRESS=JPEG -co TILED=YES -csv %s.csv -csvDelim \",\" -tileIndex %s.shp -targetDir %s %s" % (size_x, size_y, overlapstr, infile_base_name, infile_base_name, tiledir_tiff, infile)

print(retile_command)
os.system(retile_command)

# now move the CSV file out of the tiled directory
csv_out_dir = os.path.dirname(infile_stem)
csv_move_command = "mv %s/%s.csv %s" % (tiledir_tiff, infile_base_name, csv_out_dir)
print(csv_move_command)
os.system(csv_move_command)



print("  ... images are tiled and saved to %s/ with tiled image coordinates in %s.csv. You may want to run:\npython %s %s.csv %s%s" % (tiledir_tiff, infile_stem, executable.replace("make_tiff_tiles.py", "convert_tiles_to_jpg.py"), infile_stem, epoch_l, magnify))


#by
