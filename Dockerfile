FROM continuumio/anaconda:5.2.0

MAINTAINER Zooniverse <contact@zooniverse.org>

WORKDIR /tprn

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        imagemagick \
        && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p data

ADD conda_env/tprn.yml /tprn

# Use the below to manually create a conda env and export it for re-use
# RUN conda create -y -n tprn
# RUN conda activate tprn
# RUN conda install gdal pandas ujson pyproj
# RUN conda env export > conda_env/tprn.yml

# use the manually created conda env to setup
RUN conda env create -f tprn.yml

# setup conda to use the env we just imported
RUN echo "source activate $(head -1 tprn.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 tprn.yml | cut -d' ' -f2)/bin:$PATH

ADD ./ /tprn
