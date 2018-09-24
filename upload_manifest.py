'''

create_manifest.py takes the before and after tile csv files and combines them to a single
zooniverse upload csv manifest for use by the panoptes cli subject uploader

'''

import sys, os, re, argparse
import pandas as pd
import pdb # pdb.set_trace()

parser = argparse.ArgumentParser(description='Create a tiled image data csv manifest to upload subjects to the Zooniverse.')
parser.add_argument('--marshal-dir', dest='marshal_dir', help='the directory to marshal the file uploads from')
parser.add_argument('manifest_csv_file',help='the path to the subject manifest csv file')

args = parser.parse_args()

tiled_data_dir = os.environ.get('DATA_OUT_DIR','outputs/')

manifest_csv_file = args.manifest_csv_file
marshal_dir = "%s/%s" % (tiled_data_dir, args.marshal_dir)

# setup the tile output paths
if not os.path.exists(marshal_dir):
    os.mkdir(marshal_dir)

print("Corralling the  manifest subject file data into ...")

manifest_csv_file_df = pd.read_csv(manifest_csv_file)

for index, row in manifest_csv_file_df.iterrows():
    # TODO: move the file data from before / after dirs to the corral dir
    # tiled_data_dir
    before_file_path = "%s/tiles_before_jpg/%s" % (tiled_data_dir, row['jpg_file_before'])
    symlink_path = "%s/%s" % (marshal_dir, row['jpg_file_before'])
    # TODO do this once and detect previously linked states
    os.symlink(os.path.abspath(before_file_path), symlink_path)

    pdb.set_trace()


    # os.path.isfile(symlink_path)
    # os.unlink(symlink_path)
