import logging
from collections.abc import Generator
from datetime import datetime, timezone

import arxiv

from llama_eats.models import Paper

logger = logging.getLogger(__name__)


class ArxivClient:
    """Client for fetching papers from arXiv."""

    def __init__(self, page_size: int = 1000) -> None:
        """Initialize the ArxivClient.

        Parameters
        ----------
        page_size : int
            The number of results to fetch per page. Default is 1000.

        """
        self.client = arxiv.Client(page_size=page_size)

    def yield_papers(
        self,
        start_date: datetime,
        end_date: datetime | None = None,
        max_results: int | None = None,
    ) -> Generator[Paper, None, None]:
        """Yield papers submitted between start_date and end_date.

        Parameters
        ----------
        start_date : datetime
            The start date for the search.
        end_date : datetime, optional
            The end date for the search. If None, defaults to the current date and time.
        max_results : int, optional
            The maximum number of results to return.

        """
        if end_date is None:
            end_date = datetime.now(timezone.utc)

        start_date = start_date.astimezone(timezone.utc)
        end_date = end_date.astimezone(timezone.utc)
        start_date = start_date.strftime("%Y%m%d%H%M")
        end_date = end_date.strftime("%Y%m%d%H%M")

        search = arxiv.Search(
            max_results=max_results,
            query=f"submittedDate:[{start_date} TO {end_date}]",
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Ascending,
        )

        try:
            for result in self.client.results(search):
                yield Paper(
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    subjects=result.categories,
                    abstract=result.summary,
                    submit=result.published,
                    pdf_url=result.pdf_url,
                    abs_url=result.entry_id,
                    journal="arXiv",
                    id=result.entry_id.split("/")[-1].split("v")[0],
                )
        except Exception as e:
            err_msg = f"Error fetching papers from arXiv: {e}"
            logger.exception(err_msg)
            raise RuntimeError(err_msg) from e
