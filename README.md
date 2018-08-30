# tPRN-scripts
Scripts to help build subjects and deploy Planetary Response Network (PRN) project through the Zooniverse platform.

# Get started

Use docker-compse to run the code and attach your input data to the container
+ `TPRN_DATA_DIR=/your_tpnr_data_dir docker-compose run --rm tprn bash`

if you need to (re)build the container
+ `docker-compose build tprn`

# Rebuild the conda deps and export the config
+ `docker-compose build tprn-conda-env-build`
+ `docker-compose run --rm tprn-conda-env-build bash`
+ `conda env export > conda_env/tprn.yml`

# Running the scripts
Run the scripts through docker-compose
+ `TPRN_DATA_DIR=/your_tpnr_data_dir docker-compose run --rm tprn python make_tiff_tiles.py`

Alternatively bash into a container and run the scripts interactively
+ `TPRN_DATA_DIR=/your_tpnr_data_dir docker-compose run --rm tprn bash`
  + activate the conda env
  `source activate tprn`
  + from the prompt in the container
  `python make_tiff_tiles.py`

# Tile up the before and after tiffs
To avoid specifing this every time you can setup your local data directory as an environment variable, e.g. `export TPRN_DATA_DIR=/your_tpnr_data_dir`.

If you don't do this you will have to prefix `TPRN_DATA_DIR=/your_tpnr_data_dir` before the docker-compose commands below.

For each epoch run the following commands:

1. Run *make_tiff_tiles.py* on your **before** input data (note the outputs)
`docker-compose run --rm tprn python make_tiff_tiles.py data/roi_planet_before.tif before x=500 y=500`
0. Run *convert_tiles_to_jpg.py* on your tiled **before** tiff data
`docker-compose run --rm tprn python convert_tiles_to_jpg.py data/roi_planet_before.csv before --run`
0. Run *make_tiff_tiles.py* on your **after** input data (note the outputs)
`docker-compose run --rm tprn python make_tiff_tiles.py data/roi_planet_after.tif after x=500 y=500`
0. Run *convert_tiles_to_jpg.py* on your tiled tiff data
`docker-compose run --rm tprn python convert_tiles_to_jpg.py data/roi_planet_after.csv after --run`

## TODO

Keep following the steps outlined in https://docs.google.com/document/d/1QveOh74QpxEIhxx--7t9Swahe2BmG5yBBtqhSRtLLUk/edit#

Subject import from TIFF

1. Allow the output dir to be specified through ENV vars (with default) and avoid hard coding the /data dir into the scripts
0. Ensure that the python scripts run with the conda env via bash and docker run directly (add conda env back to .bashrc and source it)
0. Check the subject metadata makes sense and add more in, e.g. add image scale to the metadata (subtract corner coordinates in meters and report as e.g. 1.8 km x 1.8 km). This is a placeholder measure for adding a proper scale bar to the jpegs.
0. auto make the subject set manifest via the tiles_*_jpg folders and the accompanying *_extra.csv file metadata. ensure they match while making the manifest
0. use the zooniverse cli tool to upload the created manifest
0. look at adding in blank image cuts (use file size as a proxy) while creating the subject manifest

Classification data export to IBCC format
1. export classification data from Zooniverse API
0. Use coleman offline aggregation tool to get the extracts for each worklfow (audit the workflow, point tool data should work)
0. Convert the flat csv files in point 2 to IBCC format (see https://github.com/zooniverse/Data-digging/blob/master/example_scripts/planetary_response_network/caribbean_irma_2017/extract_markings_to1file.py)
0. Get an example of the IBCC input format
