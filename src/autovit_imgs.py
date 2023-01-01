"""Parse car images from Autovit.

This module helps parse car images from Autovit.
It can be used as a stand-alone script.
"""

import argparse
import copy
from dataclasses import dataclass
import logging
import os
import re
from typing import List, Optional, Union, cast
from urllib.request import urlopen

from bs4 import BeautifulSoup
from bs4.element import Tag
import ratelimit


# Utility type alias for values which work like paths.
PathLike = Union[str, os.PathLike]


@dataclass
class ArticleInfo:
    """Contains metadata about an article (a car)."""
    article: Tag
    id: str
    img_url: Optional[str]
    name: str


@dataclass
class Image:
    """Wraps an image and its metadata."""
    image: bytes
    info: ArticleInfo


# Maximum number of requests in a `LIMIT_PERIOD` period.
LIMIT_CALLS: int = 1
# Duration of a period, in seconds.
LIMIT_PERIOD: int = 2


def download_webpage(url: str) -> str:
    """Download a text page from a given URL."""
    resp = urlopen(url).read().decode('utf-8')
    return resp


def download_image(url: str) -> bytes:
    """Download the raw bytes of an image from a given URL."""
    return urlopen(url).read()


@ratelimit.sleep_and_retry
@ratelimit.limits(calls=LIMIT_CALLS, period=LIMIT_PERIOD)
def check_autovit_limit() -> None:
    """
    Utility function which forces requests to Autovit to respect rate limits.

    This function should be used as a "guard", simply call it before you make a
    request.
    """
    pass


def download_autovit_webpage(url: str) -> str:
    """Download a webpage from Autovit, respecting rate limits."""
    check_autovit_limit()
    return download_webpage(url)


def download_autovit_image(url: str) -> bytes:
    """Download an image from Autovit, respecting rate limits."""
    check_autovit_limit()
    return download_image(url)


def parse_article_info(article: Tag) -> ArticleInfo:
    """Parse relevant metadata about an article."""
    # Index pages seem to only include thumbnails of cars. They "create" these
    # thumbnails by appending the wanted image size to the URL. If we remove
    # this part of the URL, we should have access to the full image.
    try:
        img_size_pattern = r";s=\d+x\d+$"
        img_url = cast(Tag, article.find("img")).attrs["src"]
        img_url = re.sub(img_size_pattern, "", img_url)
    except:
        img_url = None

    return ArticleInfo(
        article=copy.copy(article),
        id=article.attrs["id"],
        img_url=img_url,
        name=cast(Tag, article.find("a")).text,
    )


def parse_index_page(html: str) -> Optional[List[ArticleInfo]]:
    """Extract all articles found in a page."""
    # Articles are <article> tags inside the page's only <main> tag.
    soup = BeautifulSoup(html, "html.parser")

    main_tag = cast(Tag, soup.find("main"))
    if main_tag is None:
        return None

    articles = main_tag.find_all("article")
    return [parse_article_info(a) for a in articles]


def obtain_image(info: ArticleInfo) -> Optional[Image]:
    """Downloads the image corresponding to an article from Autovit."""
    if info.img_url is None:
        return None

    image_bytes = download_autovit_image(info.img_url)
    return Image(image=image_bytes, info=copy.copy(info))


def save_dir(info: ArticleInfo, output_dir: PathLike) -> str:
    """Returns the path of the directory where an article's info is saved."""
    return os.path.join(output_dir, info.id)


def done_path(info: ArticleInfo, output_dir: PathLike) -> str:
    """Return the path of the file that says an article has been processed."""
    return os.path.join(save_dir(info, output_dir), ".done")


def already_scraped(info: ArticleInfo, output_dir: PathLike) -> bool:
    """Check if a given article can already be found on disk."""
    return os.path.isfile(done_path(info, output_dir))


def save_to_disk(image: Image, output_dir: PathLike) -> None:
    """Save all information related to an image to disk."""
    save_path = save_dir(image.info, output_dir)

    # Make sure the directory exists.
    os.makedirs(save_path, exist_ok=True)

    # Save the image to disk.
    img_path = os.path.join(save_path, f"{image.info.id}.webp")
    with open(img_path, "wb") as fout:
        fout.write(image.image)

    # Save the "metadata" to disk.
    metadata_path = os.path.join(save_path, f"metadata.html")
    with open(metadata_path, "w") as fout:
        fout.write(str(image.info.article))

    # Remember that we processed this article.
    with open(done_path(image.info, output_dir), "w") as fout:
        fout.write(image.info.name)


def main(index_pages_urls: List[str], output_dir: PathLike) -> None:
    """Scrape the given webpages and save the results to disk."""
    for i, index_url in enumerate(index_pages_urls):
        while True:
            html = download_autovit_webpage(index_url)
            if infos := parse_index_page(html):
                break
            logging.warning(f"Failed to parse {index_url}. Retrying...")

        logging.info(f"Starting page #{i} ({len(infos)} entries): {index_url}")
        for j, info in enumerate(infos):
            if already_scraped(info, output_dir):
                logging.info(
                    f"Skipping article, seems known: {info.id} ({info.name})")
                continue

            if image := obtain_image(info):
                save_to_disk(image, output_dir)
                logging.info(f"Done {j:2}: {info.id} {info.name}")
            elif info.img_url is None:
                logging.info(f"Article lacks image: {info.id} ({info.name})")

        logging.info(f"Done page #{i}")


if __name__ == "__main__":
    # Customize the logger.
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description="Autovit Image Scraper",
        epilog="""This tool expects \"index\" URLs which contain multiple
cars, such as the main search page on Autovit.""",
    )
    parser.add_argument(
        "--dir", help="The output directory", type=str, required=True)
    parser.add_argument(
        "--urls", help="The list of \"index\" URLs to parse",
        nargs=argparse.REMAINDER, required=True)
    args = parser.parse_args()

    # Run the scraper.
    main(args.urls, args.dir)
