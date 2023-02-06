# Car Price Prediction

## Running the web application

First, make sure you have installed all dependencies:

```bash
pip install -r requirements.txt
```

To run the application, use the following Makefile rule:

```bash
make run_app
```

This command will provide a URL. Access that URL using your browser.

## Scraping data

You can find notebooks for scraping data in the `src/scraping` directory.

Image are downloaded separately from other data, such as car prices or
specifications. Both notebooks expect to receive a list of offer URLs to scrape.

### Downloading images without a fixed list

If you want to scrape the images yourself, you can do so using the
`download_images` Makefile rule:

```bash
make download_images
```

This will download images from Autovit into the `data` directory. The URLs are
discovered by "browsing" the website, so you cannot chose the exact cars to
process.

> **Note** that you should probably set which pages you want to explore. Do this
> by changing the two numbers in the command of this rule, inside `Makefile`.

If you want to change the rate limit used during scraping (for example, to make
it run faster), you should change the limits inside the script itself.

## Cropping images

If you want to train a model which uses the images, you might want to crop them
to a smaller size only once, to save time during subsequent training processes.

You can use the following Makefile rule to do this:

```bash
make crop_images
```