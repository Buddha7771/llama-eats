import logging

import requests

from llama_eats.models import NotionDatabaseEntry

logger = logging.getLogger(__name__)


class NotionAPIError(Exception):
    """Custom exception for Notion API errors."""


class NotionClient:
    """Client for interacting with Notion's API to fetch database entries."""

    database_url = "https://api.notion.com/v1/databases"

    def __init__(self, token: str) -> None:
        self.token = token

    @property
    def headers(self) -> dict:
        """Return headers for Notion API requests."""
        return {
            "Authorization": "Bearer " + self.token,
            "Notion-Version": "2022-02-22",
        }

    def fetch_database(self, database_id: str) -> list[NotionDatabaseEntry]:
        """Fetch a database from Notion.

        Notion database must have the following properties:
        - title: Title of the paper
        - abstract: Abstract of the paper
        - URL: URL of the paper

        Parameters
        ----------
        database_id: str
            The ID of the Notion database to fetch.

        Returns
        -------
        list[NotionDatabaseEntry]
            A list of entries from the Notion database.

        """
        try:
            url = f"{self.database_url}/{database_id}/query"
            response = requests.post(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            msg = f"Failed to fetch Notion database {database_id}: {e}"
            logger.exception(msg)
            raise NotionAPIError(msg) from e

        data = response.json()
        results = data.get("results", [])
        entries = []

        try:
            for result in results:
                properties = result["properties"]
                title = properties["title"]["title"]
                abstract = properties["abstract"]["rich_text"]
                url = properties["URL"]["url"]

                if not title or not abstract:
                    continue

                title_text = title[0].get("text", {}).get("content", "")
                abstract_text = abstract[0].get("text", {}).get("content", "")

                if not title_text or not abstract_text:
                    continue

                entry = NotionDatabaseEntry(
                    title=title_text,
                    abstract=abstract_text,
                    url=url or "",
                )
                entries.append(entry)
        except (KeyError, IndexError) as e:
            msg = f"Failed to parse Notion database entry: {e}"
            logger.exception(msg)
            raise NotionAPIError(msg) from e
        else:
            return entries
