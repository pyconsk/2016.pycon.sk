#!/bin/bash

SOURCE_DIR="$(cd "$(dirname "$0")/.." ; pwd -P)"
TMP_DIR="/tmp"
GIT_ROOT="${SOURCE_DIR}/.."
STAGING_DIR="staging"
FLASK_URL="127.0.0.1:5000"

# Go to flask templated site activate envs and run flask dev server
cd "${SOURCE_DIR}"

if [ -f envs/bin/activate ]; then
	trap 'pkill -P $(jobs -pr) 2> /dev/null' SIGINT SIGTERM EXIT
	source envs/bin/activate
	python views.py &
	echo "Running wget --mirror in 3 seconds..."
	sleep 3
else
	echo "ENVS not found!"
	exit 1
fi

# Store flask templated site as html
cd "${TMP_DIR}"

if [ -d "${FLASK_URL}" ]; then
	rm -rf "${FLASK_URL}"
fi

wget -nv http://"${FLASK_URL}"/sitemap.xml --output-document=sitemap.xml && \
wget -mkEpnv http://"${FLASK_URL}"/sk/index.html

if [ $? -eq 0 ]; then
	cd "${TMP_DIR}/${FLASK_URL}" || exit 3

	# Restore static folder
	rm -rf static
	cp -a "${SOURCE_DIR}"/static . || exit 4

	# Regenerate symlinks
	ln -s static/download files

	# Classic favicon.ico location
	ln -s static/images/favicon.ico .

    # Get mtime of main CSS
	VERSION=$(stat --format=%Y static/css/pycon.css 2> /dev/null || stat -f%m static/css/pycon.css)
    find . -type f -name "*.html" | xargs sed -i.old "s#css/pycon.css\"#css/pycon.css?v=${VERSION}\"#"
	find . -type f -name "*.old" -delete

	cd "${GIT_ROOT}"

	# Move stored site as new site
	if [ -d "${STAGING_DIR}" ]; then
		rm -rf "${STAGING_DIR}"
	fi

	mv "${TMP_DIR}/${FLASK_URL}" "${STAGING_DIR}"
else
	echo "wget FAILED!"
	exit 1
fi
