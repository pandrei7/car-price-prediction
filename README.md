# Car Price Prediction

## Download images

If you want to scrape the images yourself, you can do so using the
`download_images` Makefile rule:

```bash
make download_images
```

This will download images from Autovit into the `data` directory.

> **Note** that you should probably set which pages you want to scrape. Do this
> by changing the two numbers in the command of this rule, inside `Makefile`.

If you want to change the rate limit used during scraping (for example, to make
it run faster), you should change the limits inside the script itself.
