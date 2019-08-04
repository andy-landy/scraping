"""
Base Interface, for OOP fans
"""

class ISerpScraper:
    def scrap_image_urls_and_thumbs(self, query, count, filters):
        raise NotImplementedError()


class SerpScraperMock(ISerpScraper):
    def __init__(self, *args, **kwargs):
        pass

    def scrap_image_urls_and_thumbs(self, query, count, filters):
        return [('https://i5.walmartimages.ca/images/Large/062/0_r/6000191270620_R.jpg', '')] * count
