Use a pre defined manifest to contain metadata about a PRN response event and to configure a data processing pipline.

Each manifest will contain information to run the different data processing stages. I.e.

1. Tile and upload before and after event subjects to a Zooniverse PRN subject set.
0. Extract result data from the Zooniverse project.
0. Geo convert the results data to latitude and longitude and store in a location for downstream processing (IBCC).

### Example manifest
```
{
  "event": {
    "name": 'caribbean',
    "date": 'October 2018'
    "bounding_box_coords": {
      "latitude": ['y1', 'y2'],
      "longitude": ['x1', 'x2'],
    },
    "s3_metadata":
      // INSERT SOME DATE / RUN metadata to s3 event paths
      "s3_bucket_path": "planetary-response-network/data/",
      "s3_bucket_suffix": "s3.amazonaws.com"
    },
  }

  "stages": [
    {
      "name": "tile_and_upload",
      "before_source": "before_geo_tiff_image_name.tiff",
      "after_source": "after_geo_tiff_image_name.tiff",
      "imagery_source": 'planet',
      "zooniverse_project_id": "1",
      "zooniverse_subject_set_id": "1"
    },
    {
      // This stage will run coleman's code and store it in s3
      // https://aggregation-caesar.zooniverse.org/Scripts.html#extracting-data
      "name": "extract_data_from_raw_exports",
      "raw_classification_data_source": ""
      "s3_upload_path_template": "${s3_bucket_path}/extracted_raw_data/${run_date}/${project_id}-${tool_type}-extracts.csv"
    }.
    {
      // this stage will run Sam's code to convert geo location to lat / lon
      // https://github.com/AroneyS/prn_data_extract
      "name": "geo_convert_extracted_data"
      "s3_extracted_data_files_location": "${s3_bucket_path}/extracted_raw_data/",
      "s3_upload_path_template": "${s3_bucket_path}/extracted_raw_data/${run_date}/geo_converted/${project_id}-${tool_type}-extracts.csv",
      "s3_upload_IBCC_path": "${s3_bucket_path}/extracted_raw_data/${run_date}/IBCC/${project_id}-${tool_type}-extracts.csv"
    }
  ]
}
```
