#!/bin/bash

GIT_ROOT="$(cd "$(dirname "$0")/.." ; pwd -P)"
STAGING_DIR="web"

cd "${GIT_ROOT}"

git push . staging:live
