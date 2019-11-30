SHELL := /bin/bash

.PHONY: all
all: clean build


.PHONY: install_deps
install_deps:
	pushd ./api && \
		poetry install && \
		popd


.PHONY: clean
clean:
	find . -type f -iname "*.pyc" -or -type d -name "__pycache__" -delete;
	rm -rf ./dist \
		./api/dist \
		./api/wsi_api/app/{ui,db}


.PHONY: build
build: clean install_deps
	@# Prep the static asset folders in package
	mkdir -p ./api/wsi_api/app/{ui,db}

	@# Copy over the built UI
	cp -rv ui/* ./api/wsi_api/app/ui/

	@# Copy over the database
	cp ./data/wsi_data.db ./api/wsi_api/app/db/

	@# Build the package!
	pushd ./api && \
		poetry build -vv && \
		popd

	@# Show us the goods
	mv ./api/dist .


.PHONY: bump
bump:
	pushd ./api && \
		poetry version && \
		popd

.PHONY: version
version:
	@grep version ./api/pyproject.toml | cut -d\" -f2


# This is nightmarish and leads to redundant builds.
# Bump versions manually for now. Build numbers in CircleCI might be
# a solution.
#
# .PHONY: ci_build
# ci_build: bumpversion build
# 	git add ./api/pyproject.toml
# 	git commit -m "CircleCI: Version Bump"
# 	git push origin master
