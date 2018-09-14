# tPRN-scripts
Scripts to help build subjects and deploy Planetary Response Network (PRN) project through the Zooniverse platform.

# Get started

Use docker-compse to run the code and attach your input data to the container
+ `TPRN_DATA_DIR=/your_tpnr_data_dir docker-compose run --rm tprn bash`

if you need to (re)build the container
+ `docker-compose build tprn`

#### Add your local data directory to the docker container
To allow the code to access you data directory you can specify the path via an ENV variable via `TPRN_DATA_DIR=/path/to/tiff/data` either at run time or for your shell session. This directory will be mounted into the running container to the
`/tprn/data/ directory`.

To avoid specifying this every time you can setup your local data directory as an environment variable, e.g. `export TPRN_DATA_DIR=/your_tpnr_data_dir`.

If you don't do this you will have to prefix `TPRN_DATA_DIR=/your_tpnr_data_dir` before the docker-compose commands below, e.g.
+ `TPRN_DATA_DIR=/tprn_data/ docker-compose run --rm tprn python make_tiff_tiles.py`

All the example scripts below assume you have set this env variable.

# Running the scripts
Run the scripts through docker-compose
+ `docker-compose run --rm tprn python make_tiff_tiles.py`

Alternatively bash into a container and run the scripts interactively
+ `docker-compose run --rm tprn bash`
  + activate the conda env
  `source activate tprn`
  + from the prompt in the container
  `python make_tiff_tiles.py`

# Tile up the before and after tiffs
*The input TIFF images are should be in the mounted input directory (see docker-compose.yml for more details)*
For each epoch run the following commands:

**Before images**
1. Run *make_tiff_tiles.py* on your **before** input data file
`docker-compose run --rm tprn python make_tiff_tiles.py roi_planet_before.tif before x=500 y=500`
  + Use the output `roi_planet_before.csv` file as an input to the next step
  ```
  FINISHED
  mv outputs/tiles_before_tiff/roi_planet_before.csv outputs
  ... images are tiled and saved to outputs/tiles_before_tiff/
  with tiled image coordinates in roi_planet_before.csv.
  ```
0. Run *convert_tiles_to_jpg.py* on your tiled **before** tiff data
`docker-compose run --rm tprn python convert_tiles_to_jpg.py roi_planet_before.csv before --run`

**After images**
1. Run *make_tiff_tiles.py* on your **after** input data
`docker-compose run --rm tprn python make_tiff_tiles.py roi_planet_after.tif after x=500 y=500`
0. Run *convert_tiles_to_jpg.py* on your tiled tiff data (using the output from step above as the input csv file)
`docker-compose run --rm tprn python convert_tiles_to_jpg.py roi_planet_after.csv after --run`

# Rebuild the conda deps and export the config
Note: most likely not needed right now
+ `docker-compose build tprn-conda-env-build`
+ `docker-compose run --rm tprn-conda-env-build bash`
+ `conda env export > conda_env/tprn.yml`


## TODO

Keep following the steps outlined in https://docs.google.com/document/d/1QveOh74QpxEIhxx--7t9Swahe2BmG5yBBtqhSRtLLUk/edit#

Subject import from TIFF

0. Check the subject metadata makes sense and add more in, e.g. add image scale to the metadata (subtract corner coordinates in meters and report as e.g. 1.8 km x 1.8 km). This is a placeholder measure for adding a proper scale bar to the jpegs.
0. auto make the subject set manifest via the tiles_*_jpg folders and the accompanying *_extra.csv file metadata. ensure they match while making the manifest
0. use the zooniverse cli tool to upload the created manifest
0. look at adding in blank image cuts (use file size as a proxy) while creating the subject manifest

Classification data export to IBCC format
1. export classification data from Zooniverse API
0. Use coleman offline aggregation tool to get the extracts for each worklfow (audit the workflow, point tool data should work)
0. Convert the flat csv files in point 2 to IBCC format (see https://github.com/zooniverse/Data-digging/blob/master/example_scripts/planetary_response_network/caribbean_irma_2017/extract_markings_to1file.py)
0. Get an example of the IBCC input format
