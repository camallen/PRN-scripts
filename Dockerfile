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

# use the existing conda env for deps
RUN conda env create -f tprn.yml

# allow the conda env to run via bash
RUN echo "source activate tprn" > ~/.bashrc

# activate the created tprn environment from the yaml file
ENV PATH /opt/conda/envs/tprn/bin:$PATH

# install the panoptes-cli tool for interacting with the Zooniverse API
# using a branch due to https://github.com/zooniverse/panoptes-cli/pull/86
RUN pip install --upgrade pip
RUN pip install -U git+git://github.com/zooniverse/panoptes-cli.git@allow-cli-and-api-code-use

ADD ./ /tprn
