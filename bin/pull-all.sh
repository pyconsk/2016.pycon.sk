#!/bin/bash

GIT_ROOT="$(cd "$(dirname "$0")/.." ; pwd -P)"

cd "${GIT_ROOT}"

for branch in staging live master; do
	echo "Switching to branch ${branch}"
	git checkout "${branch}" && git pull origin ${branch}
	echo
done
