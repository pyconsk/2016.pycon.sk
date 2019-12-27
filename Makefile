# Frequently used commands

.PHONY: help messages compile staging live publish

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  init       initialize virtual enviroment and install requirements"
	@echo "  messages   extract translation strings and update translation catalogs"
	@echo "  compile    compile translation catalogs"
	@echo "  live       generate static site into /docs folder"
	@echo "  pull       pull all branches from remote repository"
	@echo "  push       push all branches to remote repository"

init:
	@bin/init-envs.sh

messages:
	@cd src && pybabel extract -F babel.cfg -o messages.pot .
	@cd src && pybabel update -i messages.pot -d translations

compile:
	@cd src && pybabel compile -d translations

live:
	@bin/live-gen.sh

pull:
	@bin/pull-all.sh

push:
	@bin/push-all.sh

