FROM ubuntu:22.04

RUN apt-get update && apt-get install --fix-missing -y \ 
	build-essential \
	cmake \
	gcc \
	make \
	ca-certificates \
	libglib2.0-0 \
	libjpeg-dev \
	libpng-dev \
	sudo \
	nano \
	wget \
	curl \
	gfortran \
	libopenblas-dev \ 
	liblapack-dev \
	sqlite3 \
	libsqlite3-dev \
	openslide-tools \
	lsb-release \
	libboost-dev \
	ffmpeg \
	libsm6 \
	libxext6 \
	git

# Create a non-root user and switch to it.
RUN adduser --disabled-password --gecos '' --shell /bin/bash user
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# All users can use /home/user as their home directory.
ENV HOME=/home/user
RUN chmod 777 /home/user
#RUN chmod 755 /home/user

# Install Miniconda
RUN curl -so ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh
ENV PATH=/home/user/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false
ENV CONDA_DEFAULT_ENV=anhir

# Create e.g. a Python 3.8 environment. Install mamba for speed of env creation
RUN /home/user/miniconda/bin/conda install -n base -c conda-forge mamba

ENV CONDA_PREFIX=/home/user/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH
WORKDIR /home/user/ANHIR

# creating from yaml not working on both conda and mamba - 
# check that copy operation completed successfully
# then, check that yaml file in correct format

# copy env file and install dependencies
COPY env.yaml /home/user/ANHIR
RUN mamba env create -f env.yaml
# clean
RUN /home/user/miniconda/bin/conda clean -ya

# copy ANHIR source code
RUN git clone https://github.com/MWod/ANHIR_MW.git
# add init file so ANHIR_MW repo code visible 
RUN touch ANHIR_MW/__init__.py
