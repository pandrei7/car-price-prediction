SHELL := /usr/bin/env bash

.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "run_app         - run the web application"
	@echo "download_images - scrape images from Autovit"
	@echo "crop_images     - crop the downloaded images"

# Run the web application.
.PHONY: run_app
run_app:
	python3 -m src.app.main

# Download Autovit images from a range of URLs.
.PHONY: download_images
download_images:
	@set -e ;\
	URL=https://www.autovit.ro/autoturisme/second?search%5Border%5D=created_at_first%3Adesc ;\
	python3 src/scraping/autovit_imgs.py --dir data/autovit_images --urls "$$URL&page="{1..2} ;\

# Crop the downloaded images to a separate directory.
.PHONY: crop_images
crop_images:
	rm -rf data/small_images
	@echo "Copying original images..."
	cp -r data/autovit_images data/small_images
	@echo "Cropping images..."
	find data/small_images -type f -name "*.webp" -exec mogrify \
		-resize 220x220^  -gravity Center -extent 220x220 "{}" \;