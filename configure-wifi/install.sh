#!/bin/bash

# To be executed in the Raspberry
VENV_DIR=/opt/configure_wifi
virtualenv "${VENV_DIR}"
${VENV_DIR}/bin/pip install -r requirements.txt

sed -i.bk  -s "s#^VENV_DIR=.*#VENV_DIR=${VENV_DIR}#g" start.sh
chmod +x start.sh

chmod +x rc3.d/S99configure-wifi
cp rc3.d/S99configure-wifi /etc/rc3.d/
