SHELL := /usr/bin/env bash

.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "download_images - scrape images from Autovit"

# Download Autovit images from a range of URLs.
.PHONY: download_images
download_images:
	@set -e ;\
	URL=https://www.autovit.ro/autoturisme/second?search%5Border%5D=created_at_first%3Adesc ;\
	python3 src/scraping/autovit_imgs.py --dir data/autovit_images --urls "$$URL&page="{1..2} ;\
