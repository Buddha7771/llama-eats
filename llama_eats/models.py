from datetime import datetime

from pydantic import BaseModel


class Paper(BaseModel):
    """Base model containing metadata for an academic paper.

    Parameters
    ----------
    title : str
        The title of the paper.
    abstract : str
        The abstract of the paper.
    submit : datetime
        The submission date and time.
    abs_url : str
        URL to the paper's abstract page.
    id : str
        Unique identifier for the paper.
    journal : str
        The journal or repository where the paper is published.
    subjects : list[str], optional
        List of subject categories or topics, by default None.
    authors : list[str], optional
        List of paper authors, by default None.
    pdf_url : str , optional
        URL to the PDF version of the paper, by default None.

    """

    title: str
    abstract: str
    submit: datetime
    abs_url: str
    id: str
    journal: str
    subjects: list[str] | None = None
    authors: list[str] | None = None
    pdf_url: str | None = None


class NotionDatabaseEntry(BaseModel):
    """Base model representing a Notion database entry.

    Parameters
    ----------
    title: str
        Title of the paper.
    abstract: str
        Abstract of the paper.
    url: str
        URL of the paper.
    """

    title: str
    abstract: str
    url: str
