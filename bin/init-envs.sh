#!/bin/bash

set -e

GIT_ROOT="$(cd "$(dirname "$0")/.." ; pwd -P)"
cd "${GIT_ROOT}"

python3 -m venv envs3
source envs3/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
