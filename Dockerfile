FROM python:3.8
# install the notebook package
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache poetry

RUN poetry install --extras ["all"]

# create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}
USER ${USER}