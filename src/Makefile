# Frequently used commands

.PHONY: help messages compile staging live publish

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  init       initialize virtual enviroment and install requirements"
	@echo "  messages   extract translation strings and update translation catalogs"
	@echo "  compile    compile translation catalogs"
	@echo "  staging    generate static html files in staging branch"
	@echo "  live       push staging branch into live branch"
	@echo "  pull       pull all branches from remote repository"
	@echo "  push       push all branches to remote repository"

init:
	@../bin/init-envs.sh

messages:
	@pybabel extract -F babel.cfg -o messages.pot .
	@pybabel update -i messages.pot -d translations

compile:
	@pybabel compile -d translations

staging:
	@../bin/staging-gen.sh

live:
	@../bin/live-copy.sh

pull:
	@../bin/pull-all.sh

push:
	@../bin/push-all.sh

