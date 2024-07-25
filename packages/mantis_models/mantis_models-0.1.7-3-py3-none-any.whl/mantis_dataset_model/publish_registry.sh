#!/bin/bash
# export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
source /opt/cyber_range/cr_api_client_venv/bin/activate
python3 -m build
python3 -m twine upload --repository gitlab dist/* --config-file ./.pypirc
