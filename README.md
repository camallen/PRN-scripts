# tPRN-scripts
Scripts to help build subjects and deploy Planetary Response Network (PRN) project through the Zooniverse platform.

# Get started

Use docker-compse to run the code and attach your input data to the container
+ `TPRN_DATA_DIR=/your_tpnr_data_dir docker-compose run --rm tprn bash`

if you need to (re)build the container
+ `docker-compose build tprn`

# Running the scripts
Run the scripts through docker-compose:
+ `TPRN_DATA_DIR=/your_tpnr_data_dir docker-compose run --rm tprn python make_tiff_tiles.py`

Alternatively bash into a container and run the scripts interactively
+ `TPRN_DATA_DIR=/your_tpnr_data_dir docker-compose run --rm tprn bash`
  + from the prompt in the container
  `python make_tiff_tiles.py`
