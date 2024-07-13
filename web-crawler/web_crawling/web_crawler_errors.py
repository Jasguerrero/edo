class WebCrawlerError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = f"Error crawling the web. HTTP Status code {errors}"

class NoResultsFoundError(ValueError):
    pass