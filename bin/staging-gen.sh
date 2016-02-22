#!/bin/bash

GIT_ROOT="$(cd "$(dirname "$0")/.." ; pwd -P)"
TMP_DIR="/tmp"
SOURCE_DIR="${GIT_ROOT}/src"
STAGING_DIR="web"
FLASK_PORT="9999"
FLASK_URL="127.0.0.1:${FLASK_PORT}"
STASH_REQUIRED=""
DRY_RUN=""

cd "${GIT_ROOT}"

which git > /dev/null || exit 127
which wget > /dev/null || echo 128

if [[ ! -f envs/bin/activate ]]; then
	echo "ENVS not found!"
	exit 1
fi

if [[ "${1}" == "-n" || "${1}" == "--dry-run" ]]; then
	DRY_RUN="true"
	echo "* Dry run *"
fi

# Check whether we have some uncommited changes
GIT_STATUS="$(git status -s)"

if [[ -n "${GIT_STATUS}" ]]; then
	echo "${GIT_STATUS}"
	echo
	echo "There are some uncommited changes."
	read -p "Do you want to continue? [y/N]: " yn
	case "${yn}" in
		y|Y)
			STASH_REQUIRED="true"
			;;
		*)
			echo "Doing nothing."
			exit 1
			;;
	esac
fi

# Fetch sha1 commit hashes
MASTER_COMMIT="$(git rev-list --format=%n%s%b --max-count=1 HEAD)"
PYCON_CSS_COMMIT="$(git rev-list --max-count=1 --abbrev-commit HEAD src/static/css/pycon.css)"

# Go to flask templated site activate envs and run flask dev server
source envs/bin/activate
cd "${SOURCE_DIR}"

export FLASK_PORT
trap 'pkill -P $(jobs -pr) 2> /dev/null' SIGINT SIGTERM EXIT
python views.py &
echo "Running wget --mirror in 3 seconds..."
sleep 3

# Store flask templated site as html into temp folder
cd "${TMP_DIR}"

if [[ -d "${FLASK_URL}" ]]; then
	rm -rf "${FLASK_URL}"
fi

# Wget mirror
wget -nv http://"${FLASK_URL}"/sitemap.xml --output-document=sitemap.xml && \
wget -mkEpnv http://"${FLASK_URL}"/sk/index.html

if [[ $? -ne 0 ]]; then
	echo "wget FAILED!"
	exit 1
fi

cd "${TMP_DIR}/${FLASK_URL}" || exit 3

# Restore static folder
rm -rf static
cp -a "${SOURCE_DIR}"/static . || exit 4

# Classic favicon.ico location
ln -s static/images/favicon.ico .

# Get git commit hash of main CSS file
if [[ -n "${PYCON_CSS_COMMIT}" ]]; then
	find . -type f -name "*.html" | xargs sed -i.old "s#css/pycon.css\"#css/pycon.css?v=${PYCON_CSS_COMMIT}\"#"
	find . -type f -name "*.old" -delete
fi

cd "${GIT_ROOT}"

# Stop here if a dry run was requested
if [[ -n "${DRY_RUN}" ]]; then
	echo
	echo "Dry run was requested."
	echo "The result can be found in: ${TMP_DIR}/${FLASK_URL}"
	exit 0
fi

# Stash uncommited changes if needed
[[ -n "${STASH_REQUIRED}" ]] && git stash

# Go to staging branch
git checkout staging || exit 5

# Move stored site as new site
if [[ -d "${STAGING_DIR}" ]]; then
	rm -rf "${STAGING_DIR}"
fi

# Update and commit staging branch
mv "${TMP_DIR}/${FLASK_URL}" "${STAGING_DIR}"
git add .
git status
git commit -m "Updated from master ${MASTER_COMMIT}"

# Go back to master
git checkout master
[[ -n "${STASH_REQUIRED}" ]] && git stash pop || true

exit 0
