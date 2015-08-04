# Frequently used commands

.PHONY: help messages compile staging live publish

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  init       initialize virtual enviroment and install requirements"
	@echo "  staging    generate staging site html files"
	@echo "  live       replace live site with staging site"
	@echo "  publish    push changes stored in git to production server"

init:
	@bin/init-envs.sh

staging:
	@bin/staging-gen.sh

live:
	@bin/live-copy.sh

publish:
	@git push origin master

