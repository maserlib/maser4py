FROM python:3.8
# install pip and poetry
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache poetry

ENV CDF_URL="https://spdf.gsfc.nasa.gov/pub/software/cdf/dist/cdf38_1/cdf38_1-dist-all.tar.gz"

# install libs needed to install nasa cdf
RUN apt-get update && apt-get install -y gfortran ncurses-dev

# create user with a home directory
ARG NB_USER="maser_user"
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}
ENV PATH="/home/${NB_USER}/.local/bin:$PATH"

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}
# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}

# install cdf
RUN wget $CDF_URL
RUN tar -xf cdf38_1-dist-all.tar.gz
WORKDIR ${HOME}/cdf38_1-dist
RUN make OS=linux ENV=gnu CURSES=yes FORTRAN=no UCOPTIONS=-O2 SHARED=yes all
RUN make install

WORKDIR ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

# avoid virtualenv creation
RUN poetry config virtualenvs.create false --local
RUN poetry install --extras "all"
