#!/bin/bash

GIT_ROOT="$(cd "$(dirname "$0")/../.." ; pwd -P)"
STAGING_DIR="staging"
LIVE_DIR="live"

cd "${GIT_ROOT}"
# Move stored site as new site
if [ -d "${STAGING_DIR}" ] && [ -d "${LIVE_DIR}" ]; then
	rm -rf "${LIVE_DIR}"
	cp -va "${STAGING_DIR}" "${LIVE_DIR}"
else
	echo "Couldn't found staging or live site directory"
fi
