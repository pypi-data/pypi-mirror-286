from talc.evals import Document

import requests
import aiohttp
from readabilipy import simple_json_from_html_string
from markdownify import markdownify as md


class Web:
    def __get_readable(self, url, html: str, use_readability: bool = True):
        """Parse HTML and return the knowledge base as a list of documents."""
        # TODO: Move html documents to blob storage to store the original content before any pre-processing.
        readable = simple_json_from_html_string(html, use_readability=use_readability)
        content = md(readable["plain_content"])
        document = Document(
            url=url, title=readable["title"], content=content, filepath=url
        )
        return [document]

    def scrape(self, url: str, use_readability: bool = True) -> list[Document]:
        """Synchronously scrape a webpage and return a list of Documents."""
        # Note: Moving linking and chunking to later stages after kb upload.

        print("Scraping doc: " + url)
        response = requests.get(url)

        text: str = response.text
        return self.__get_readable(url, text, use_readability=use_readability)

    async def ascrape(self, url: str, use_readability: bool = True) -> list[Document]:
        """Asynchronously scrape a webpage and return a list of Documents."""
        # Note: Moving linking and chunking to later stages after kb upload.

        print("Scraping doc: " + url)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                text: str = await response.text()
                return self.__get_readable(url, text, use_readability=use_readability)
