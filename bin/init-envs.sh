#!/bin/bash

set -e

GIT_ROOT="$(cd "$(dirname "$0")/.." ; pwd -P)"
cd "${GIT_ROOT}"

virtualenv envs
source envs/bin/activate
pip install -r doc/requirements.txt
