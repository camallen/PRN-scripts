'''

create_pipeline_manifest.py takes user input about a PRN activation event.
This metadata is used to locate and process the source before and after event imagery
to Zooniverse subjects
stored creates a json file

This information includes:
1. Event name and Region of interest (ROI) coordinate details
2. Before and after source GeoTIFF imagery locations in s3 and the provider information
3. The Zooniverse project and subject set to upload the tiled data into
4. S3 bucket and path details for storing data products created by the PRN pipeline E.G. extracted and formatted raw classifcation data for use by IBCC code
'''

import sys, os, io, json
# import pdb
data = {}
# get the event metadata from the user
data['name'] = input('What is the event name the PRN is activating for? ')
latitude = input('What are the region of interest (ROI) latitude co-coordinates? ')

data['roi'] = latitude


json_manifest_file_path = 'outputs/prn_pipeline_manifest.json'

# write the output data as json file
with open(json_manifest_file_path, 'w') as f:
    # json.dump(data, f, sort_keys = True, indent = 2, ensure_ascii=False)
    json.dump(data, f, ensure_ascii=False)

# TODO: upload the pipeline definition to s3
