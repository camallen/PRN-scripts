'''

create_manifest.py takes the before and after tile csv files and combines them to a single
zooniverse upload csv manifest for use by the panoptes cli subject uploader

'''

import sys, os, re
import pandas as pd
import pdb # pdb.set_trace()

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

print("Constructing the before / after manifest upload CSV...")

# use the data dir for outputs from the make tiles as inputs here
tiled_data_dir = os.environ.get('DATA_OUT_DIR','outputs/')

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
    before_prefix, before_suffix = re.split("before", row['tif_file'])
    after_prefix, after_suffix = re.split("after", after_manifest_row['tif_file'])
    tif_file_names_match = (before_prefix == after_prefix) and (before_suffix == after_suffix)

    before_prefix, before_suffix = re.split("before", row['jpg_file'])
    after_prefix, after_suffix = re.split("after", after_manifest_row['jpg_file'])
    jpg_file_names_match = (before_prefix == after_prefix) and (before_suffix == after_suffix)

    if not (tif_file_names_match and jpg_file_names_match):
        print('\nError: file tiling name parts do not match!')
        print('Tile filenames in manifests for row %s do not match.and can not be grouped into 1 subject!' % (index))
        print('%s and %s' % (row['tif_file'], after_manifest_row['tif_file']))
        print('%s and %s' % (row['jpg_file'], after_manifest_row['jpg_file']))
        break

    # The tif files are created by gdal so will exist
    # jpg files are via a shell script using `convert`
    # this program may error, report and continue leaving some missing JPG images
    before_jpg_path = "%s/tiles_before_jpg/%s" % (tiled_data_dir, row['jpg_file'])
    after_jpg_path = "%s/tiles_after_jpg/%s" % (tiled_data_dir, after_manifest_row['jpg_file'])
    jpg_files_exist = os.path.isfile(before_jpg_path) and os.path.isfile(after_jpg_path)
    if not jpg_files_exist:
        print('\nError: missing JPG subject files!')
        print('Check the before file exists: %s' % before_jpg_path)
        print('Check the after file exists: %s' % after_jpg_path)
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

# All input validations have passed!

# construct a combined data from that will create the resulting manifest
# copying the the jpg before tile and associated metadata
# and append the after subject tile jpg as well

# sizes = [getsizes_local(q) for q in tileparams.tif_file]
# prm_zoo_manifest['tifsize_x_pix'] = [q[0] for q in sizes]
# prm_zoo_manifest['tifsize_y_pix'] = [q[1] for q in sizes]
# prm_zoo_manifest['imsize_x_pix'] = magfac * tileparams['tifsize_x_pix']
# prm_zoo_manifest['imsize_y_pix'] = magfac * tileparams['tifsize_y_pix']
# prm_zoo_manifest['google_maps_link'] = [get_gmaps(q) for q in tileparams.iterrows()]
# prm_zoo_manifest['openstreetmap_link'] = [get_osm(q) for q in tileparams.iterrows()]
# prm_zoo_manifest.to_csv('manifest_output_path')

# Add attribution columns for DG, Planet etc
# so that each subject has the required image attribution and license information.

# add image scale coords in (put this into the convert_tiles_to_jpg.py script?)
# x_km = (row['x_m_max'] - row['x_m_min']) / 1000
# y_km = (row['y_m_max'] - row['y_m_min']) / 1000


# look at hiding most metadata from talk
# In future deployments it might be good to hide most of the metadata columns so that people don’t have to scroll to get to the Maps links (which always seem to show up at the bottom no matter where they are in the manifest). But that will require making my processing scripts able to deal with the “//”, “#” and “!” prefixes that would be needed for that. So I haven’t done it yet.
