'''

create_manifest.py takes the before and after tile csv files and combines them to a single
zooniverse upload csv manifest for use by the panoptes cli subject uploader

'''

import sys, os, re
import pandas as pd
import pdb

executable = sys.argv[0]

try:
    before_csv_infile = sys.argv[1]
    after_csv_infile  = sys.argv[2]
except:
    print("\nUsage: %s before_files_extra.csv after_files_extra.csv" % executable)
    print("      before_files_extra.csv is the before epoch tile metadata from convert_tiles_to_jpg.py")
    print("      after_files_extra.csv  is the after epoch tile metadata from convert_tiles_to_jpg.py")
    sys.exit(0)
# TODO: add provider provider param for input for correct subject metadata source attribution

# read both into pandas data frames?
before_manifest_df = pd.read_csv(before_csv_infile)
after_manifest_df = pd.read_csv(after_csv_infile)

# TODO: find a pandas way to compare the set of columns in each data from
for index, row in before_manifest_df.iterrows():
    try:
        after_manifest_row = after_manifest_df.loc[index]
    except KeyError as e:
        print('\nError: files do not match!')
        print('Unknown row %s in after manifest file: %s' % (index, e))
        break

    # check the file names match
    # pdb.set_trace()
    before_prefix, before_suffix = re.split("before", row['tif_file'])
    after_prefix, after_suffix = re.split("after", after_manifest_row['tif_file'])
    tif_file_names_match = (before_prefix == after_prefix) and (before_suffix == after_suffix)

    before_prefix, before_suffix = re.split("before", row['jpg_file'])
    after_prefix, after_suffix = re.split("after", after_manifest_row['jpg_file'])
    jpg_file_names_match = (before_prefix == after_prefix) and (before_suffix == after_suffix)

    # pdb.set_trace()
    if not (tif_file_names_match and jpg_file_names_match):
        print('\nError: file tiling name parts do not match!')
        print('Tile filenames in manifests for row %s do not match.and can not be grouped into 1 subject!' % (index))
        print('%s and %s' % (row['tif_file'], after_manifest_row['tif_file']))
        print('%s and %s' % (row['jpg_file'], after_manifest_row['jpg_file']))
        break


    # TODO: a much better way of comparing col values
    # cols_to_compare = ['lon_min', 'lon_max', 'lat_min', 'lat_max']
    lon_min_match = row['lon_min'] == after_manifest_row['lon_min']
    lon_max_match = row['lon_max'] == after_manifest_row['lon_max']
    lat_min_match = row['lat_min'] == after_manifest_row['lat_min']
    lat_max_match = row['lat_max'] == after_manifest_row['lat_max']

    geo_cords_match = lon_min_match and lon_max_match and lat_min_match and lat_max_match
    if not geo_cords_match:
        print('\nError: files do not match!')
        print('Geo coords in manifests for row %s have different coords!' % (index))
        break



# compare the
