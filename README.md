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
  + from the prompt in the container
  `python make_tiff_tiles.py`
