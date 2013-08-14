BOT_NAME = 'tabcrawler'

SPIDER_MODULES = ['tabcrawler.spiders']
NEWSPIDER_MODULE = 'tabcrawler.spiders'
DOWNLOAD_DELAY = 3
ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
IMAGES_STORE = '/Users/jinzemin/Desktop/GuitarFan/tabcrawler/tabs'

# ITEM_PIPELINES = [
#     'tabcrawler.pipelines.ArtistPipeline',
# ]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tabcrawler (+http://www.yourdomain.com)'
