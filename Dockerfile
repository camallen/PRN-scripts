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

ADD ./ /tprn

# activate the created tprn environment from the yaml file
ENV PATH /opt/conda/envs/tprn/bin:$PATH
