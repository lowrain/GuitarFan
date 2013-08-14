from scrapy.item import Item, Field


class LetterArtistItem(Item):
    letter = Field()
    artists = Field()
    images = Field()
    image_urls = Field()


class TabItem(Item):
    artist = Field()
    title = Field()
    format = Field()
    images = Field()
    image_urls = Field()