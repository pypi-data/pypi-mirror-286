#!/bin/sh
cd $CI_PROJECT_DIR
apt-get update

export APPTAINER_URL=$(wget -qO- 'https://api.github.com/repos/apptainer/apptainer/releases/latest' | grep '/apptainer_' | cut -d '"' -f4)
wget -O /tmp/apptainer.deb $APPTAINER_URL
apt install -yq /tmp/apptainer.deb
pip install -U -r requirements.txt
pytest -m "not no_ci" --cov=plus_slurm && \
codecov
