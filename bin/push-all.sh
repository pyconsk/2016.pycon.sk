#!/bin/bash

GIT_ROOT="$(cd "$(dirname "$0")/.." ; pwd -P)"

cd "${GIT_ROOT}"

git push -f --all
