.PHONY: all
all: clean build

.PHONY: clean
clean:
	find . -type f -iname "*.pyc" -or -type d -name "__pycache__" -delete
	rm -rf ./dist
	rm -rf ./api/dist
	rm -rf ./api/wsi_api/app/{ui,db}

.PHONY: build
build: clean
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
