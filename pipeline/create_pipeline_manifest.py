'''

create_pipeline_manifest.py takes user input about a PRN activation event.
This metadata is used to locate and process the source before and after event imagery
to Zooniverse subjects
stored creates a json file

This information includes:
1. Event name and Region of interest (ROI) bounding box coordinates
2. Before and after source GeoTIFF imagery locations in s3 and the provider information
3. The Zooniverse project and subject set to upload the tiled data into
4. S3 bucket and path details for storing data products created by the PRN pipeline E.G. extracted and formatted raw classifcation data for use by IBCC code
'''

import sys, os, io, json, datetime
current_dt = datetime.datetime.now()

data = { "date": current_dt.strftime("%Y/%m/%d") }

# get the event metadata from the user
data['name'] = input('What is the event name the PRN is activating for? ')
west_longitude = input('What is the most westerly bounding longitude coordinate? ')
south_latitude = input('What is the most southerly bounding latitude coordinate? ')
east_longitude = input('What is the most easterly bounding longitude coordinate? ')
north_latitude = input('What is the most northerly bounding latitude coordinate? ')

# https://wiki.openstreetmap.org/wiki/Bounding_Box
# bbox = left,bottom,right,top
data['bounding_box_coords'] = [ west_longitude, south_latitude, east_longitude, north_latitude ]

# Before and after source GeoTIFF imagery locations in s3 and the provider information
before_image_file_name = input('What is file name of the before GeoTIFF image? ')
after_image_file_name = input('What is file name of the after GeoTIFF image? ')

data['geotiff_source_imagery'] = {
    "before_image_file_name": before_image_file_name,
    "after_image_file_name": after_image_file_name
}

zoo_project_id = input('What is the tPRN Zooniverse project id? ')
zoo_subject_set_id = input('What is the tPRN Zooniverse subject_set_id to upload data into? ')

data['zooniverse_metadata'] = {
    "project_id": zoo_project_id,
    "subject_set_id": zoo_subject_set_id
}

# TODO: add s3 bucket and folder path details
# S3 bucket and path details for storing data products created by the PRN pipeline E.G. extracted and formatted raw classifcation data for use by IBCC code


json_manifest_file_path = 'outputs/prn_pipeline_manifest.json'
# write the output data as json file
with open(json_manifest_file_path, 'w') as f:
    # json.dump(data, f, sort_keys = True, indent = 2, ensure_ascii=False)
    json.dump(data, f, ensure_ascii=False)

# TODO: upload the pipeline definition to s3
