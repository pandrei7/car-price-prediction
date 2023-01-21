# Car Price Prediction

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
