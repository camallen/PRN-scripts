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

# Tiling up your before / after tiff data
To avoid specifing this every time you can setup your local data directory as an environment variable, e.g. `export TPRN_DATA_DIR=/your_tpnr_data_dir`.

If you don't do this you will have to prefix `TPRN_DATA_DIR=/your_tpnr_data_dir` before the docker-compose commands below.

For each epoch (before / after) run the following commands:

1. Run *make_tiff_tiles.py* on your before input data (note the outputs)
`docker-compose run --rm tprn python make_tiff_tiles.py data/roi_planet_before.tif before x=500 y=500`
0. Run *convert_tiles_to_jpg.py* on your tiled tiff data
`docker-compose run --rm tprn python convert_tiles_to_jpg.py data/roi_planet_before.csv before --run`
