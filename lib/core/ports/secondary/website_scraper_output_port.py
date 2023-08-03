class WebsiteScraperOutputPort:
    """
    Interface for an output port of a website scraper.

    This interface defines the methods that an output port of a website scraper should implement.

    Methods:
    --------
    extract_text_from_html(url: str) -> str:
        Extracts text from the given HTML string and returns it as a string.
    """
    def extract_text_from_html(self, url: str) -> str:
        """
        Extracts text from the given HTML string and returns it as a string.

        Parameters:
        -----------
        url : str
            The HTML string to extract text from.

        Returns:
        --------
        str
            The extracted text as a string.
        """
        raise NotImplementedError("Should have implemented this")