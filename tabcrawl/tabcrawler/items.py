from scrapy.item import Item, Field


class LetterArtistItem(Item):
    letter = Field()
    artists = Field()


class ArtistTabItem(Item):
    artist = Field()
    tabs = Field()