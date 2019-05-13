#!/bin/bash

VENV_DIR=/opt/configure_wifi
pushd "$(dirname $0)"
  ${VENV_DIR}/bin/gunicorn --bind 0.0.0.0:8000 --threads 2 --workers 2 wifi:app
popd
