#!/bin/bash

set -e

SOURCE_DIR="$(cd "$(dirname "$0")/.." ; pwd -P)"
cd "${SOURCE_DIR}"
virtualenv envs
source envs/bin/activate
pip install -r doc/requirements.txt
