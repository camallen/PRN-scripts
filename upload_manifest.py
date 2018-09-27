'''

create_manifest.py takes the before and after tile csv files and combines them to a single
zooniverse upload csv manifest for use by the panoptes cli subject uploader

'''

import sys, os, re, argparse, subprocess
import pandas as pd
import pdb # pdb.set_trace()
from panoptes_cli.commands import subject_set
from panoptes_client import Panoptes

# allow OS env to set a defaultS
default_batch_size = os.environ.get('BATCH_SIZE',10)
default_marshal_dir = os.environ.get('MARSHAL_DIR','marshal_dir')
tiled_data_dir = os.environ.get('DATA_OUT_DIR','outputs/')

parser = argparse.ArgumentParser(description='Create a tiled image data csv manifest to upload subjects to the Zooniverse.')
parser.add_argument('--marshal-dir', dest='marshal_dir', default=default_marshal_dir, help='the directory to marshal the file uploads from')
parser.add_argument('--batch-size', dest='batch_size', default=default_batch_size, help='the number of subjects to attempt to upload at once')
parser.add_argument('--admin-mode', dest='admin_mode', default=False, help='run the Zooniverse CLI in admin mode')
parser.add_argument('--subject-set', dest='subject_set_id', help='the subject set to upload the data to', required=True)
parser.add_argument('manifest_csv_file',help='the path to the subject manifest csv file')

args = parser.parse_args()

manifest_csv_file_path = args.manifest_csv_file
marshal_dir = "%s/%s" % (tiled_data_dir, args.marshal_dir)
batch_size = args.batch_size
admin_mode = args.admin_mode
subject_set_id = args.subject_set_id

# setup the tile output paths
if not os.path.exists(marshal_dir):
    os.mkdir(marshal_dir)

print("Marshaling the manifest subject file data into directory for uploads...")

manifest_csv_file_df = pd.read_csv(manifest_csv_file_path)

# TODO: find out if we are resuming a previously borked upload
# use a file to indicate this state
upload_state_tracker_path = "%s/%s" % (tiled_data_dir, 'upload_state_tracker.txt')

proc_to_find_last_uploaded_index = subprocess.run(["tail", "-n", "1", upload_state_tracker_path], capture_output=True)
# Proxy for missing file
# CompletedProcess(args=['tail', '-n', '1', 'outputs/upload_state_tracker.txt'],
#   returncode=1, stdout=b'',
#   stderr=b"tail: cannot open 'outputs/upload_state_tracker.txt' for reading: No such file or directory\n"
#)
if proc_to_find_last_uploaded_index.returncode == 1:
    # start at the beginning
    last_uploaded_index = 0
else:
    # file format is index,last_file_name.txt
    tail_output = str(proc_to_find_last_uploaded_index.stdout, 'utf-8')
    last_uploaded_index = int(tail_output.split(',')[0])

manifest_rows_to_upload_in_batch = []
batch_number = 1

# setup access to the Zooniverse API
username = os.environ.get('ZOONIVERSE_USERNAME')
password = os.environ.get('ZOONIVERSE_PASSWORD')
creds_exist = username and password
if not creds_exist:
    print("Missing zooniverse credentials, pass them in as environment variables")
    exit(1)
Panoptes.connect(username=username, password=password, admin=admin_mode)

# symlink all the tiled jpg data to the marshaling dir for uplaod
for index, row in manifest_csv_file_df.iterrows():
    # skip to where we were up to
    if index <= last_uploaded_index:
        continue

    # add the row to the batch we are processing
    manifest_rows_to_upload_in_batch.append(row)
    num_rows_in_batch = len(manifest_rows_to_upload_in_batch)

    if num_rows_in_batch == batch_size:
        print("Uploading batch number: %s" % batch_number)

        # link the row data for uploading
        before_file_path = "%s/tiles_before_jpg/%s" % (tiled_data_dir, row['jpg_file_before'])
        symlink_path = "%s/%s" % (marshal_dir, row['jpg_file_before'])
        if not os.path.isfile(symlink_path):
            os.symlink(os.path.abspath(before_file_path), symlink_path)

        after_file_path = "%s/tiles_after_jpg/%s" % (tiled_data_dir, row['jpg_file_after'])
        symlink_path = "%s/%s" % (marshal_dir, row['jpg_file_after'])
        if not os.path.isfile(symlink_path):
            os.symlink(os.path.abspath(after_file_path), symlink_path)

        # marshal the manifest to where symlinked subjects are
        abs_path_to_manifest_file = os.path.abspath(manifest_csv_file_path)
        csv_manifest_file_name = os.path.basename(manifest_csv_file_path)
        manifest_symlink_path = "%s/%s" % (marshal_dir, csv_manifest_file_name)
        if not os.path.isfile(manifest_symlink_path):
            os.symlink(abs_path_to_manifest_file, manifest_symlink_path)

        # TODO: work on this function to be quieter (opt)
        # and not use the latest data, maybe create a branch that has the changes but on the older non-async versions

        pdb.set_trace()

        # i need to catch exceptions here and abort asap if we get any?
        # E.g. https://github.com/zooniverse/panoptes-cli/issues/83
        # Traceback (most recent call last):
        #   File "upload_manifest.py", line 109, in <module>
        #     subject_set.subject_set_upload(subject_set_id, [manifest_symlink_path], True, [], None)
        #   File "/opt/conda/envs/tprn/lib/python3.7/site-packages/panoptes_cli/commands/subject_set.py", line 277, in subject_set_upload
        #     move_created(0)
        #   File "/opt/conda/envs/tprn/lib/python3.7/site-packages/panoptes_cli/commands/subject_set.py", line 248, in move_created
        #     if subject.async_save_result():
        # TypeError: 'bool' object is not callable

        # Look into how we can better handle errors and rollback in the cli subject_st_upload function
        # i.e. delete the subjects we haven't unlinked and report back to the calling code?
        # maybe this should be here not in the CLI?

        subject_set.subject_set_upload(subject_set_id, [manifest_symlink_path], True, [], None)

        # TODO: mount the panoptes creds into the

        # write the index state to the tracker file path
        # use python code though
        upload_state_tracker_file = open(upload_state_tracker_path, "a")
        upload_state_tracker_file.write("%s,%s" % (index,row['jpg_file_before']))
        upload_state_tracker_file.close()

        # reset the batch
        manifest_rows_to_upload_in_batch = []
        # bump the batch number
        batch_number += 1

    else:
        continue


# os.path.isfile(symlink_path)
# os.unlink(symlink_path)
