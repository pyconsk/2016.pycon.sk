#!/bin/bash

GIT_ROOT="$(cd "$(dirname "$0")/.." ; pwd -P)"

cd "${GIT_ROOT}"

for branch in staging live master; do
	git checkout "${branch}"
	git pull origin ${branch}
done
