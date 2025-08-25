from llama_eats.integrations.notion_client import NotionClient
from llama_eats.settings import settings


def test_notion_key_db_fetch():
    client = NotionClient(token=settings.notion_token)
    key_entries = client.fetch_database(settings.notion_key_db_id)

    if not key_entries:
        msg = "No entries found in the Notion key database."
        raise AssertionError(msg)

    for entry in key_entries:
        if not (entry.title and entry.abstract and entry.url):
            msg = f"Entry {entry} is missing required fields."
            raise AssertionError(msg)
